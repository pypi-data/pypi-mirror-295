from __future__ import annotations

import asyncio
import importlib
import pkgutil
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import AsyncGenerator, Optional

import yaml

import app.reports.report_lib as rlib
import app.reports.storage.report_backend as report_backend
from app.reports.report import Report, ReportListResult
from app.reports.reporter import Reporter

_engine: Optional[ReportEngine] = None


class ReportEngine:
    def __init__(self, config: dict):
        self.backend_config = config["backend"]
        self.backend: report_backend.ReportBackend = (
            report_backend.get_backend(self.backend_config)
        )
        data = pkgutil.get_data("app", "reports/portfolio/inventory.yaml")
        if not data:
            raise ValueError("Inventory not found")
        self.inventory: dict = yaml.safe_load(data)

    def get_inventory(self) -> dict:
        return self.inventory

    async def generate_report(
        self, report: Report, api_key: str, api_url: str
    ):
        try:
            await self.backend.register_report(report)
            report_files = await self.make_reports(
                r=report, api_key=api_key, api_url=api_url
            )
            await asyncio.gather(
                *[
                    self.backend.publish_report_file(
                        report=report, format=fmt, report_path=path
                    )
                    for fmt, path in report_files.items()
                ]
            )
            report.update(status="published")
            await self.backend.update_report(report)
            return report_files

        except Exception as e:
            report.update(status="failed", error=repr(e))
            await self.backend.update_report(report)
            raise e

    async def get_report(self, id: str, org_uid: str) -> Report:
        return await self.backend.get_report(id, org_uid)

    async def download_report(
        self, id: str, org_uid: str, format: rlib.FORMATS
    ) -> AsyncGenerator[bytes, None]:
        async for chunk in self.backend.download_report_file(
            id, org_uid, format
        ):
            yield chunk

    async def delete_report(self, id: str, org_uid: str):
        # Get the report to get all the formats to delete
        report = await self.backend.get_report(id, org_uid)
        await asyncio.gather(
            *[
                self.backend.delete_report_file(id, org_uid, fmt)
                for fmt in report.formats
            ],
            self.backend.delete_report(id, org_uid),
        )

    async def list_reports(self, org_uid: str) -> list[Report]:
        return await self.backend.list_reports(org_uid)

    async def list_reports_v2(
        self, org_uid: str, rli: rlib.ReportListInput
    ) -> ReportListResult:
        return await self.backend.list_reports_v2(org_uid, rli)

    def get_report_spec(self, report: str):
        reports = self.get_inventory()["inventory"]
        spec = [r for r in reports if r["id"] == report]
        if not spec:
            raise ValueError(f"Report {report} not found")
        return spec[0]

    def get_supported_formats(self, report: str):
        spec = self.get_report_spec(report)
        return spec["supported_formats"]

    def get_reporter(self, report: str) -> Reporter:
        spec = self.get_report_spec(report)
        reporter_str = spec["reporter"]
        mod_str, cls_str = reporter_str.rsplit(".", 1)
        mod = importlib.import_module(mod_str)
        cls = getattr(mod, cls_str)
        return cls(spec)

    async def make_reports(
        self, r: Report, api_key: str, api_url: str
    ) -> dict[rlib.FORMATS, Path]:
        i = r.input
        rid = r.id
        reporter = self.get_reporter(i.report_id)

        loop = asyncio.get_running_loop()
        with ProcessPoolExecutor() as executor:
            result = await loop.run_in_executor(
                executor, reporter.generate_reports, r, api_key, api_url
            )
        return result


def make_engine(config: dict) -> ReportEngine:
    global _engine
    if not _engine:
        _engine = ReportEngine(config)
    return _engine


def get_engine() -> ReportEngine:
    global _engine
    if not _engine:
        raise ValueError("Report engine not initialized")
    return _engine
