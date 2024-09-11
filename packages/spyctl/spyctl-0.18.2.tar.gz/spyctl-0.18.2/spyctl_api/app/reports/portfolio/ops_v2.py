import json
import logging
from collections import Counter, defaultdict
from datetime import datetime
from functools import reduce
from typing import Any, Sequence, Tuple, Iterable, Literal
from datetime import datetime

import numpy as np
import pandas as pd
from spyctl.api.source_query_resources import get_cluster_full, get_nodes

import app.reports.mdx_lib as mdx_lib
import app.reports.report_lib as rlib
from app.reports.reporter import Reporter

s_cluster = "model_k8s_cluster:"
s_node = "model_k8s_node"
s_replicaset = "model_k8s_replicaset"
s_daemonset = "model_k8s_daemonset"
s_deployment = "model_k8s_deployment"
s_pod = "model_k8s_pod"
s_service = "model_k8s_service"
s_endpoint = "model_k8s_endpoint"
s_statefulset = "model_k8s_statefulset"
s_job = "model_k8s_job"
s_cronjob = "model_k8s_cronjob"
s_container = "model_container"
s_namespace = "model_k8s_namespace"
s_opsflags = "event_opsflag"
# s_event_metrics = "event_metric:agent"

k8s_schemas = [
    s_cluster,
    s_node,
    s_daemonset,
    s_deployment,
    s_pod,
    s_service,
    s_namespace,
]
report_schemas = [s_opsflags] + k8s_schemas

DATA_LOWER_LIMIT = 25_000
DATA_UPPER_LIMIT = 50_000

logger = logging.getLogger("uvicorn")


def make_index(rec_list: list, schemas: list[str]) -> Tuple[dict, dict]:
    index = dict()
    schema_index: dict = defaultdict(dict)
    for rec in rec_list:
        for schema in schemas:
            if schema in rec["schema"]:
                index[rec["id"]] = rec
                schema_index[schema][rec["id"]] = rec
    return index, schema_index


def get_resources(pod: dict):
    spec = pod.get("spec", {})
    if not spec:
        return {}
    containers = spec.get("containers", [])
    rv = {
        "limits_cpu": 0.0,
        "limits_memory": 0.0,
        "requests_cpu": 0.0,
        "requests_memory": 0.0,
    }
    for cont in containers:
        resources = cont.get("resources", {})
        if resources:
            rv["limits_cpu"] += convert_unit(
                resources.get("limits", {}).get("cpu", "0")
            )
            rv["limits_memory"] += convert_unit(
                resources.get("limits", {}).get("memory", "0")
            )
            rv["requests_cpu"] += convert_unit(
                resources.get("requests", {}).get("cpu", "0")
            )
            rv["requests_memory"] += convert_unit(
                resources.get("requests", {}).get("memory", "0")
            )
    return rv


def convert(x):
    if x == np.nan:
        return x
    if isinstance(x, float):
        return x
    if isinstance(x, int):
        return x
    if isinstance(x, str):
        return convert_unit(x)


def filter_and_project(model: dict) -> dict | None:

    rv = {
        "id": model["id"],
        "time": model["time"],
        "valid_from": model["valid_from"],
        "status": model["status"],
    }
    if "valid_to" in model:
        rv["valid_to"] = model["valid_to"]

    if model.get("kind") == "Pod":
        rv.update(
            {
                "kind": model["kind"],
                "name": model["metadata"]["name"],
                "namespace": model["metadata"]["namespace"],
                "node_name": model["spec"].get("nodeName"),
                "healthy": get_pod_health(model),
            }
        )
        rv.update(get_resources(model))
        return rv

    if model.get("kind") == "Node":
        rv.update(
            {
                "kind": model["kind"],
                "name": model["metadata"]["name"],
                "allocatable_cpu": model["k8s_status"]["allocatable"]["cpu"],
                "allocatable_memory": model["k8s_status"]["allocatable"][
                    "memory"
                ],
                "allocatable_pods": model["k8s_status"]["allocatable"]["pods"],
                "arch": model["k8s_status"]["nodeInfo"]["architecture"],
                "osImage": model["k8s_status"]["nodeInfo"]["osImage"],
                "containerRuntime": model["k8s_status"]["nodeInfo"][
                    "containerRuntimeVersion"
                ],
                "instance_type": model["metadata"]["labels"].get(
                    "node.kubernetes.io/instance-type", "unknown"
                ),
                "cores": int(model["k8s_status"]["capacity"]["cpu"]),
                "taints": model["spec"].get("taints", []),
                "control_plane": model["metadata"]["labels"].get(
                    "node-role.kubernetes.io/controlplane", False
                ),
            }
        )
        return rv

    if model.get("kind") in [
        "DaemonSet",
        "Deployment",
        "Service",
        "Namespace",
    ]:
        rv.update(
            {
                "kind": model["kind"],
                "name": model["metadata"]["name"],
                "namespace": model["metadata"].get("namespace"),
            }
        )

        if model.get("kind") in ["DaemonSet", "Deployment"]:
            rv["tolerations"] = (
                model["spec"]
                .get("template", {})
                .get("spec", {})
                .get("tolerations", [])
            )
        return rv

    if s_cluster in model["schema"]:
        rv.update(
            {
                "kind": "Cluster",
                "name": model["name"],
            }
        )
        return rv

    return None


class OpsReporter(Reporter):

    def __init__(self, spec: dict):
        super().__init__(spec)
        self.df: pd.DataFrame = pd.DataFrame()
        self.cluster_stats: pd.Series = pd.Series()
        self.pods_usage: pd.DataFrame = pd.DataFrame()
        self.pods_usage_ns: pd.DataFrame = pd.DataFrame()
        self.pods_usage_node: pd.DataFrame = pd.DataFrame()
        self.pods_usage_capacity: pd.DataFrame = pd.DataFrame()
        self.healthcheck: pd.DataFrame = pd.DataFrame()
        self.just_nodes: pd.DataFrame = pd.DataFrame()
        self.nodes_missing_agents: pd.DataFrame = pd.DataFrame()
        self.df_flags: pd.DataFrame = pd.DataFrame()

    def collector(
        self,
        args: dict[str, str | float | int | bool],
        org_uid: str,
        api_key: str,
        api_url: str,
    ) -> list:
        return []

    def processor(self, data: list, args: dict) -> dict:
        return {}

    def get_raw_data(
        self,
        st: float,
        et: float,
        cluid: str,
        org_uid: str,
        api_key: str,
        api_url: str,
        what: Literal["models", "opsflags"],
    ) -> Iterable[dict]:
        match what:
            case "models":
                sources = [f"{cluid}_base", f"{cluid}_poco"]
                projections = [
                    "id",
                    "schema",
                    "name",
                    "version",
                    "kind",
                    "metadata",
                    "spec",
                    "k8s_status",
                    "status",
                    "time",
                    "valid_from",
                    "valid_to",
                ]
                schema_filter = {
                    "filter": {
                        "or": [{"schema": schema} for schema in k8s_schemas]
                    }
                }
                projection_func = filter_and_project
            case "opsflags":
                sources = [f"{cluid}_flag"]
                projections = [
                    "id",
                    "version",
                    "schema",
                    "time",
                    "description",
                    "severity",
                    "linkback",
                ]
                schema_filter = {"filter": {"schema": s_opsflags}}
                projection_func = None
            case _:
                raise ValueError(f"Unsupported what argument: {what}")

        return get_cluster_full(
            api_url,
            api_key,
            org_uid,
            sources,
            (st, et),
            pipeline=[schema_filter, {"projection": projections}],
            limit_mem=False,
            disable_pbar=True,
            last_model=False,
            projection_func=projection_func,
        )

    def collect_and_process(
        self,
        args: dict[str, str | float | int | bool],
        org_uid: str,
        api_key: str,
        api_url: str,
    ):
        cluid = args["cluid"]

        start_time = int(args["st"])
        end_time = int(args["et"])

        # We want to have the query delta to alway be an integer
        # multiple of the slice delta, so there are no overlapping
        # slices between query window outputs
        # We are also trying to have a reasonable number of slices
        # in the report (not too many, not too few)
        query_delta = 60 * 60 * 6  # 6 hours
        report_delta = end_time - start_time

        if report_delta >= 24 * 60 * 60 * 2:  # more than 2 days
            slice_delta = 60 * 60  # 1 hour

        elif report_delta >= 24 * 60 * 60:  # more than 1 day
            slice_delta = 60 * 30  # 30 minutes

        elif report_delta >= 12 * 60 * 60:  # more than 12 hours
            slice_delta = 60 * 10  # 10 minutes

        elif report_delta >= 3 * 60 * 60:  # more than 3 hours
            slice_delta = 60 * 5  # 5 minutes

        else:  # less than 3 hours
            slice_delta = 60  # 1 minute

        # Split the start_time end_time interval into data query windows
        # collect data for each window, and slice the models up in
        # reporting slices where last_model semantics apply

        last_models = dict()
        st = start_time
        while st < end_time:
            et = min(st + query_delta, end_time)
            data = self.get_raw_data(
                st, et, cluid, org_uid, api_key, api_url, "models"
            )
            len_data = self.update_model_data(
                data=data,
                st=st,
                et=et,
                slice_delta=slice_delta,
                last_models=last_models,
            )
            self.update_flag_data(
                self.get_raw_data(
                    st, et, cluid, org_uid, api_key, api_url, "opsflags"
                )
            )
            progress = (et - start_time) / (end_time - start_time)
            logger.info(
                f"Ops report got data from {datetime.fromtimestamp(st)} "
                f"to {datetime.fromtimestamp(et)} (query window {(et-st)//3600} h): "
                f"{len_data} records - {progress:.0%}"
            )

            st = et

        # All dataframes are built-up - finalize context creation
        if self.df.empty:
            self.context = {"error": {"message": "No data available"}}
            return

        self.context = dict()

        # Cluster name and id
        self.context["cluster"] = (
            self.df[self.df["kind"] == "Cluster"]
            .head(1)[["name", "id"]]
            .iloc[0]
            .to_dict()
        )

        # Reporting period
        self.context["st"] = datetime.fromtimestamp(args["st"]).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        self.context["et"] = datetime.fromtimestamp(args["et"]).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Toleration analysis
        # Get nodes at end of reporting period
        i_last = self.cluster_stats.index[-1][0]
        cluster_monitors = self.df[
            (self.df["kind"] == "Deployment")
            & (self.df["name"].str.contains("clustermonitor"))
            & (self.df["time_slice_dt"] == i_last)
        ]
        cluster_monitor = cluster_monitors.groupby("id").last()

        nano_agent_daemonsets = self.df[
            (self.df["kind"] == "DaemonSet")
            & (self.df["name"].str.startswith("spyderbat-nano"))
            & (self.df["time_slice_dt"] == i_last)
        ]
        nano_agent_daemonset = nano_agent_daemonsets.groupby("id").last()

        i_last = self.cluster_stats.index[-1][0]

        nodes_df = self.df[
            (self.df["kind"] == "Node") & (self.df["status"] == "active")
        ]
        self.just_nodes = nodes_df[(nodes_df["time_slice_dt"] == i_last)][
            [
                "id",
                "name",
                "arch",
                "osImage",
                "containerRuntime",
                "instance_type",
                "cores",
                "taints",
                "control_plane",
            ]
        ]

        node_taints = get_node_taints(self.just_nodes)
        missing_tol_nano = check_tolerations(node_taints, nano_agent_daemonset)
        missing_tol_cm = check_tolerations(node_taints, cluster_monitor)
        self.context["missing_tol_nano"] = missing_tol_nano
        self.context["missing_tol_cm"] = missing_tol_cm

        # Flag to see if clustermonitor was down at end of reporting period
        self.context["clustermonitor_down"] = bool(
            self.healthcheck.iloc[-1]["clustermonitor_down"] == 1
        )

        if logger.level == logging.DEBUG:
            for df in [
                self.df,
                self.cluster_stats,
                self.pods_usage,
                self.pods_usage_ns,
                self.pods_usage_node,
                self.pods_usage_capacity,
                self.healthcheck,
                self.just_nodes,
                self.nodes_missing_agents,
                self.df_flags,
            ]:
                logger.debug(
                    f"Processor - Memory usage dataframe: {rlib.get_size(df):,}"
                )

    def update_flag_data(self, data: Iterable[dict]):
        if logger.level == logging.DEBUG:
            data = list(data)
            size_flags = rlib.get_size(data)
            logger.debug(f"Memory usage: flags: {size_flags:,}")

        self.df_flags = pd.concat(
            [self.df_flags, pd.DataFrame(data)],
            ignore_index=True,
        )

    def update_model_data(
        self,
        data: Iterable[dict],
        st: float,
        et: float,
        slice_delta: int,
        last_models: dict,
    ):
        data_sorted = sorted(data, key=lambda x: x["time"])
        len_data = len(data_sorted)
        if len_data == 0:
            return 0

        models_sliced = rlib.make_slice_projections(
            data_sorted,
            start=st,
            end=et,
            delta=slice_delta,
            last_models=last_models,
        )

        if logger.level == logging.DEBUG:
            size_models = rlib.get_size(data_sorted)
            size_models_sliced = rlib.get_size(models_sliced)
            logger.debug(f"Memory usage: models: {size_models:,}")
            logger.debug(
                f"Memory usage: sliced_models: {size_models_sliced:,}"
            )

        self.update_dataframes(models_sliced)
        return len_data

    def update_dataframe(
        self,
        orig: pd.DataFrame | pd.Series,
        update: pd.DataFrame | pd.Series,
        name: str = "",
        check_dupe_index: bool = True,
    ):
        if orig.empty:
            return update
        else:
            rv = pd.concat([orig, update])
            if check_dupe_index and (dupes := rv.index.duplicated()).any():
                logger.warning(f"Duplicate index/data: {name} ({len(dupes)})")
                rv = rv[~dupes]
            return rv

    def update_dataframes(self, data: list):
        if not data or len(data) == 0:
            return

        (
            df,
            cluster_stats,
            pods_usage,
            pods_usage_ns,
            pods_usage_node,
            pods_usage_capacity,
            healthcheck,
            nodes_missing_agents,
        ) = self.make_dataframes(data)

        self.df = self.update_dataframe(
            self.df, df, "df", check_dupe_index=False
        )
        self.cluster_stats = self.update_dataframe(
            self.cluster_stats,
            cluster_stats,
            "cluster_stats",
        )
        self.pods_usage = self.update_dataframe(
            self.pods_usage, pods_usage, "pods_usage"
        )
        self.pods_usage_ns = self.update_dataframe(
            self.pods_usage_ns,
            pods_usage_ns,
            "pods_usage_ns",
        )
        self.pods_usage_node = self.update_dataframe(
            self.pods_usage_node,
            pods_usage_node,
            "pods_usage_node",
        )
        self.pods_usage_capacity = self.update_dataframe(
            self.pods_usage_capacity,
            pods_usage_capacity,
            "pods_usage_capacity",
        )
        self.healthcheck = self.update_dataframe(
            self.healthcheck, healthcheck, "healthcheck"
        )
        self.nodes_missing_agents = self.update_dataframe(
            self.nodes_missing_agents,
            nodes_missing_agents,
            "node_missing_agents",
            check_dupe_index=False,
        )
        # Keep only last one for each node missing an agent across all intervals
        self.nodes_missing_agents = self.nodes_missing_agents.groupby(
            "id"
        ).last()

    def make_dataframes(self, data: list) -> tuple:
        df = pd.DataFrame(data)

        # Cleanup and type conversions
        df["time_dt"] = pd.to_datetime(df["time"], unit="s")
        df["time_slice_dt"] = pd.to_datetime(df["time_slice"], unit="s")
        df["allocatable_cpu"] = df["allocatable_cpu"].apply(convert)
        df["allocatable_memory"] = df["allocatable_memory"].apply(convert)
        df["allocatable_pods"] = df["allocatable_pods"].apply(convert)

        cluster_stats = (
            df[df["status"] == "active"]
            .groupby(["time_slice_dt", "kind"])["id"]
            .nunique()
        )
        # Pod requested resources over time
        pods_usage = (
            df[(df["kind"] == "Pod") & (df["status"] == "active")]
            .groupby(["time_slice_dt"])
            .agg(
                {
                    "requests_cpu": "sum",
                    "requests_memory": "sum",
                    "id": "nunique",
                }
            )
            .rename(columns={"id": "nr_pods"})
        )

        # Pod requested resources over time, grouped by namespace
        pods_usage_ns = (
            df[(df["kind"] == "Pod") & (df["status"] == "active")]
            .groupby(["time_slice_dt", "namespace"])
            .agg(
                {
                    "requests_cpu": "sum",
                    "requests_memory": "sum",
                    "id": "nunique",
                }
            )
            .rename(columns={"id": "nr_pods"})
            .fillna(0)
        )

        # Pod requested resources over time, grouped by node
        pods_usage_node = (
            df[(df["kind"] == "Pod") & (df["status"] == "active")]
            .groupby(["time_slice_dt", "node_name"])
            .agg(
                {
                    "requests_cpu": "sum",
                    "requests_memory": "sum",
                    "id": "nunique",
                }
            )
            .rename(columns={"id": "nr_pods"})
            .fillna(0)
        )

        # Allocatable resource capacity over time in nodes
        nodes_df = df[(df["kind"] == "Node") & (df["status"] == "active")]
        node_capacity = nodes_df.groupby(["time_slice_dt"]).agg(
            {
                "allocatable_cpu": "sum",
                "allocatable_memory": "sum",
                "allocatable_pods": "sum",
            }
        )

        # Merge usage dataframes
        pods_usage_capacity = pd.merge(
            pods_usage, node_capacity, on="time_slice_dt", how="outer"
        ).fillna(0)

        # Health checks nano agent
        nodes_with_nanoagents = (
            df[
                (df["kind"] == "Pod")
                & (df["status"] == "active")
                & (df["healthy"])
                & (df["name"].str.startswith("spyderbat-nano"))
            ]
            .groupby(["time_slice_dt"])["node_name"]
            .unique()
            .rename("nodes_with_nanoagents")
        )

        all_nodes = (
            df[(df["kind"] == "Node") & (df["status"] == "active")]
            .groupby(["time_slice_dt"])["name"]
            .unique()
            .rename("all_nodes")
        )
        healthcheck = pd.merge(
            nodes_with_nanoagents, all_nodes, on="time_slice_dt", how="outer"
        )
        # Fill out any missing values with empty lists
        healthcheck = healthcheck.apply(
            lambda col: col.apply(
                lambda x: x if isinstance(x, Iterable) else []
            )
        )

        healthcheck["nodes_missing_agents"] = healthcheck.apply(
            lambda x: list(
                set(x["all_nodes"]) - set(x["nodes_with_nanoagents"])
            ),
            axis=1,
        )
        healthcheck["nr_nodes"] = healthcheck["all_nodes"].apply(len)
        healthcheck["nr_nodes_unhealthy"] = healthcheck[
            "nodes_missing_agents"
        ].apply(len)
        healthcheck["nr_nodes_healthy"] = (
            healthcheck["nr_nodes"] - healthcheck["nr_nodes_unhealthy"]
        )

        cm_up = (
            df[
                (df["kind"] == "Pod")
                & (df["status"] == "active")
                & (df["healthy"])
                & (df["name"].str.startswith("clustermonitor"))
            ]
            .groupby(["time_slice_dt"])["name"]
            .nunique()
            .astype(bool)
            .astype(int)
            .fillna(0)
        )
        # The cast to bool and then back to int is to convert any nr of clustermonitors
        # higher than 1 (it's running) to a 1 for the chart

        healthcheck["clustermonitor_up"] = cm_up
        healthcheck["clustermonitor_down"] = (
            1 - healthcheck["clustermonitor_up"]
        )
        # If we have no data, we don't know if it was up or down
        healthcheck.fillna(
            {"clustermonitor_up": 0, "clustermonitor_down": 0}, inplace=True
        )

        nodes_missing = reduce(
            set.union, healthcheck["nodes_missing_agents"].apply(set)
        )
        healthcheck["nodes_missing_agents"].apply(list)
        nodes_missing_agents = (
            nodes_df[nodes_df["name"].isin(nodes_missing)].groupby("id").last()
        )

        return (
            df,
            cluster_stats,
            pods_usage,
            pods_usage_ns,
            pods_usage_node,
            pods_usage_capacity,
            healthcheck,
            nodes_missing_agents,
        )

    def renderer(
        self,
        fmt: str,
        rid: str,
    ) -> Any:

        context = self.context
        if "error" in context:
            return self.render(context, fmt, rid)

        if fmt in ["json", "yaml"]:
            ctx = context.copy()
            ctx["cluster_stats"] = rlib.df_to_dict(
                self.cluster_stats,
                apply_cols={"time_slice_dt": lambda x: x.timestamp()},
            )
            ctx["pods_usage"] = rlib.df_to_dict(
                self.pods_usage,
                apply_cols={"time_slice_dt": lambda x: x.timestamp()},
            )
            ctx["pods_usage_ns"] = rlib.df_to_dict(
                self.pods_usage_ns,
                apply_cols={"time_slice_dt": lambda x: x.timestamp()},
            )
            ctx["pods_usage_node"] = rlib.df_to_dict(
                self.pods_usage_node,
                apply_cols={"time_slice_dt": lambda x: x.timestamp()},
            )
            ctx["pods_usage_capacity"] = rlib.df_to_dict(
                self.pods_usage_capacity,
                apply_cols={"time_slice_dt": lambda x: x.timestamp()},
            )
            ctx["healthcheck"] = rlib.df_to_dict(
                self.healthcheck,
                apply_cols={
                    "nodes_missing_agents": list,
                    "nodes_with_nanoagents": list,
                    "all_nodes": list,
                },
            )
            ctx["nodes_missing_agents"] = rlib.df_to_dict(
                self.nodes_missing_agents,
                drop_cols=["time_dt"],
            )

        if fmt == "mdx":
            ctx = context.copy()

            # Cluster stats grid
            i_last = self.cluster_stats.index[-1][0]

            # First time period can be incomplete so we take the second one
            i_first = self.cluster_stats.unstack().index[1]

            d_last = self.cluster_stats.loc[i_last, :].to_dict()
            d_first = self.cluster_stats.loc[i_first, :].to_dict()

            columns = []
            columns.append({"title": "Time period", "field": "time_period"})
            columns.extend(
                [
                    {"title": key, "field": key}
                    for key in d_last
                    if key != "Cluster"
                ]
            )

            d_last["time_period"] = "End of reporting period"
            d_first["time_period"] = "Start of reporting period"

            grid = mdx_lib.make_grid(columns, [d_last, d_first])
            ctx["cluster_stat_grid"] = grid

            # Nodes information grid
            node_records = self.just_nodes.to_dict(orient="records")
            node_count = len(node_records)
            columns = [
                {"title": "Property", "field": "name"},
                {"title": "Value", "field": "value"},
                {"title": "Count", "field": "prop_count"},
            ]
            node_summary = get_node_summary(node_records)
            data = friendly_node_summary(node_summary)
            data = [
                {
                    "id": index,
                    "name": d["name"],
                    "value": d["value"],
                    "prop_count": f'{d["prop_count"]}/{node_count}',
                }
                for index, d in enumerate(data)
            ]
            grid = mdx_lib.make_grid(columns, data)
            ctx["node_summary_grid"] = grid

            # Pod usage chart
            pods_usage_chart = mdx_lib.make_chart_df(
                "line",
                self.pods_usage_capacity,
                columns=["nr_pods", "allocatable_pods"],
                chart_options={
                    "title": "Pod usage vs allocatable pod capacity",
                    "yAxisTickFormat": {
                        "label": "Nr of pods",
                    },
                },
            )
            ctx["pods_usage_chart"] = pods_usage_chart

            # Pod cpu usage chart
            pods_cpu_chart = mdx_lib.make_chart_df(
                "line",
                self.pods_usage_capacity,
                columns=["requests_cpu", "allocatable_cpu"],
                chart_options={
                    "title": "Pod CPU request vs allocatable cpu capacity",
                    "yAxisTickFormat": {
                        "label": "CPU request",
                    },
                },
            )
            ctx["pods_cpu_chart"] = pods_cpu_chart

            # Pod memory usage chart
            pods_memory_chart = mdx_lib.make_chart_df(
                "line",
                self.pods_usage_capacity,
                columns=["requests_memory", "allocatable_memory"],
                chart_options={
                    "title": "Pod Memory requests vs allocatable memory capacity",
                    "yAxisTickFormat": {
                        "label": "Memory request",
                        "type": "bytes",
                    },
                },
            )
            ctx["pods_memory_chart"] = pods_memory_chart

            # Pod usage by namespace
            pods_usage_ns_chart = mdx_lib.make_chart_df(
                "line",
                self.pods_usage_ns["nr_pods"].unstack().fillna(0),
                chart_options={
                    "title": "Number of pods per namespace",
                    "yAxisTickFormat": {
                        "label": "Nr of pods",
                    },
                },
            )
            ctx["pods_usage_ns_chart"] = pods_usage_ns_chart

            # Pod usage by nodes
            # we'll be skipping this chart if the nr of nodes is too high (more than 15)
            if self.df["node_name"].nunique() <= 15:
                pods_usage_node_chart = mdx_lib.make_chart_df(
                    "line",
                    self.pods_usage_node["nr_pods"].unstack().fillna(0),
                    chart_options={
                        "title": "Number of pods per node",
                        "yAxisTickFormat": {
                            "label": "Nr of pods",
                        },
                    },
                )
                ctx["pods_usage_node_chart"] = pods_usage_node_chart

            # Node health
            nano_agent_chart = mdx_lib.make_chart_df(
                type="bar",
                df=self.healthcheck[
                    ["nr_nodes_healthy", "nr_nodes_unhealthy"]
                ],
                chart_options={
                    "stacked": True,
                    "title": "Nano agent health across nodes over time",
                    "yAxisTickFormat": {
                        "label": "Nr of nano agents",
                    },
                },
                dataset_options={
                    "nr_nodes_healthy": {
                        "color": "green",
                        "label": "Healthy",
                    },
                    "nr_nodes_unhealthy": {
                        "color": "red",
                        "label": "Unhealthy",
                    },
                },
            )
            ctx["nano_agent_chart"] = nano_agent_chart

            clustermonitor_chart = mdx_lib.make_chart_df(
                type="area",
                df=self.healthcheck[
                    ["clustermonitor_up", "clustermonitor_down"]
                ],
                chart_options={
                    "title": "Cluster Monitor health over time",
                    "yAxisTickFormat": {
                        "label": "Status clustermonitor",
                    },
                },
                dataset_options={
                    "clustermonitor_up": {
                        "color": "green",
                        "label": "Clustermonitor Up",
                    },
                    "clustermonitor_down": {
                        "color": "red",
                        "label": "Clustermonitor Down",
                    },
                },
            )
            ctx["clustermonitor_chart"] = clustermonitor_chart

            if are_nodes_missing_agents := (
                len(self.nodes_missing_agents) > 0
            ):
                nodes_taints = self.nodes_missing_agents[
                    ["name", "taints"]
                ].explode("taints")

                # Filter out nodes without taints
                nodes_taints = nodes_taints[~nodes_taints["taints"].isna()]
                if len(nodes_taints) > 0:
                    taints_norm = pd.json_normalize(nodes_taints["taints"])
                    grid_table = (
                        nodes_taints.drop(columns="taints")
                        .reset_index()
                        .join(taints_norm)
                        .fillna("")[["name", "key", "value", "effect"]]
                    )
                    ctx["nodes_missing_agents_grid"] = mdx_lib.make_grid_df(
                        grid_table, blank_repeated=True
                    )

            if ctx["missing_tol_nano"]:
                columns = [
                    {"title": "Effect", "field": "effect"},
                    {"title": "Key", "field": "key"},
                    {"title": "Value", "field": "value"},
                ]
                data = ctx["missing_tol_nano"]
                ctx["missing_tol_nano_grid"] = mdx_lib.make_grid(columns, data)

            if ctx["missing_tol_cm"]:
                columns = [
                    {"title": "Effect", "field": "effect"},
                    {"title": "Key", "field": "key"},
                    {"title": "Value", "field": "value"},
                ]
                data = ctx["missing_tol_cm"]
                ctx["missing_tol_nano_grid"] = mdx_lib.make_grid(columns, data)

            if len(self.df_flags) > 0:
                ctx["opsflags_count"] = len(self.df_flags)
                self.df_flags["Time"] = pd.to_datetime(
                    self.df_flags["time"], unit="s"
                ).dt.strftime("%Y-%m-%d %H:%M:%S")
                self.df_flags["type"] = (
                    self.df_flags["schema"].str.split(":").str[1]
                )
                self.df_flags.rename(
                    columns={"linkback": "link"}, inplace=True
                )

                stats = (
                    self.df_flags.groupby("severity")["type"]
                    .value_counts()
                    .unstack()
                    .fillna(0)
                    .transpose()
                    .reset_index()
                )
                ctx["opsflags_stats_grid"] = mdx_lib.make_grid_df(stats)

                ctx["opsflags_list_grid"] = mdx_lib.make_grid_df(
                    self.df_flags[
                        self.df_flags["severity"].isin(["critical", "high"])
                    ][:100][
                        ["Time", "type", "description", "severity", "link"]
                    ],
                    blank_repeated=True,
                )

        return self.render(ctx, fmt, rid)


def get_node_taints(nodes: pd.DataFrame) -> set[Tuple]:
    taint_series = nodes.taints.apply(lambda x: set([to_tuple(t) for t in x]))
    taints = reduce(set.union, taint_series, set())
    return taints


def check_tolerations(
    node_taints: set[Tuple], k8s_resource: pd.DataFrame
) -> list:
    if not node_taints:
        return []
    tolerations = {
        to_tuple(taint) for taint in k8s_resource["tolerations"].iloc[0]
    }

    missing_tolerations = [
        to_dict(taint) for taint in node_taints - tolerations
    ]
    return missing_tolerations


def get_friendly_metrics(metrics: dict) -> Sequence[dict]:
    rv = [
        {
            "name": "Number of nodes",
            "value": metrics["nr_nodes"],
        },
        {
            "name": "Number of namespaces",
            "value": metrics["nr_namespaces"],
        },
        {
            "name": "Number of pods",
            "value": metrics["nr_pods"],
        },
        {
            "name": "Number of deployments",
            "value": metrics["nr_deployments"],
        },
        {
            "name": "Number of daemonsets",
            "value": metrics["nr_daemonsets"],
        },
        {
            "name": "Number of services",
            "value": metrics["nr_services"],
        },
    ]
    return rv


def get_node_summary(node_records: list) -> dict | Sequence[dict]:
    summary = {}
    for prop in [
        "instance_type",
        "cores",
        "arch",
        "osImage",
        "containerRuntime",
    ]:
        summary[prop] = dict(Counter([node[prop] for node in node_records]))

    return summary


def friendly_node_summary(summary: dict) -> dict | Sequence[dict]:
    friendly = {
        "instance_type": "Instance Type",
        "cores": "Nr of cores",
        "arch": "Hardware Arch",
        "osImage": "OS",
        "containerRuntime": "Container Runtime",
    }
    md_summary = []
    for prop in friendly.keys():
        for i, key in enumerate(summary[prop]):
            md_summary.append(
                {
                    "name": friendly[prop] if i == 0 else "",
                    "value": key,
                    "prop_count": summary[prop][key],
                }
            )
    return md_summary


def get_node_headroom(node_usage: dict) -> dict | Sequence[dict]:
    rv = {"pods": [], "cpu": [], "memory": []}
    for metric in ["pods", "cpu", "memory"]:
        for node in node_usage.values():
            if node["headroom"][metric] < 0:
                rv[metric].append(
                    {
                        "name": node["name"],
                        "instance_type": node["instance_type"],
                        "cores": node["cores"],
                        f"capacity_{metric}": node["capacity"][metric],
                        f"usage_{metric}": node["usage"][metric],
                        f"headroom_{metric}": node["headroom"][metric],
                    }
                )
    return rv


def get_node_usage(index: dict, schema_index: dict) -> dict[str, dict]:
    index_schema = schema_index
    node_usage = defaultdict(dict)
    nodes = index_schema[s_node].values()
    pods = index_schema[s_pod].values()
    for node in nodes:

        node_usage[node["metadata"]["name"]] = {
            "name": node["metadata"]["name"],
            "arch": node["k8s_status"]["nodeInfo"]["architecture"],
            "osImage": node["k8s_status"]["nodeInfo"]["osImage"],
            "containerRuntime": node["k8s_status"]["nodeInfo"][
                "containerRuntimeVersion"
            ],
            "instance_type": node["metadata"]["labels"].get(
                "node.kubernetes.io/instance-type", "unknown"
            ),
            "cores": int(node["k8s_status"]["capacity"]["cpu"]),
            "capacity": {
                "pods": int(node["k8s_status"]["capacity"]["pods"]),
                "memory": convert_unit(
                    node["k8s_status"]["capacity"]["memory"]
                ),
                "cpu": convert_unit(node["k8s_status"]["capacity"]["cpu"]),
            },
            "usage": {"pods": 0, "memory": 0, "cpu": 0},
            "headroom": {"pods": 0, "memory": 0, "cpu": 0},
            "taints": node["spec"].get("taints", []),
            "control_plane": node["metadata"]["labels"].get(
                "node-role.kubernetes.io/controlplane", False
            ),
        }

    for pod in pods:
        node_name = pod["spec"].get("nodeName")
        if node_name:
            node_usage[node_name]["usage"]["pods"] += 1
            for container in pod["spec"]["containers"]:
                if "resources" not in container:
                    continue
                if "requests" not in container["resources"]:
                    continue
                node_usage[node_name]["usage"]["memory"] += convert_unit(
                    container["resources"]["requests"].get("memory", 0)
                )
                node_usage[node_name]["usage"]["cpu"] += convert_unit(
                    container["resources"]["requests"].get("cpu", 0)
                )

    for node in node_usage.values():
        for metric in ["pods", "memory", "cpu"]:
            node["headroom"][metric] = (
                node["capacity"][metric] - node["usage"][metric]
            )
    return node_usage


def convert_unit(amount: str) -> float:
    if type(amount) is int:
        return amount
    stripped = amount.strip()
    if stripped.endswith("Ki"):
        return int(stripped[:-2]) * 1024
    if stripped.endswith("Mi"):
        return int(stripped[:-2]) * 1024 * 1024
    if stripped.endswith("Gi"):
        return int(stripped[:-2]) * 1024 * 1024 * 1024
    if stripped.endswith("Ti"):
        return int(stripped[:-2]) * 1024 * 1024 * 1024 * 1024
    if stripped.endswith("Pi"):
        return int(stripped[:-2]) * 1024 * 1024 * 1024 * 1024 * 1024
    if stripped.endswith("Ei"):
        return int(stripped[:-2]) * 1024 * 1024 * 1024 * 1024 * 1024 * 1024
    if stripped.endswith("K"):
        return int(stripped[:-1]) * 1000
    if stripped.endswith("M"):
        return int(stripped[:-1]) * 1000 * 1000
    if stripped.endswith("G"):
        return int(stripped[:-1]) * 1000 * 1000 * 1000
    if stripped.endswith("T"):
        return int(stripped[:-1]) * 1000 * 1000 * 1000 * 1000
    if stripped.endswith("P"):
        return int(stripped[:-1]) * 1000 * 1000 * 1000 * 1000 * 1000
    if stripped.endswith("E"):
        return int(stripped[:-1]) * 1000 * 1000 * 1000 * 1000 * 1000 * 1000
    if stripped.endswith("m"):
        return int(stripped[:-1]) / 1000
    return int(stripped)


def get_cont_health(status: dict) -> dict:
    return {
        "container_id": (
            status["containerID"].split("://")[-1]
            if "containerID" in status
            else "not present"
        ),
        "ready": status.get("ready", False),
        "started": status.get("started", False),
    }


def get_pod_health(rec: dict) -> bool:
    status = rec["k8s_status"]
    phase = status.get("phase")
    cont_status = status.get("containerStatuses", [])

    cont_health = [get_cont_health(status) for status in cont_status]
    healthy = rec["status"] == "closed" or (
        phase == "Running"
        and all([ch["ready"] and ch["started"] for ch in cont_health])
    )
    return healthy


def to_tuple(d: dict) -> tuple:
    return tuple(sorted(d.items()))


def to_dict(t: tuple) -> dict:
    return dict(t)


def get_agent_health(index: dict, schema_index: dict) -> dict:

    rv: dict = {"nano_agent": {}, "cluster_monitor": {}}
    nodes = schema_index[s_node].values()
    nano_agent_ds = [
        ds
        for ds in schema_index[s_daemonset].values()
        if "nanoagent" in ds["metadata"]["name"]
    ]
    nano_agents = [
        pod
        for pod in schema_index[s_pod].values()
        if "nanoagent" in pod["metadata"]["name"]
    ]

    unhealthy_agents = [
        agent for agent in nano_agents if not get_pod_health(agent)
    ]

    nodes_missing_agents = [
        node
        for node in nodes
        if node["metadata"]["name"]
        not in [agent["spec"].get("nodeName") for agent in nano_agents]
    ]
    nano_healthy = (
        len(unhealthy_agents) == 0 and len(nodes_missing_agents) == 0
    )

    rv["nano_agent"]["healthy"] = nano_healthy
    rv["nano_agent"]["unhealthy_agents"] = [
        {
            "name": n["metadata"]["name"],
            "status": n["k8s_status"]["phase"],
            "node": n["spec"].get("nodeName", "not assigned to a node"),
        }
        for n in unhealthy_agents
    ]
    rv["nano_agent"]["nodes_not_running"] = [
        {"name": n["metadata"]["name"], "taints": n["spec"].get("taints", [])}
        for n in nodes_missing_agents
    ]

    node_taints = set()
    for node in nodes:
        for taint in node["spec"].get("taints", []):
            node_taints.add(to_tuple(taint))
    nano_tolerations = set()
    for ds in nano_agent_ds:
        for taint in (
            ds["spec"]
            .get("template", {})
            .get("spec", {})
            .get("tolerations", [])
        ):
            nano_tolerations.add(to_tuple(taint))

    nano_missing_tolerations = [
        to_dict(taint) for taint in node_taints - nano_tolerations
    ]
    rv["nano_agent"]["missing_tolerations"] = nano_missing_tolerations

    cluster_monitor = [
        pod
        for pod in schema_index[s_pod].values()
        if "clustermonitor" in pod["metadata"]["name"]
    ]
    monitor_healthy = len(cluster_monitor) == 1 and get_pod_health(
        cluster_monitor[0]
    )
    rv["cluster_monitor"]["healthy"] = monitor_healthy

    cluster_monitor_dep = [
        dep
        for dep in schema_index[s_deployment].values()
        if "clustermonitor" in dep["metadata"]["name"]
    ]
    cm_tolerations = set()
    for dep in cluster_monitor_dep:
        for taint in (
            dep["spec"]
            .get("template", {})
            .get("spec", {})
            .get("tolerations", [])
        ):
            cm_tolerations.add(to_tuple(taint))

    cm_missing_tolerations = [
        to_dict(taint) for taint in node_taints - nano_tolerations
    ]
    rv["cluster_monitor"]["missing_tolerations"] = cm_missing_tolerations
    return rv
