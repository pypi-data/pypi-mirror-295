from __future__ import annotations

import json
import time
from collections import defaultdict
from copy import deepcopy
from datetime import datetime
from typing import Optional, Tuple

import spyctl.resources.api_filters as _af
from spyctl.api.agents import get_agent_metrics, get_agents

from app.reports.reporter import Reporter
import app.reports.mdx_lib as mdx_lib

from . import agent_stats

s_cluster = "model_k8s_cluster"
s_node = "model_k8s_node"
s_event_metrics = "event_metric:agent"

report_schemas = [s_cluster, s_node, s_event_metrics]


def make_index(rec_list: list, schemas: list[str]) -> Tuple[dict, dict]:
    index = dict()
    schema_index = defaultdict(dict)
    for rec in rec_list:
        for schema in schemas:
            if schema in rec["schema"]:
                index[rec["id"]] = rec
                schema_index[schema][rec["id"]] = rec
    return index, schema_index


class AgentMetricsReporter(Reporter):
    def collector(
        self,
        args: dict[str, str | float | int | bool],
        org_uid: str,
        api_key: str,
        api_url: str,
    ) -> list:

        sources = [f"global:{org_uid}"]
        filters = {"cluster": args["cluster"]}
        pipeline = _af.Agents.generate_pipeline(
            None, None, True, filters=filters
        )
        st = int(args["st"])
        et = int(args["et"])
        agent_st = st_at_least_2hrs(st)
        agents = list(
            get_agents(
                api_url,
                api_key,
                org_uid,
                sources,
                time=(agent_st, et),
                pipeline=pipeline,
                limit_mem=False,
                disable_pbar_on_first=True,
            )
        )

        sources = [agent["muid"] for agent in agents]
        pipeline = _af.AgentMetrics.generate_pipeline()
        metrics = get_agent_metrics(
            api_url,
            api_key,
            org_uid,
            sources,
            (agent_st, et),
            pipeline,
            limit_mem=False,
            disable_pbar=True,
        )
        return agents + list(metrics)

    def processor(
        self,
        data: list,
        args: dict[str, str | float | int | bool],
        format: Optional[str] = "md",
        mock: dict = {},
    ) -> dict:
        if not data:
            return {"error": {"message": "No data available"}}
        context = {}
        _index, schema_index = make_index(
            rec_list=data, schemas=report_schemas
        )

        # Cluster name
        context["cluster"] = {
            "name": args["cluster"],
        }

        context["st"] = int(args["st"])
        context["et"] = int(args["et"])

        # Filter event_metrics just to the ones for this cluster
        metrics = schema_index[s_event_metrics].values()

        # Compute stats
        stats = agent_stats.compute_stats(metrics)
        context["agent_metrics"] = stats["agents"]
        context["metrics_summary"] = stats["summary"]
        context.update(mock)
        return context

    def renderer(self, format: str, rid: str) -> Path:
        context = self.context
        if format == "mdx":
            mdx_context = self.make_mdx_context(context)
            return self.render(mdx_context, format, rid)
        else:
            return super().renderer(format, rid)

    def make_mdx_context(self, context: dict) -> dict:
        if "error" in context:
            return context
        mdx_context = deepcopy(context)
        mdx_context["st"] = datetime.fromtimestamp(context["st"]).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        mdx_context["et"] = datetime.fromtimestamp(context["et"]).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        summary_grid = self.make_summary_grid(context["metrics_summary"])
        mdx_context["metrics_summary"]["grid"] = summary_grid

        for metric in ["cpu", "mem", "bps"]:
            agent_grid = self.make_agent_grid(context["agent_metrics"], metric)
            mdx_context["agent_metrics"][metric] = {}
            mdx_context["agent_metrics"][metric]["grid"] = agent_grid
        return mdx_context

    def make_agent_grid(self, agent_metrics: dict, metric: str) -> str:
        match metric:
            case "cpu":
                type = None
            case "mem":
                type = "bytes"
            case "bps":
                type = "bytesPerSecond"
            case _:
                raise ValueError(f"Invalid metric: {metric}")
        columns = [
            {"title": "Agent", "field": "agent"},
            {
                "title": "Mean",
                "field": "mean",
            },
            {
                "title": "P90",
                "field": "p90",
            },
            {
                "title": "P99",
                "field": "p99",
            },
        ]
        if type:
            for col in columns:
                col["type"] = type
        data = [
            {
                "id": index,
                "agent": stats["name"],
                "mean": round(stats[metric]["mean"], 3),
                "p90": round(stats[metric]["p90"], 3),
                "p99": round(stats[metric]["p99"], 3),
            }
            for index, stats in enumerate(agent_metrics.values())
        ]
        return mdx_lib.make_grid(columns, data)

    def make_summary_grid(self, summary: dict) -> str:
        columns = [
            {"title": "Metric", "field": "metric"},
            {
                "title": "Mean",
                "field": "mean",
            },
            {
                "title": "P90",
                "field": "p90",
            },
            {
                "title": "P99",
                "field": "p99",
            },
        ]
        data = [
            {
                "metric": "CPU load",
                "mean": round(summary["cpu"]["mean"], 3),
                "p90": round(summary["cpu"]["p90"], 3),
                "p99": round(summary["cpu"]["p99"], 3),
            },
            {
                "metric": "Memory (MB)",
                "mean": f'{round(summary["mem"]["mean"] / 1048576)} MB',
                "p90": f'{round(summary["mem"]["p90"] / 1048576)} MB',
                "p99": f'{round(summary["mem"]["p99"] / 1048576)} MB',
            },
            {
                "metric": "Bandwidth (bytes/sec)",
                "mean": f'{round(summary["bps"]["mean"])}',
                "p90": f'{round(summary["bps"]["p90"])}',
                "p99": f'{round(summary["bps"]["p99"])}',
            },
        ]
        return mdx_lib.make_grid(columns, data)


def st_at_least_2hrs(st: float):
    two_hours_secs = 60 * 60 * 2
    now = time.time()
    if now - st < two_hours_secs:
        return now - two_hours_secs
    return st
