from pathlib import Path
from typing import AsyncGenerator, Protocol, Optional

from app.reports.report import Report, ReportListResult
from app.reports.report_lib import FORMATS, ReportListInput


class ReportBackend(Protocol):

    async def register_report(self, report: Report): ...

    async def update_report(self, report: Report): ...

    async def get_report(self, id: str, org_uid: str) -> Report: ...

    async def delete_report(self, id: str, org_uid: str): ...

    async def delete_report_file(
        self, id: str, org_uid: str, format: FORMATS
    ): ...

    async def list_reports(self, org_uid: str) -> list[Report]: ...

    async def list_reports_v2(
        self, org_uid: str, rli: ReportListInput
    ) -> ReportListResult: ...

    async def publish_report_file(
        self, report: Report, format: FORMATS, report_path: Path
    ): ...

    async def download_report_file(
        self, id, org_uid: str, format: FORMATS
    ) -> AsyncGenerator[bytes, None]: ...


def get_backend(backend_config: dict) -> ReportBackend:
    match backend_config["kind"]:
        case "s3":
            from app.reports.storage.s3_backend import S3Backend

            return S3Backend(backend_config)
        case "simple_file":
            from app.reports.storage.simple_file_backend import (
                SimpleFileBackend,
            )

            return SimpleFileBackend(backend_config)
        case _:
            raise ValueError("Unsupported backend kind")
