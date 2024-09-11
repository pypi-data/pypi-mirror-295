import json
import os

import pytest

from app.reports.report import Report
from app.reports.report_engine import ReportEngine
from app.reports.report_lib import ReportInput

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")
ORG = os.getenv("ORG")
DO_INTEGRATED_TESTS = os.getenv("DO_INTEGRATED_TESTS") is not None


@pytest.fixture()
def engine():
    yield ReportEngine(
        {"backend": {"kind": "simple_file", "dir": "/tmp/reports"}}
    )


def report(filename: str):
    import os

    cwd = os.getcwd()
    fname = (
        filename
        if filename.startswith("/") or filename.startswith("./")
        else cwd + f"/app/reports/portfolio/tests/testdata/{filename}"
    )
    with open(fname) as f:
        report_input = json.load(f)
        report_input["org_uid"] = ORG
        ri = ReportInput.model_validate(report_input)
        rep = Report(input=ri, formats=["json", "yaml", "md", "html", "pdf"])
        return rep


async def test_report_agent_metrics(engine):
    if not API_KEY or not API_URL or not ORG:
        pytest.skip("Skipping test without API_KEY, API_URL, ORG")
    if not DO_INTEGRATED_TESTS:
        pytest.skip("Skipping integration test")

    ri = report("spec_agent_metrics.json")

    reports = await engine.make_reports(ri, API_KEY, API_URL)
    for fmt, path in reports.items():
        assert path.exists()
        if fmt != "pdf":
            assert path.read_text() != ""
            if fmt not in ["json", "yaml"]:
                assert "Nano agent usage report" in path.read_text()


def test_ops_get_data():
    if not API_KEY or not API_URL or not ORG:
        pytest.skip("Skipping test without API_KEY, API_URL, ORG")
    if not DO_INTEGRATED_TESTS:
        pytest.skip("Skipping integration test")

    import app.reports.portfolio.ops_v2 as ops

    end = 1724040000

    # Get 1st day of data
    st = end - 3600 * 48
    et = end - 3600 * 24
    rep = ops.OpsReporter(spec={})
    models1 = list(
        rep.get_raw_data(
            st=st,
            et=et,
            cluid="clus:cqP418TptGU",
            org_uid="spyderbatuid",
            api_key=API_KEY,
            api_url=API_URL,
            what="models",
        )
    )
    assert len(models1) > 0

    flags1 = list(
        rep.get_raw_data(
            st=st,
            et=et,
            cluid="clus:cqP418TptGU",
            org_uid="spyderbatuid",
            api_key=API_KEY,
            api_url=API_URL,
            what="opsflags",
        )
    )
    assert len(flags1) > 0


    # Get 2nd day of data
    st = et
    et = st + 3600 * 24
    models2 = list(
        rep.get_raw_data(
            st=st,
            et=et,
            cluid="clus:cqP418TptGU",
            org_uid="spyderbatuid",
            api_key=API_KEY,
            api_url=API_URL,
            what="models",
        )
    )
    assert len(models2) > 0

    flags2 = list(
        rep.get_raw_data(
            st=st,
            et=et,
            cluid="clus:cqP418TptGU",
            org_uid="spyderbatuid",
            api_key=API_KEY,
            api_url=API_URL,
            what="opsflags",
        )
    )
    assert len(flags2) > 0

    model1_versions = set([(m["id"], m["version"]) for m in models1])
    model2_versions = set([(m["id"], m["version"]) for m in models2])
    assert model1_versions.intersection(model2_versions) == set()

    flag1_versions = set([(f["id"], f["version"]) for f in flags1])
    flag2_versions = set([(f["id"], f["version"]) for f in flags2])
    assert flag1_versions.intersection(flag2_versions) == set()


def test_collect_and_process():
    if not API_KEY or not API_URL or not ORG:
        pytest.skip("Skipping test without API_KEY, API_URL, ORG")
    if not DO_INTEGRATED_TESTS:
        pytest.skip("Skipping integration test")

    import app.reports.portfolio.ops_v2 as ops

    et = 1724084181   # Mon Aug 19 12:16:21 EDT 2024
    st = et - 3600 * 7*24

    rep = ops.OpsReporter(spec={})
    rep.collect_and_process(
        args = {
            "st": st,
            "et": et,
            "cluid": "clus:cqP418TptGU"
        },
        org_uid="spyderbatuid",
        api_key=API_KEY,
        api_url=API_URL
    )
    assert len(rep.df) > 0


async def test_report_ops(engine):
    if not API_KEY or not API_URL or not ORG:
        pytest.skip("Skipping test without API_KEY, API_URL, ORG")
    if not DO_INTEGRATED_TESTS:
        pytest.skip("Skipping integration test")

    ri = report("spec_ops.json")

    reports = await engine.make_reports(ri, API_KEY, API_URL)
    for fmt, path in reports.items():
        assert path.exists()
        if fmt != "pdf":
            assert path.read_text() != ""
            if fmt not in ["json", "yaml"]:
                assert "Operational report" in path.read_text()


def test_project_for_table():
    pytest.skip("Skipping test for now")
    import app.reports.portfolio.cluster_profile as cp

    data = [
        {"id": "2", "l1": {"l2": 1}},
        {"id": "1", "l1": {"l2": 2}},
        {"id": "2", "l1": {"l2": 2}},
        {"id": "1", "l1": {"l2": 1}},
    ]
    assert cp.project_for_table(data, ["id", "l1.l2"]) == [
        {"id": "1", "l1.l2": 1},
        {"id": "", "l1.l2": 2},
        {"id": "2", "l1.l2": 1},
        {"id": "", "l1.l2": 2},
    ]


def test_prep_tables():
    pytest.skip("Skipping test for now")
    import app.reports.portfolio.cluster_profile as cp

    ds = {
        "daemonsets": {
            "daemonset:mupQ8S67xUo:Zd3zgg:5Dgpl7ajHK": {
                "kind": "DaemonSet",
                "metadata": {
                    "name": "test1",
                    "namespace": "default",
                },
            },
            "daemonset:mupQ8S67xUo:Zd3zgg:qVMI7OQLsd": {
                "kind": "DaemonSet",
                "metadata": {
                    "name": "test2",
                    "namespace": "default",
                },
            },
            "daemonset:mupQ8S67xUo:Zd3zgg:qVMI7OQabc": {
                "kind": "DaemonSet",
                "metadata": {
                    "name": "testa",
                    "namespace": "kuuber",
                },
            },
            "daemonset:mupQ8S67xUo:Zd3zgg:qVMI7OQdef": {
                "kind": "DaemonSet",
                "metadata": {
                    "name": "testb",
                    "namespace": "kuuber",
                },
            },
        }
    }
    result = cp.prep_tables(ds)
    assert result is not None


def test_cluster_profile_local(engine):
    pytest.skip("Skipping test with local data for now")
    ri = report("spec_cluster_profile_local.json")
    reports = engine.make_reports(ri, API_KEY, API_URL)
    for fmt, path in reports.items():
        assert path.exists()
        if fmt != "pdf":
            rep = path.read_text()
            assert rep != ""
            if fmt not in ["json", "yaml"]:
                assert "Cluster Profile report" in rep

        # move the file path to sample dir
        path.rename(
            f"app/reports/portfolio/samples/test-{ri.input.report_id}.{fmt}"
        )


def test_cluster_profile_api(engine):
    pytest.skip("Skipping test for cluster profile report for now")
    if not API_KEY or not API_URL or not ORG:
        pytest.skip("Skipping test without API_KEY, API_URL, ORG")
    if not DO_INTEGRATED_TESTS:
        pytest.skip("Skipping integration test")

    ri = report("spec_cluster_profile_api.json")
    reports = engine.make_reports(ri, API_KEY, API_URL)
    for fmt, path in reports.items():
        assert path.exists()
        if fmt != "pdf":
            rep = path.read_text()
            assert rep != ""
            if fmt not in ["json", "yaml"]:
                assert "Cluster Profile report" in rep


async def test_report_linux_usage(engine):
    if not API_KEY or not API_URL or not ORG:
        pytest.skip("Skipping test without API_KEY, API_URL, ORG")
    if not DO_INTEGRATED_TESTS:
        pytest.skip("Skipping integration test")

    ri = report("spec_linux_usage.json")

    reports = await engine.make_reports(ri, API_KEY, API_URL)
    for fmt, path in reports.items():
        assert path.exists()
        if fmt != "pdf":
            assert path.read_text() != ""
            if fmt not in ["json", "yaml"]:
                assert "Linux usage report" in path.read_text()


if __name__ == "__main__":
    import sys

    API_KEY = sys.argv[2]
    API_URL = sys.argv[3]
    rep = report(sys.argv[1])
    engine = ReportEngine(
        {"backend": {"kind": "simple_file", "dir": "/tmp/reports"}}
    )
    reports = engine.make_reports(rep, API_KEY, API_URL)
    print(reports)
