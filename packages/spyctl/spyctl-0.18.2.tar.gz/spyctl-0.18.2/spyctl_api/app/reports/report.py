from __future__ import annotations

import datetime
import time
from typing import Optional, Tuple

import ulid
from pydantic import BaseModel, Field

import app.reports.report_lib as rlib

_future = 32503680000.0  # Timestamp of 3000-01-01 00:00:00


class Report(BaseModel):
    id: Optional[str] = Field(None, title="Id of the report")
    input: rlib.ReportInput = Field(title="Input for the report")
    status: rlib.STATUSES = Field(
        title="Status of the report generation", default="scheduled"
    )
    formats: list[rlib.FORMATS] = Field(
        title="List of formats the report is available in", default=[]
    )
    error: Optional[str] = Field(
        title="Error message if the report failed", default=None
    )
    change_log: list[Tuple[float, dict]] = Field(
        title="Log of changes to the report", default=[]
    )

    def __init__(self, **kw):
        super().__init__(**kw)
        if "id" not in kw:
            # We want ids that are monotonically decreasing to help in returning
            # reports from the backend in order of most recent first.
            # We use ulid but pass in an int that is the year 3000 - current time
            self.id = str(ulid.from_timestamp(_future - time.time()))
            if self.input.report_tags is None:
                self.input.report_tags = {}
            self.input.report_tags["time_scheduled"] = time.time()

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
            if k == "status" and v == "published":
                if self.input.report_tags is None:
                    self.input.report_tags = {}
                self.input.report_tags[f"time_published"] = time.time()
        self.change_log.append((time.time(), kwargs))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "input": self.input.model_dump(),
            "status": self.status,
            "error": self.error,
            "change_log": self.change_log,
            "formats": self.formats,
        }

    @staticmethod
    def from_dict(data: dict) -> Report:
        report = Report.model_validate(data)
        report.id = data["id"]
        return report


class ReportListResult(BaseModel):
    reports: list[Report] = Field(title="List of reports")
    continuation_token: Optional[str] = Field(
        title="Next token to get more reports",
        default=None,
    )
