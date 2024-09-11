from __future__ import annotations
from datetime import datetime, timedelta
import asyncio
import json
from pathlib import Path
from typing import Tuple

from app.reports.report_engine import Report

""" Simple file backend, only used for testing, not for production
"""


def id_2_meta_path(id: str, org_uid: str) -> Path:
    return Path(f"reports/{org_uid}/meta/{id}.json")


def id_2_file_path(id: str, org_uid: str) -> Path:
    return Path(f"reports/{org_uid}/files/{id}.report")


def org_2_prefix_path(org_uid: str) -> Path:
    return Path(f"reports/{org_uid}/meta/")


class SimpleFileBackend:
    def __init__(self, backend_config: dict):
        self.dir = Path(backend_config["dir"])

    async def register_report(self, report: Report):
        try:
            fpath = self.dir / id_2_meta_path(report.id, report.input.org_uid)
            with open(fpath, "w") as f:
                json.dump(report.to_dict(), f)
        except Exception as e:
            raise self.handle_error(e)

    async def update_report(self, report: Report):
        await self.register_report(report)

    async def get_report(self, id: str, org_uid: str) -> Report:
        try:
            fpath = self.dir / id_2_meta_path(id, org_uid)
            with open(fpath, "r") as f:
                data = json.load(f)
                return Report.from_dict(data)
        except Exception as e:
            raise self.handle_error(e)

    async def delete_report(self, id: str, org_uid: str):
        try:
            fpath_meta = self.dir / id_2_meta_path(id, org_uid)
            fpath_file = self.dir / id_2_file_path(id, org_uid)
            fpath_meta.unlink()
            fpath_file.unlink()

        except Exception as e:
            raise self.handle_error(e)

    async def list_reports(self, org_uid: str):
        try:
            dir_path = self.dir / org_2_prefix_path(org_uid)
            rv = []
            for fpath in dir_path.glob("*.json"):
                with open(fpath, "r") as f:
                    data = json.load(f)
                    rv.append(Report.from_dict(data))
            return rv
        except Exception as e:
            raise self.handle_error(e)

    async def publish_report_file(
        self, report: Report, report_bytes: bytes
    ) -> None:

        try:
            fpath = self.dir / id_2_file_path(report.id, report.input.org_uid)
            with open(fpath, "wb") as f:
                f.write(report_bytes)
        except Exception as e:
            raise self.handle_error(e)

    async def download_report_file(self, id: str, org_uid: str) -> str:
        return str(self.dir / id_2_file_path(id, org_uid))

    def handle_error(self, e: Exception) -> Exception:
        if isinstance(e, FileNotFoundError):
            return KeyError(f"Report not found")
        elif isinstance(e, PermissionError):
            return PermissionError(f"Access denied")
        else:
            return e
