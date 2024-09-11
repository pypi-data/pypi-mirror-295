from __future__ import annotations

from importlib import resources as impresources
from pathlib import Path
from typing import Annotated, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.responses import FileResponse, Response, StreamingResponse

import app.config
import app.reports.report_engine as report_engine
import app.reports.report_lib as rlib
from app.reports.portfolio import samples
from app.reports.report import Report, ReportListResult
from app.reports.report_engine import ReportEngine, make_engine

router = APIRouter(prefix="/api/v1")
content_types = {
    "html": "text/html",
    "md": "text/markdown",
    "json": "application/json",
    "yaml": "text/yaml",
    "pdf": "application/pdf",
    "csv": "text/csv",
}


def get_engine():
    return make_engine(
        {
            "backend": {
                "kind": app.config.get("report_backend_kind", fallback="s3"),
                "aws_access_key_id": app.config.get("aws_access_key_id"),
                "aws_secret_access_key": app.config.get(
                    "aws_secret_access_key"
                ),
                "aws_role_arn": app.config.get("aws_role_arn"),
                "bucket": app.config.get("report_bucket", fallback="reports"),
            }
        }
    )


EngineDep = Annotated[ReportEngine, Depends(get_engine)]


# ------------------------------------------------------------------------------
# Report Service
# ------------------------------------------------------------------------------


@router.get(
    "/org/{org_uid}/report/inventory",
    response_model=rlib.ReportInventory,
    response_model_exclude_none=True,
)
def inventory(org_uid: str, engine: EngineDep) -> rlib.ReportInventory:
    inv = engine.get_inventory()["inventory"]
    filtered = {"inventory": [r for r in inv if r["id"] != "mocktest"]}
    return rlib.ReportInventory.model_validate(filtered)


@router.post(
    "/org/{org_uid}/report",
    response_model=Report,
    response_model_exclude_none=True,
)
def generate(
    org_uid: str,
    i: rlib.ReportGenerateInput,
    background_tasks: BackgroundTasks,
    engine: EngineDep,
) -> Report:

    if i.generate_user:
        if not i.report_tags:
            i.report_tags = {}
        i.report_tags["user_scheduled"] = i.generate_user
    core_input = rlib.ReportInput(
        org_uid=org_uid,
        report_id=i.report_id,
        report_args=i.report_args,
        report_tags=i.report_tags,
    )
    supported_formats = engine.get_supported_formats(i.report_id)
    report = Report(input=core_input, formats=supported_formats)
    background_tasks.add_task(
        engine.generate_report, report, i.api_key, i.api_url
    )
    return report


@router.get(
    "/org/{org_uid}/report/status/{id}",
    response_model=Report,
    response_model_exclude_none=True,
)
async def get_report_status(
    id: str, org_uid: str, engine: EngineDep
) -> Report:
    try:
        report = await engine.get_report(id, org_uid)
        return report
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f"Report {id} for org {org_uid} not found"
        )


@router.get("/org/{org_uid}/report/download/{id}.{format}")
async def download_report(
    org_uid: str, id: str, format: rlib.FORMATS, engine: EngineDep
):

    try:
        engine = report_engine.get_engine()
        content_type = content_types.get(format)
        if id.startswith("sample-"):
            # Sample reports are not stored in the backend
            sample = impresources.files(samples) / f"{id}.{format}"
            if not Path(str(sample)).exists():
                raise KeyError()
            response: Response = FileResponse(
                str(sample), media_type=content_type
            )
        else:
            report = await engine.get_report(id, org_uid)
            if report.status != "published":
                raise HTTPException(
                    status_code=404, detail="Report not published"
                )
            response = StreamingResponse(
                engine.download_report(id, org_uid, format),
                media_type=content_type,
            )
        response.headers["Content-Disposition"] = (
            f"attachment; filename={id}.{format}"
        )
        return response

    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Report {id}.{format} for org {org_uid} not found",
        )


@router.delete("/org/{org_uid}/report/{id}")
async def delete_report(org_uid: str, id: str, engine: EngineDep):

    try:
        await engine.delete_report(id, org_uid)
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f"Report {id} for org {org_uid} not found"
        )


@router.get("/org/{org_uid}/report/")
async def list_reports(
    org_uid: str, engine: EngineDep
) -> dict[str, list[Report]]:

    try:
        reports = await engine.list_reports(org_uid)
        return {"reports": reports}
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f"No reports found for org {org_uid}"
        )


@router.post(
    "/org/{org_uid}/report/",
    response_model=ReportListResult,
    response_model_exclude_none=True,
)
async def list_reports_v2(
    org_uid: str,
    engine: EngineDep,
    rli: Optional[rlib.ReportListInput] = rlib.ReportListInput(),
) -> ReportListResult:

    try:
        return await engine.list_reports_v2(org_uid, rli)
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f"No reports found for org {org_uid}"
        )
