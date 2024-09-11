from collections import Counter, defaultdict
from datetime import datetime
from itertools import chain
from pathlib import Path
from typing import Optional, Sequence, Tuple, Iterable, Any

import spyctl.config.configs as cfg
import spyctl.resources.api_filters as _af
import spyctl.api.athena_search as search_api

from app.reports.reporter import Reporter

"""
# TODO
# 1. Test out on larger clusters
# 2. Parallellize data collection and support first getting all ids across queries, then getting objects
# 3. Project only fields required to lower memory usage
# 4. Consider how to handle changes compared to earlier reports
# 5. Show no tables if empty but show message that no data is available
# 6. See if we can add search links to table numbers
# 7. Reduce down to connections by deployment and/or service for incoming traffic

Content scope
north-south traffic

inside-out - to where - by dns- by ip
Top 15 destinations ip blocks (in general)
Top 15 destinations
- by country
- by asn name
- by server dns name
- cloud name

(diffs)
New destinations not seen last time (country/asn/server dns/cloud name)

Top talkers
- by kubernetes owner (kind/namespace/name)
- by client process name
(what changed - new/removed OR big increase/decrease by connection count)

outside-in
coming in - to where
coming in - from where

Specific ports - top client/servers by traffic


coming in - to where - by dns, by ip
          - from where - by dns, by ip

east-west traffic
which services is a deployment talking to (hubble chart) and the nr of connections
create a dot file for graphviz (hubble cilium)
coming in - to where

(diagrams)

External API usage (outbound)
"""

s_cluster = "model_k8s_cluster"
# s_node = "model_k8s_node"
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
s_connbundle = "model_bundled_connection"

report_schemas = [
    s_cluster,
    # s_node,
    s_daemonset,
    s_deployment,
    s_cronjob,
    s_pod,
    s_service,
    s_namespace,
    s_container,
    s_connbundle,
]


def make_index(rec_list: list, schemas: list[str], time_slices: list[Tuple[float]]=[]) -> Tuple[dict, dict]:
    index = dict()
    schema_index: dict = defaultdict(dict)
    for rec in rec_list:
        for schema in schemas:
            if schema in rec["schema"]:
                index[rec["id"]] = rec
                schema_index[schema][rec["id"]] = rec
            if "metadata" in rec and "namespace" in rec["metadata"]:
                schema_index[s_namespace][rec["metadata"]["namespace"]] = {
                    "id": rec["metadata"]["namespace"],
                    "metadata": {"name": rec["metadata"]["namespace"]},
                }
    return index, schema_index


class ProfileReporter(Reporter):
    def collector(
        self,
        args: dict[str, str | float | int | bool],
        org_uid: str,
        api_key: str,
        api_url: str,
    ) -> list:

        all_the_things = []
        cluid = args["cluid"]

        print("getting cluster")
        cluster = search_api.search_athena(
            api_url,
            api_key,
            org_uid,
            schema=s_cluster,
            query=f'id="{cluid}"',
            start_time=int(args["st"]),
            end_time=int(args["et"]),
            use_pbar=False,
        )
        all_the_things.extend(cluster)

        # nodes = search_api.search_athena(
        #     api_url, api_key, org_uid,
        #     schema="model_k8s_node",
        #     query=f'cluster_uid="{cluid}"'
        # )
        # all_the_things.extend(nodes)

        # namespaces = search_api.search_athena(
        #     api_url, api_key, org_uid,
        #     schema="model_k8s_namespace",
        #     query=f'cluster_uid="{cluid}"'
        # )
        # all_the_things.extend(namespaces)

        print("getting daemonsets")
        daemonsets = search_api.search_athena(
            api_url,
            api_key,
            org_uid,
            schema="model_k8s_daemonset",
            query=f'cluster_uid="{cluid}"',
            start_time=int(args["st"]),
            end_time=int(args["et"]),
            use_pbar=False,
        )
        all_the_things.extend(daemonsets)

        print("getting deployments")
        deployments = search_api.search_athena(
            api_url,
            api_key,
            org_uid,
            schema="model_k8s_deployment",
            query=f'cluster_uid="{cluid}"',
            start_time=int(args["st"]),
            end_time=int(args["et"]),
            use_pbar=False,
        )
        all_the_things.extend(deployments)

        print("getting statefulsets")
        statefulsets = search_api.search_athena(
            api_url,
            api_key,
            org_uid,
            schema="model_k8s_statefulset",
            query=f'cluster_uid="{cluid}"',
            start_time=int(args["st"]),
            end_time=int(args["et"]),
            use_pbar=False,
        )
        all_the_things.extend(statefulsets)

        print("getting cronjobs")
        cronjobs = search_api.search_athena(
            api_url,
            api_key,
            org_uid,
            schema="model_k8s_cronjob",
            query=f'cluster_uid="{cluid}"',
            start_time=int(args["st"]),
            end_time=int(args["et"]),
            use_pbar=False,
        )
        all_the_things.extend(cronjobs)

        print("getting jobs")
        jobs = search_api.search_athena(
            api_url,
            api_key,
            org_uid,
            schema="model_k8s_job",
            query=f'cluster_uid="{cluid}"',
            start_time=int(args["st"]),
            end_time=int(args["et"]),
            use_pbar=False,
        )
        all_the_things.extend(jobs)

        print("getting services")
        services = search_api.search_athena(
            api_url,
            api_key,
            org_uid,
            schema="model_k8s_service",
            query=f'cluster_uid="{cluid}"',
            start_time=int(args["st"]),
            end_time=int(args["et"]),
            use_pbar=False,
        )
        all_the_things.extend(services)

        print("getting pods")
        pods = search_api.search_athena(
            api_url,
            api_key,
            org_uid,
            schema="model_k8s_pod",
            query=f'cluster_uid="{cluid}"',
            start_time=int(args["st"]),
            end_time=int(args["et"]),
            use_pbar=False,
        )
        all_the_things.extend(pods)

        print("getting containers")
        containers = search_api.search_athena(
            api_url,
            api_key,
            org_uid,
            schema="model_container",
            query=f'cluster_uid="{cluid}"',
            start_time=int(args["st"]),
            end_time=int(args["et"]),
            use_pbar=False,
        )
        all_the_things.extend(containers)

        print("getting cbundles - server")
        cbundles_server = search_api.search_athena(
            api_url,
            api_key,
            org_uid,
            schema="model_bundled_connection",
            query=f'server_cluster_uid="{cluid}"',
            start_time=int(args["st"]),
            end_time=int(args["et"]),
            use_pbar=False,
        )
        all_the_things.extend(cbundles_server)

        print("getting cbundles - client")
        cbundles_client = search_api.search_athena(
            api_url,
            api_key,
            org_uid,
            schema="model_bundled_connection",
            query=f'server_cluster_uid="{cluid}"',
            start_time=int(args["st"]),
            end_time=int(args["et"]),
            use_pbar=False,
        )
        all_the_things.extend(cbundles_client)

        return all_the_things


    def processor(
        self,
        data: list,
        args: dict[str, str | float | int | bool],
    ) -> dict:
        if not data:
            return {"error": {"message": "No data available"}}
        context: dict = {}
        index, schema_index = make_index(rec_list=data, schemas=report_schemas)

        # Cluster name and id
        cluster = list(schema_index[s_cluster].values())[0]
        context["cluster"] = {
            "name": cluster["name"],
            "cluid": cluster["id"],
        }

        # Reporting period
        context["st"] = datetime.fromtimestamp(int(args["st"])).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        context["et"] = datetime.fromtimestamp(int(args["et"])).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        context["namespaces"] = sorted(
            [
                ns["metadata"]["name"]
                for ns in schema_index[s_namespace].values()
            ]
        )
        context["daemonsets"] = schema_index.get(s_daemonset, {})
        context["deployments"] = schema_index.get(s_deployment, {})
        context["statefulsets"] = schema_index.get(s_statefulset, {})
        context["cronjobs"] = schema_index.get(s_cronjob, {})
        context["services"] = schema_index.get(s_service, {})
        # context["jobs"] = get_by_namespace(s_job, schema_index)
        context["images"] = analyze_images(schema_index)
        context["connections"] = analyze_connections(
            schema_index, cluster["id"]
        )
        return context

    def renderer(
        self,
        context: dict,
        format: str,
        rid: str,
    ) -> Path:

        rv = context
        if format in ["json", "yaml"]:
            rv = {}
            for key, value in context.items():
                if key in [
                    "daemonsets",
                    "deployments",
                    "statefulsets",
                    "cronjobs",
                    "jobs",
                    "services",
                ]:
                    value = organize_by_namespace(value)
                rv[key] = value

        if format in ["md", "html"]:
            rv = prep_tables(context)

        return self.render(rv, format, rid)

def prep_tables(context: dict) -> dict:
    new_context = dict()
    for key, value in context.items():
        if key in [
            "daemonsets",
            "deployments",
            "statefulsets",
            "cronjobs",
            "jobs",
            "services",
        ]:
            value = project_for_table(
                value.values(), ["metadata.namespace", "metadata.name"]
            )

        if key == "images":
            new_images = dict()
            new_images["repos_all"] = value["repos_all"]
            new_images["all"] = value["all"]
            by_ns = [
                {
                    "namespace": ns,
                    "image": c[0],
                    "count": c[1],
                }
                for ns, counts in value["by_ns"].items()
                for c in counts
            ]
            new_images["by_ns"] = project_for_table(
                by_ns, ["namespace", "image", "count"], sort=False
            )
            repos_by_ns = [
                {
                    "namespace": ns,
                    "repo": c[0],
                    "count": c[1],
                }
                for ns, counts in value["repos_by_ns"].items()
                for c in counts
            ]
            new_images["repos_by_ns"] = project_for_table(
                repos_by_ns, ["namespace", "repo", "count"], sort=False
            )
            value = new_images

        new_context[key] = value
    return new_context



def project_for_table(
    l: list[dict], projection: Iterable, sort: bool = True
) -> list[dict]:

    rv = []
    prev = {k: None for k in projection}
    iterate = (
        sorted(l, key=lambda d: [get_val(d, k) for k in projection])
        if sort
        else l
    )
    for d in iterate:
        df = {}
        different = False
        for k in projection:
            if get_val(d, k) == get_val(prev, k) and not different:
                df[k] = ""
            else:
                df[k] = get_val(d, k)
                different = True
        if any(df.values()):
            rv.append(df)
        prev = d
    return rv


def get_val(d: dict, k: str) -> Optional[Any]:
    keys = k.split(".")
    for key in keys:
        d = d.get(key)
        if d is None:
            return None
    return d


def set_val(d: dict, k: str, v: Any) -> None:
    keys = k.split(".")
    for key in keys[:-1]:
        d = d.setdefault(key, {})
    d[keys[-1]] = v


def organize_by_namespace(resources: dict) -> dict:

    by_ns: dict[str, list] = defaultdict(list)
    for rec in resources.values():
        ns = rec["metadata"]["namespace"]
        by_ns[ns].append(rec)
    return by_ns


def analyze_images(schema_index: dict) -> dict:
    images_all: Counter = Counter()
    image_repos_all: Counter = Counter()
    images_by_ns: dict[str, Counter] = defaultdict(Counter)
    image_repos_by_ns: dict[str, Counter] = defaultdict(Counter)
    for container in schema_index[s_container].values():
        image = container.get("image")
        namespace = container.get("pod_namespace")
        if image:
            images_all.update([image])
            split = image.split("/")
            repo = split[0] if len(split) > 1 else "public registry"
            image_repos_all.update([repo])
            if namespace:
                images_by_ns[namespace].update([image])
                image_repos_by_ns[namespace].update([repo])
    rv_images_all = sorted(
        images_all.items(), key=lambda x: x[1], reverse=True
    )
    rv_repos_all = sorted(
        image_repos_all.items(), key=lambda x: x[1], reverse=True
    )
    rv_images_by_ns = {
        k: sorted(v.items(), key=lambda x: x[1], reverse=True)
        for k, v in images_by_ns.items()
    }
    rv_repos_by_ns = {
        k: sorted(v.items(), key=lambda x: x[1], reverse=True)
        for k, v in image_repos_by_ns.items()
    }

    return {
        "all": rv_images_all,
        "repos_all": rv_repos_all,
        "by_ns": rv_images_by_ns,
        "repos_by_ns": rv_repos_by_ns,
    }

def friendly_key(key: Tuple) -> str:
    return "_".join(str(item) for item in key)

def counters_to_list(counters: dict, top:int = 0) -> dict:
    rv = {}
    for counter_type, counter in counters.items():
        counter_name = "_".join([str(c) for c in counter_type])
        l = []
        for ck, cv in counter.items():
            r = dict()
            for i, c in enumerate(counter_type):
                r[c] = ck[i]
            r["count"] = cv
            l.append(r)
        rv[counter_name] = {
            "list": l,
            "order": [str(c) for c in counter_type]
        }

    for counter_name, l in rv.items():
        if top > 0:
            rv[counter_name] = sorted(l["list"], key=lambda x: x["count"], reverse=True)[:top]
        else:
            rv[counter_name] = sorted(l["list"], key=lambda x: [x[f] for f in l["order"]])

    return rv

def analyze_connections(schema_index: dict, cluster: str) -> dict:
    connections = schema_index["model_bundled_connection"]
    fields_ew = [(
        "client_pod_namespace",
        "client_pod_owner_name",
        "client_proc_name",
        "server_pod_namespace",
        "server_pod_owner_name",
        "server_dns_name",
        "server_proc_name",
        "server_port")
    ]
    ew = defaultdict(Counter)

    fields_ns_outbound = [
        ("server_asn_name",),
        ("server_asn_country",),
        ("server_cloud_name",),
        ("server_dns_name",),
        ("server_port",)
    ]
    ns_outbound = defaultdict(Counter)

    fields_ns_inbound = [
        ("server_pod_namespace", "server_pod_owner_name", "server_proc_name", "server_port"),
        ("server_proc_name",),
        ("server_dns_name",),
    ]
    ns_inbound = defaultdict(Counter)

    for conn in connections.values():
        enrich_conn(conn, schema_index)
        if (
            conn.get("client_cluster_uid", "") == cluster
            and conn.get("server_cluster_uid", "") == cluster
        ):
            for by_key in fields_ew:
                update_counter(conn, by_key, ew[by_key])
        else:
            if conn.get("client_cluster_uid", "") == cluster:
                # north-south outbound traffic counters
                for by_key in fields_ns_outbound:
                    update_counter(conn, by_key, ns_outbound[by_key])
            else:
                # north-south inbound traffic counters
                for by_key in fields_ns_inbound:
                    update_counter(conn, by_key, ns_inbound[by_key])
    rv = {
        "north_south": {
            "outbound": counters_to_list(ns_outbound, top=10),
            "inbound": counters_to_list(ns_inbound, top=10),
        },
        "east_west": counters_to_list(ew)
    }
    return rv



def friendly_connections(connections: dict) -> dict:
    friendly_connections = {}
    friendly_connections["north_south"] = {
        "outbound": {
            k: v.most_common(10)
            for k, v in connections["north_south"]["outbound"].items()
        },
        "inbound": {
            k: v.most_common(10)
            for k, v in connections["north_south"]["outbound"].items()
        },
    }
    friendly_connections["east_west"] = counters_to_list(connections["east_west"])
    return friendly_connections


def enrich_conn(conn: dict, schema_index: dict):
    if (pod_uid := conn.get("server_pod_uid")) is not None:
        enrich_conn_pod(pod_uid, conn, schema_index, "server")
    if (pod_uid := conn.get("client_pod_uid")) is not None:
        enrich_conn_pod(pod_uid, conn, schema_index, "client")


def enrich_conn_pod(pod_uid: str, conn: dict, schema_index: dict, cl_sv: str):
        pod = schema_index[s_pod].get(pod_uid)
        if pod is not None:
            conn[f"{cl_sv}_pod_name"] = pod["metadata"]["name"]
            conn[f"{cl_sv}_pod_namespace"] = pod["metadata"]["namespace"]
            if (owner_name := pod.get("owner_name")) is not None:
                conn[f"{cl_sv}_pod_owner_name"] = owner_name
            if (deployment_name := pod.get("deployment_name")) is not None:
                conn[f"{cl_sv}_pod_owner_name"] = deployment_name
            if (cronjob_name := pod.get("cronjob_name")) is not None:
                conn[f"{cl_sv}_pod_owner_name"] = cronjob_name




def update_counter(record: dict, by_key: Tuple, counter: Counter) -> None:
    value = tuple(record.get(k, "no value") for k in by_key)
    counter.update({value: record["num_connections"]})



def to_tuple(d: dict) -> tuple:
    return tuple(sorted(d.items()))


def to_dict(t: tuple) -> dict:
    return dict(t)
