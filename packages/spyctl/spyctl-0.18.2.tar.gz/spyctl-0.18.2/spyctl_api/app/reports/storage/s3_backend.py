from __future__ import annotations

import asyncio
import json
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import AsyncGenerator, Optional, Tuple

import aioboto3
from botocore.exceptions import ClientError

from app.reports.report import Report, ReportListResult
from app.reports.report_lib import FORMATS, ReportListInput

REPORTLIST_PAGE_SIZE = 20


def id_2_meta_key(id: str, org_uid: str) -> str:
    return f"reports/{org_uid}/meta/{id}.json"


def meta_key_2_id(key: str) -> Tuple[str, str]:
    parts = key.split("/")
    return parts[-1].split(".")[0], parts[-2]


def id_2_file_key(id: str, org_uid: str, format: FORMATS) -> str:
    return f"reports/{org_uid}/files/{id}.{format}"


def org_2_prefix(org_uid: str) -> str:
    return f"reports/{org_uid}/meta/"


class S3Backend:
    def __init__(self, backend_config: dict):
        self.bucket = backend_config["bucket"]
        self.aws_access_key_id = backend_config.get("aws_access_key_id")
        self.aws_secret_access_key = backend_config.get(
            "aws_secret_access_key"
        )
        self.aws_role_arn = backend_config.get("aws_role_arn")
        self.session = None
        self.assumed_role = None

    async def ensure_session(self):
        # if we already have a session, we just need to check if we are
        # using an assumed role and it's creds aren't expired yet.
        if self.session:
            if not self.aws_role_arn:
                return
            if self.assumed_role:
                expiration = self.assumed_role["Credentials"]["Expiration"]
                if datetime.now(expiration.tzinfo) < expiration - timedelta(
                    minutes=5
                ):
                    return

        if self.aws_access_key_id and self.aws_secret_access_key:
            self.session = aioboto3.Session(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
            )

            if self.aws_role_arn:
                async with self.session.client("sts") as sts_client:
                    self.assumed_role = await sts_client.assume_role(
                        RoleArn=self.aws_role_arn, RoleSessionName="gd"
                    )
                    creds = self.assumed_role["Credentials"]
                    self.session = aioboto3.Session(
                        aws_access_key_id=creds["AccessKeyId"],
                        aws_secret_access_key=creds["SecretAccessKey"],
                        aws_session_token=creds["SessionToken"],
                    )
            return

        self.session = aioboto3.Session()

    async def register_report(self, report: Report):
        await self.ensure_session()
        async with self.session.client("s3") as s3:  # type: ignore
            try:
                await s3.put_object(
                    Bucket=self.bucket,
                    Key=id_2_meta_key(report.id, report.input.org_uid),  # type: ignore
                    Body=json.dumps(report.to_dict()),
                )
            except Exception as e:
                raise self.handle_error(e)

    async def update_report(self, report: Report):
        # Check if report is still there
        await self.ensure_session()
        try:
            existing = await self.get_report(report.id, report.input.org_uid)  # type: ignore
            await self.register_report(report)
        except Exception as e:
            raise self.handle_error(e)

    async def get_report(self, id: str, org_uid: str) -> Report:
        await self.ensure_session()
        async with self.session.client("s3") as s3:  # type: ignore
            try:
                response = await s3.get_object(
                    Bucket=self.bucket, Key=id_2_meta_key(id, org_uid)
                )
                data = await response["Body"].read()
                report = Report.from_dict(json.loads(data))
                return report
            except Exception as e:
                raise self.handle_error(e)

    async def delete_report(self, id: str, org_uid: str):
        await self.ensure_session()
        async with self.session.client("s3") as s3:  # type: ignore
            try:
                await s3.delete_object(
                    Bucket=self.bucket, Key=id_2_meta_key(id, org_uid)
                )
            except Exception as e:
                raise self.handle_error(e)

    async def delete_report_file(self, id: str, org_uid: str, format: FORMATS):
        await self.ensure_session()
        async with self.session.client("s3") as s3:  # type: ignore
            try:
                await s3.delete_object(
                    Bucket=self.bucket, Key=id_2_file_key(id, org_uid, format)
                )
            except Exception as e:
                raise self.handle_error(e)

    async def list_reports(self, org_uid: str):
        # TODO - this interface needs to become an async generator
        rv = []
        await self.ensure_session()
        async with self.session.client("s3") as s3:  # type: ignore
            # List all files under the common key
            response = await s3.list_objects_v2(
                Bucket=self.bucket, Prefix=org_2_prefix(org_uid)
            )
            for item in response.get("Contents", []):
                file_key = item["Key"]
                # Download each file
                response = await s3.get_object(
                    Bucket=self.bucket, Key=file_key
                )
                data = await response["Body"].read()
                rv.append(Report.from_dict(json.loads(data)))
        return rv

    async def next_s3_batch(
        self, org_uid: str, next_s3_token: Optional[str]
    ) -> list:
        async with self.session.client("s3") as s3:  # type: ignore
            args: dict = dict(
                Bucket=self.bucket,
                Prefix=org_2_prefix(org_uid),
                MaxKeys=REPORTLIST_PAGE_SIZE,
            )
            if next_s3_token:
                args["StartAfter"] = next_s3_token
            response = await s3.list_objects_v2(**args)
            return response.get("Contents", [])

    async def list_reports_v2(
        self,
        org_uid: str,
        rli: ReportListInput,
    ) -> ReportListResult:

        await self.ensure_session()
        now = time.time()
        if not rli.scheduled_time_to:
            rli.scheduled_time_to = now
        if not rli.scheduled_time_from:
            rli.scheduled_time_from = now - 60 * 60 * 24 * 7

        # Add a minute of margin around beginning and ending
        # to account for clock skew between AWS and us
        rli.scheduled_time_from -= 60
        rli.scheduled_time_to += 60

        candidates = []
        if rli.continuation_token:
            next_s3_token = id_2_meta_key(rli.continuation_token, org_uid)
        else:
            next_s3_token = None
        s3_objects_remaining = True
        report_ls = []
        while len(report_ls) < REPORTLIST_PAGE_SIZE and s3_objects_remaining:
            candidates = await self.next_s3_batch(org_uid, next_s3_token)
            s3_objects_remaining = len(candidates) > 0
            if s3_objects_remaining:
                next_s3_token = candidates[-1]["Key"]
            report_ls += self.report_filter(candidates, rli)

        if len(report_ls) < REPORTLIST_PAGE_SIZE:
            to_return = report_ls
            # At the end of the iteration, set next_token to None ..
            next_token = None

        else:
            to_return = report_ls[:REPORTLIST_PAGE_SIZE]
            next_key = report_ls[REPORTLIST_PAGE_SIZE - 1]["Key"]
            next_token, _ = meta_key_2_id(next_key)

        # Hydrate the reports
        reports_meta = await asyncio.gather(
            *[self.get_report_meta(report["Key"]) for report in to_return]
        )
        return ReportListResult(
            reports=reports_meta, continuation_token=next_token
        )

    def report_filter(
        self, candidates: list[dict], rli: ReportListInput
    ) -> list[dict]:
        schedule_time_from = rli.scheduled_time_from
        schedule_time_to = rli.scheduled_time_to
        return [
            report
            for report in candidates
            if schedule_time_from
            <= report["LastModified"].timestamp()
            <= schedule_time_to
        ]

    async def get_report_meta(self, key: str) -> Report:
        async with self.session.client("s3") as s3:
            start = time.time()
            response = await s3.get_object(Bucket=self.bucket, Key=key)
            t1 = time.time()
            data = await response["Body"].read()
            t2 = time.time()
            report = Report.from_dict(json.loads(data))
            end = time.time()
            return report

    async def publish_report_file(
        self, report: Report, format: FORMATS, report_path: Path
    ) -> None:

        await self.ensure_session()
        async with self.session.client("s3") as s3:  # type: ignore
            try:
                await s3.upload_file(
                    Filename=str(report_path),
                    Bucket=self.bucket,
                    Key=id_2_file_key(report.id, report.input.org_uid, format),  # type: ignore
                )
            except Exception as e:
                raise self.handle_error(e)

    async def download_report_file(
        self, id: str, org_uid: str, format: FORMATS
    ) -> AsyncGenerator[bytes, None]:
        await self.ensure_session()
        async with self.session.client("s3") as s3:  # type: ignore
            try:
                key = id_2_file_key(id, org_uid, format)
                response = await s3.get_object(Bucket=self.bucket, Key=key)
                async for chunk in response["Body"].iter_chunks():
                    yield chunk
            except Exception as e:
                raise self.handle_error(e)

    def handle_error(self, e: Exception) -> Exception:
        if isinstance(e, ClientError):
            if e.response["Error"]["Code"] in ["NoSuchKey", "404"]:
                return KeyError(f"Report not found")
            elif e.response["Error"]["Code"] == "AccessDenied":
                return PermissionError(f"Access denied")
            elif e.response["Error"]["Code"] == "BucketNotFound":
                return ValueError(f"s3 backend bucket not found")
            else:
                return ValueError(f"s3 backend error: {e}")
        else:
            return e
