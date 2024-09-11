import sys
from typing import Any, Literal, Optional, Iterable, Callable
from datetime import datetime

import pandas as pd
from pydantic import BaseModel, Field


STATUSES = Literal["scheduled", "generated", "published", "failed"]
FORMATS = Literal["md", "mdx", "json", "yaml", "pdf", "html"]


class ReportGenerateInput(BaseModel):
    api_key: str = Field(
        title="API Key to access the backend data apis for the report"
    )
    api_url: str = Field(
        title="API URL to access the backend data apis for the report"
    )
    report_id: str = Field(title="Id of the report to generate")
    report_args: dict[str, str | float | int | bool | list] = Field(
        title="A dictionary of name/value pair arguments"
    )
    report_format: Optional[FORMATS] = Field(
        default="md", title="Format of the report to generate"
    )
    report_tags: Optional[dict[str, Any]] = Field(
        title="Tags to attach to the report", default={}
    )

    generate_user: Optional[str] = Field(
        title="User who requested the report", default=None
    )


class ReportInput(BaseModel):
    org_uid: str = Field(
        title="Organization Unique Id to generate the report for", default=None
    )
    report_id: str = Field(title="Id of the report to generate")
    report_args: dict[str, str | float | int | bool | list] = Field(
        title="A dictionary of name/value pair arguments"
    )
    report_tags: Optional[dict[str, Any]] = Field(
        title="Tags to attach to the report", default={}
    )


class ReportSpecArgument(BaseModel):
    name: str = Field(title="Name of the argument")
    short: str = Field(title="Short form description of the argument")
    description: str = Field(title="Description of the argument")
    required: bool = Field(title="Is the argument required")
    type: Literal[
        "cluster", "clustername", "timestamp", "muid", "machines"
    ] = Field(title="Type of the argument")
    default: Optional[Any] = Field(
        title="Suggested default value of the argument", default=None
    )


class ReportSpec(BaseModel):
    id: str = Field(title="Name of the report")
    short: str = Field(title="Short form description of the report")
    description: str = Field(title="Long form description of the report")
    args: list[ReportSpecArgument] = Field(
        title="List of arguments for the report"
    )
    supported_formats: list[FORMATS] = Field(
        title="List of supported formats for the report"
    )


class ReportInventory(BaseModel):
    inventory: list[ReportSpec] = Field(title="List of available reports")


class ReportListInput(BaseModel):
    scheduled_time_from: Optional[float] = Field(
        title="Scheduled time from", default=None
    )
    scheduled_time_to: Optional[float] = Field(
        title="Scheduled time to", default=None
    )
    continuation_token: Optional[str] = Field(
        title="Token to continue the list of reports", default=None
    )


def exists_at_time(model: dict, time: float) -> bool:
    exists = model["valid_from"] <= time and (
        "valid_to" not in model or time <= model["valid_to"]
    )
    return exists


def exists_in_window(model: dict, start: float, end: float) -> bool:
    in_window = model["valid_from"] <= end and (
        "valid_to" not in model or start <= model["valid_to"]
    )
    return in_window


def active_in_window(model: dict, start: float, end: float) -> bool:
    return exists_in_window(model, start, end) and model["status"] == "active"


def slice_and_project(
    last_models: dict,
    start: float,
    end: float,
    filter_and_project: Optional[Callable] = None,
):
    rv = []
    for x in last_models.values():
        if exists_in_window(x, start, end):
            to_add = x.copy()
            projected = filter_and_project(to_add) if filter_and_project else to_add
            if projected is not None:
                projected["time_slice"] = start
                rv.append(projected)
    return rv


def make_slice_projections(
    data_sorted,
    start=0,
    end=0,
    delta=300,
    last_models: dict= dict(),
    filter_and_project: Optional[Callable] = None,
) -> list[dict]:
    rv = []
    if start == 0:
        start = data_sorted[0]["time"]

    if end == 0:
        end = data_sorted[-1]["time"]

    st = datetime.fromtimestamp(start)
    et = datetime.fromtimestamp(end)
    st = st.replace(second=0, microsecond=0)
    et = et.replace(second=0, microsecond=0)

    i = st.timestamp()
    data_index = 0
    while i < et.timestamp():
        # Fill up last_models with data up to i + delta
        for d in data_sorted[data_index:]:
            if d["time"] < st.timestamp():
                data_index += 1
                continue
            if d["time"] > i + delta:
                break
            last_models[d["id"]] = d
            data_index += 1
        rv.extend(
            slice_and_project(last_models, i, i + delta, filter_and_project)
        )
        i += delta
    return rv


def time_slice(data, start, end, **kwargs):
    return [x for x in data if x["time"] >= start and x["time"] < end]


def get_size(obj, seen=None):
    """Recursively find the size of an object including its contents."""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, "__dict__"):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, "__iter__") and not isinstance(
        obj, (str, bytes, bytearray)
    ):
        size += sum([get_size(i, seen) for i in obj])
    return size


def df_to_dict(
    df: pd.DataFrame | pd.Series,
    drop_cols: list = [],
    apply_cols: dict = {},
) -> list:
    export = df.reset_index()
    export.drop(columns=drop_cols, inplace=True)
    for col, func in apply_cols.items():
        export[col] = export[col].apply(func)
    export.drop(columns=["time_slice_dt"], inplace=True)
    export.rename(columns={"id": "count"}, inplace=True)
    return export.to_dict(orient="records")
