"""Utility function for creating MDX rich data widgets"""

import json
import pandas as pd
from uuid import uuid4


def grid_project(
    columns: list[dict],
    data: list[dict],
    blank_repeated: bool = False,
) -> list[dict]:
    rv = []
    col_fields = [c["field"] for c in columns]
    prev = {key: None for key in col_fields}
    for rec in data:
        row = {}
        drop = True
        for key in col_fields:
            drop = drop and rec.get(key, "") == prev.get(key, "")
            row[key] = "" if drop and blank_repeated else rec.get(key, "")
        rv.append(row)
        prev = rec

    return rv


def make_grid(
    columns: list[dict],
    data: list[dict],
    options: dict = {},
    blank_repeated: bool = False,
) -> str:
    data = grid_project(columns, data, blank_repeated)
    for index in range(len(data)):
        data[index]["id"] = index

    return json.dumps(
        {
            "id": str(uuid4()),
            "columns": columns,
            "options": options,
            "data": data,
        },
        indent=4,
    )


def make_dataset(dataset_label: str, data: list, options: dict) -> dict:
    option_label = options.pop("label", None)
    label = option_label if option_label else dataset_label

    rv = {"label": label, "data": data, "options": options}
    return rv


def make_chart(type: str, options: dict, labels: list, datasets: list) -> str:
    if type in ["line", "bar"]:
        if options.get("stacked"):
            y_max = (
                max([sum(z) for z in zip(*[d["data"] for d in datasets])])
                * 1.1
            )
            y_min = min([sum(z) for z in zip(*[d["data"] for d in datasets])])
        else:
            y_max = max([max(d["data"]) for d in datasets]) * 1.1
            y_min = min([min(d["data"]) for d in datasets])
        y_min = min(0, y_min)
        chart_options = {"domain": {"y": [y_min, y_max]}}
        options.update(chart_options)
    rv = {
        "id": str(uuid4()),
        "type": type,
        "options": options,
        "data": {"labels": labels, "datasets": datasets},
    }
    return json.dumps(rv, indent=4)


def make_chart_df(
    type: str,
    df: pd.DataFrame,
    time_format: str | None = None,
    columns: list = [],
    chart_options: dict = {},
    dataset_options: dict[str, dict] = {},
) -> str:
    if time_format:
        labels = list(df.index.strftime(time_format))
    else:
        labels = [ts.timestamp() for ts in df.index]
    datasets = []
    df_selection = df[columns] if columns else df
    df_data = df_selection.to_dict(orient="list")
    datasets = [
        make_dataset(key, data, dataset_options.get(key, {}))
        for key, data in df_data.items()
    ]
    chart = make_chart(type, chart_options, labels, datasets)
    return chart


def make_grid_df(
    df: pd.DataFrame,
    grid_options: dict = {},
    column_options: dict[str, dict] = {},
    blank_repeated: bool = False,
):
    columns = []
    for c in df.columns:
        col_def = {
            "title": c.replace("_", " ").replace("-", " ").title(),
            "field": c,
        }
        col_def.update(column_options.get(c, {}))
        columns.append(col_def)

    data = df.to_dict(orient="records")
    return make_grid(columns, data, grid_options, blank_repeated)
