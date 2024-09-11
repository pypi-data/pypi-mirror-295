from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Tuple

import pandas as pd
import spyctl.api.athena_search as search_api
from spyctl.api.source_queries import retrieve_data
from spyctl.api.source_query_resources import get_machines

from app.reports.reporter import Reporter
from app.reports import mdx_lib


def new_machine() -> dict:
    return {
        "usage_hourly": {
            "labels": [],
            "load": {
                "p90": [],
                "p95": [],
                "mean": [],
            },
            "memory": {
                "p90": [],
                "p95": [],
                "mean": [],
            },
            "memory_percent": {
                "p90": [],
                "p95": [],
                "mean": [],
            },
            "network_in": {
                "p90": [],
                "p95": [],
                "mean": [],
            },
            "network_out": {
                "p90": [],
                "p95": [],
                "mean": [],
            },
        },
        "usage_daily": {
            "labels": [],
            "load": {
                "p90": [],
                "p95": [],
                "mean": [],
            },
            "memory": {
                "p90": [],
                "p95": [],
                "mean": [],
            },
            "memory_percent": {
                "p90": [],
                "p95": [],
                "mean": [],
            },
            "network_in": {
                "p90": [],
                "p95": [],
                "mean": [],
            },
            "network_out": {
                "p90": [],
                "p95": [],
                "mean": [],
            },
        },
    }


_to_friendly_metric = {
    "mem_used": "memory",
    "mem_used_percent": "memory_percent",
    "bytes_in": "network_in",
    "bytes_out": "network_out",
    "load": "load",
}

_to_friendly_unit = {0.9: "p90", 0.95: "p95", "mean": "mean"}


def load_usage_stat(usage, rec_stat):
    for key, value in rec_stat.items():
        if key == ("muid", ""):
            continue
        if key[0].startswith("time_"):
            usage["labels"].append(value.timestamp())
            continue

        metric, unit = key
        friendly_metric = _to_friendly_metric[metric]
        friendly_unit = _to_friendly_unit[unit]

        usage[friendly_metric][friendly_unit].append(value)


def update_context_dfs(
    context: dict, usage: pd.DataFrame, time_granularity: str
):
    for rec in usage.reset_index().to_dict(orient="records"):
        muid = rec[("muid", "")]
        load_usage_stat(
            context["machines"][muid][time_granularity],
            rec,
        )


class UsageReporter(Reporter):
    def collector(
        self,
        args: dict[str, str | float | int | bool],
        org_uid: str,
        api_key: str,
        api_url: str,
    ) -> list:

        et = args["time"]
        st = int(et) - 60 * 60 * 24 * 7
        rv = []

        query = f'id="{args["machines"][0]}"'
        if len(args["machines"]) > 1:
            for muid in args["machines"][1:]:
                query += f' or id="{muid}"'

        machines = search_api.search_athena(
            api_url,
            api_key,
            org_uid,
            schema="model_machine",
            query=query,
            start_time=st,
            end_time=et,
            use_pbar=False,
        )
        rv.append(list(machines))

        # Get machine metrics
        metrics = retrieve_data(
            api_url=api_url,
            api_key=api_key,
            org_uid=org_uid,
            sources=args["machines"],
            datatype="metric",
            schema="event_metric:machine",  # s_event_metrics,
            time=(st, et),
            pipeline=[],
            limit_mem=False,
            disable_pbar=True,
        )
        rv.append(list(metrics))

        return rv

    def processor(
        self,
        data: list,
        args: dict[str, str | float | int | bool | list],
    ) -> dict:
        if len(data) < 2:
            return {"error": {"message": "No data available"}}

        machines = data[0]
        metrics = data[1]
        if not machines or not metrics:
            return {"error": {"message": "No data available"}}

        context = {"machines": defaultdict(new_machine)}
        dr = []
        for r in metrics:
            mem_free = r["memory"]["free"]
            mem_total = r["memory"]["total"]
            mem_used = mem_total - mem_free
            if mem_total == 0:
                mem_used_percent = 0
            else:
                mem_used_percent = (mem_used / mem_total) * 100
            bytes_in = r["network"]["bytes_in"]
            bytes_out = r["network"]["bytes_out"]

            dr.append(
                {
                    "time": r["time"],
                    "muid": r["muid"],
                    "load": r["load_avg"][0],
                    "mem_used": mem_used,
                    "mem_used_percent": mem_used_percent,
                    "bytes_in": bytes_in,
                    "bytes_out": bytes_out,
                }
            )

        # This is a bit convoluted but it's to take into account with data gaps
        # We need to ensure we have data for every report period, both hourly
        # as daily. For that, in the pandas world, we need to have an index that
        # includes all the possible values for the time period. We can then apply
        # that index on the data, which will create entries with missing values (NaN)
        # We can then fill these up with 0s to show nothing in the data

        df = pd.DataFrame(dr)
        df["datetime"] = pd.to_datetime(df["time"], unit="s")

        # Make time columns floored to hour and to day
        df["time_hour"] = df["datetime"].dt.floor("h")
        df["time_day"] = df["datetime"].dt.floor("d")

        # Compute the quantiles and mean grouped my machine and hour/day
        # The unstack will make the quantile values (90, 95) to be part
        # of the column index.
        quantiles_hourly = (
            df.groupby(["muid", "time_hour"])[
                [
                    "load",
                    "mem_used",
                    "mem_used_percent",
                    "bytes_in",
                    "bytes_out",
                ]
            ]
            .quantile([0.9, 0.95])
            .unstack(level=-1)
        )

        quantiles_daily = (
            df.groupby(["muid", "time_day"])[
                [
                    "load",
                    "mem_used",
                    "mem_used_percent",
                    "bytes_in",
                    "bytes_out",
                ]
            ]
            .quantile([0.9, 0.95])
            .unstack(level=-1)
        )

        # Same thing for mean, daily and hourly
        mean_hourly = df.groupby(["muid", "time_hour"])[
            [
                "load",
                "mem_used",
                "mem_used_percent",
                "bytes_in",
                "bytes_out",
            ]
        ].mean()

        mean_daily = df.groupby(["muid", "time_day"])[
            [
                "load",
                "mem_used",
                "mem_used_percent",
                "bytes_in",
                "bytes_out",
            ]
        ].mean()

        # Now compute the full time index that includes all the possible time
        # periods for the reporting period (hourly, and daily)
        et = args["time"]
        st = int(et) - 60 * 60 * 24 * 7
        st_ts = pd.Timestamp(st, unit="s")
        et_ts = pd.Timestamp(et, unit="s")

        st_hourly = pd.Timestamp(
            year=st_ts.year, month=st_ts.month, day=st_ts.day, hour=st_ts.hour
        )
        st_daily = pd.Timestamp(
            year=st_ts.year, month=st_ts.month, day=st_ts.day
        )
        post = et_ts + pd.Timedelta(hours=1)
        et_hourly = pd.Timestamp(
            year=post.year, month=post.month, day=post.day, hour=post.hour
        )
        et_daily = pd.Timestamp(year=post.year, month=post.month, day=post.day)

        all_machines = args["machines"]
        all_hours = pd.date_range(st_hourly, et_hourly, freq="h")
        multi_index_hourly = pd.MultiIndex.from_product(
            [all_machines, all_hours], names=["muid", "time_hour"]
        )

        all_days = pd.date_range(st_daily, et_daily, freq="d")
        multi_index_daily = pd.MultiIndex.from_product(
            [all_machines, all_days], names=["muid", "time_day"]
        )

        # Now we can reindex the quantiles and mean dataframes to include all
        # time periods, even missing ones. We can fill these up with 0s
        quantiles_hourly = quantiles_hourly.reindex(multi_index_hourly)
        quantiles_hourly.fillna(0, inplace=True)
        quantiles_hourly = quantiles_hourly.stack(level=-1, future_stack=True)

        mean_hourly = mean_hourly.reindex(multi_index_hourly)
        mean_hourly.fillna(0, inplace=True)

        quantiles_daily = quantiles_daily.reindex(multi_index_daily)
        quantiles_daily.fillna(0, inplace=True)
        quantiles_daily = quantiles_daily.stack(level=-1, future_stack=True)

        mean_daily = mean_daily.reindex(multi_index_daily)
        mean_daily.fillna(0, inplace=True)

        # Now we just combine this all in a single dataframe, one for hourly, one for daily
        quantiles_daily = quantiles_daily.unstack(level=-1)
        quantiles_hourly = quantiles_hourly.unstack(level=-1)

        quantiles_daily.loc[:, ("load", "mean")] = mean_daily["load"]
        quantiles_daily.loc[:, ("mem_used", "mean")] = mean_daily["mem_used"]
        quantiles_daily.loc[:, ("mem_used_percent", "mean")] = mean_daily[
            "mem_used_percent"
        ]
        quantiles_daily.loc[:, ("bytes_in", "mean")] = mean_daily["bytes_in"]
        quantiles_daily.loc[:, ("bytes_out", "mean")] = mean_daily["bytes_out"]
        usage_daily = quantiles_daily.sort_index(axis=1)

        quantiles_hourly.loc[:, ("load", "mean")] = mean_hourly["load"]
        quantiles_hourly.loc[:, ("mem_used", "mean")] = mean_hourly["mem_used"]
        quantiles_hourly.loc[:, ("mem_used_percent", "mean")] = mean_hourly[
            "mem_used_percent"
        ]
        quantiles_hourly.loc[:, ("bytes_in", "mean")] = mean_hourly["bytes_in"]
        quantiles_hourly.loc[:, ("bytes_out", "mean")] = mean_hourly[
            "bytes_out"
        ]
        usage_hourly = quantiles_hourly.sort_index(axis=1)

        # Now we stuff it into the context so we can render it later
        update_context_dfs(context, usage_hourly, "usage_hourly")
        update_context_dfs(context, usage_daily, "usage_daily")

        # Add machine info
        for m in machines:
            cloud_name = None
            cloud_tags = m.get("cloud_tags")
            if cloud_tags:
                cloud_name = cloud_tags.get("Name", "")
            hostname = m["hostname"]
            display_name = cloud_name if cloud_name else hostname
            info = {
                "hostname": m["hostname"],
                "memory": m["machine_memory"],
                "processor": m["machine_processor"],
                "cores": m["machine_cores"],
                "os": m["os_system"],
                "os_version": m["os_version"],
                "os_distro_codename": m["os_distro"]["codename"],
                "muid": m["id"],
                "cloud_name": cloud_name,
                "display_name": display_name,
            }

            context["machines"][m["id"]]["info"] = info

        # Reporting time
        context["time"] = int(args["time"])
        context["et"] = args["time"]
        context["st"] = args["time"] - 60 * 60 * 24 * 7
        return context

    def renderer(self, format: str, rid: str) -> Path:
        context = self.context
        if format == "mdx":
            if "error" in context:
                return self.render(context, format, rid)

            mdx_context = self.make_mdx_context(context)
            mdx_context["st"] = datetime.fromtimestamp(context["st"]).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            mdx_context["et"] = datetime.fromtimestamp(context["et"]).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            return self.render(mdx_context, format, rid)
        else:
            return super().renderer(format, rid)

    def make_mdx_context(self, context: dict) -> dict:
        mdx_context = {
            "machines": context["machines"],
            "st": context["st"],
            "et": context["et"],
        }

        metric_options = {
            "load": {
                "yAxisTickFormat": {
                    "label": "load",
                }
            },
            "memory": {
                "yAxisTickFormat": {
                    "type": "bytes",
                    "label": "bytes",
                }
            },
            "network_in": {
                "yAxisTickFormat": {
                    "type": "bytesPerSecond",
                    "label": "Incoming traffic",
                }
            },
            "network_out": {
                "yAxisTickFormat": {
                    "type": "bytesPerSecond",
                    "label": "Outgoing traffic",
                }
            },
        }

        for muid, machine in context["machines"].items():
            for metric_type in ["load", "memory", "network_in", "network_out"]:
                title = metric_type.replace("_", " ").capitalize()
                chart = self.make_usage_chart(
                    machine,
                    metric_type=metric_type,
                    chart_type="line",
                    chart_options={
                        "title": f"{title} over time",
                        "yAxisTickFormat": metric_options[metric_type][
                            "yAxisTickFormat"
                        ],
                    },
                )
                mdx_context["machines"][muid][f"{metric_type}_chart"] = chart

                grid = self.make_usage_grid(machine, metric_type=metric_type)
                mdx_context["machines"][muid][f"{metric_type}_grid"] = grid

        return mdx_context

    def make_usage_chart(
        self,
        machine: dict,
        metric_type: str,
        chart_type: str,
        chart_options: dict,
    ):
        labels = machine["usage_hourly"]["labels"]
        datasets = [
            mdx_lib.make_dataset(
                f"Average {metric_type}",
                machine["usage_hourly"][metric_type]["mean"],
                {},
            ),
            mdx_lib.make_dataset(
                f"p90 {metric_type}",
                machine["usage_hourly"][metric_type]["p90"],
                {},
            ),
            mdx_lib.make_dataset(
                f"p95 {metric_type}",
                machine["usage_hourly"][metric_type]["p95"],
                {},
            ),
        ]
        chart = mdx_lib.make_chart(
            type=chart_type,
            options=chart_options,
            labels=labels,
            datasets=datasets,
        )
        return chart

    def make_usage_grid(self, machine: dict, metric_type: str) -> str:
        columns = [
            {"title": "Time period", "field": "time", "sorter": "string"},
            {
                "title": "Mean",
                "field": "mean",
            },
            {
                "title": "P90",
                "field": "p90",
            },
            {
                "title": "P95",
                "field": "p95",
            },
        ]
        if metric_type == "memory":
            for col in columns:
                col["type"] = "bytes"
        if metric_type in ["network_in", "network_out"]:
            for col in columns:
                col["type"] = "bytesPerSecond"
        data = []
        for relative_day in [-1, -2, -7]:
            time = {
                -1: "Last 24hr",
                -2: "One day earlier",
                -7: "One week earlier",
            }[relative_day]
            data.append(
                {
                    "time": time,
                    "mean": round(
                        machine["usage_daily"][metric_type]["mean"][
                            relative_day
                        ],
                        2,
                    ),
                    "p90": round(
                        machine["usage_daily"][metric_type]["p90"][
                            relative_day
                        ],
                        2,
                    ),
                    "p95": round(
                        machine["usage_daily"][metric_type]["p95"][
                            relative_day
                        ],
                        2,
                    ),
                }
            )
        return mdx_lib.make_grid(columns, data)
