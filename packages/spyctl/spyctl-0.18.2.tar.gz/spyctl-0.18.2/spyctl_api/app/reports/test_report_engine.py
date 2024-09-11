import asyncio
import os

import aioboto3
import pytest

import app.reports.storage.s3_backend as s3_backend
from app.reports.report import Report
from app.reports.report_engine import ReportEngine
from app.reports.report_lib import ReportInput, ReportListInput

file_bytes = b"test file contents"

API_KEY = "not_relevant_for_test"
API_URL = "not_relevant_for_test"
ORG = "test_org"


@pytest.fixture
async def mock_boto(monkeypatch):
    from moto.server import ThreadedMotoServer

    server = ThreadedMotoServer(port=0)
    server.start()
    port = server._server.socket.getsockname()[1]
    os.environ["AWS_ENDPOINT_URL"] = f"http://127.0.0.1:{port}"
    if "AWS_DEFAULT_PROFILE" in os.environ:
        del os.environ["AWS_DEFAULT_PROFILE"]
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "test")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "test")
    yield

    del os.environ["AWS_ENDPOINT_URL"]
    server.stop()


@pytest.fixture
async def bucket(mock_boto):
    bucket = "reports.mock"
    session = aioboto3.Session()
    async with session.client("s3") as s3:
        response = await s3.create_bucket(Bucket=bucket)
    yield bucket


@pytest.fixture
def engine(bucket):
    yield ReportEngine(config={"backend": {"kind": "s3", "bucket": bucket}})


@pytest.fixture
def report():
    r_input = ReportInput(
        report_id="mocktest",
        org_uid=ORG,
        report_args={
            "cluid": "clus:testcluster",
            "st": 1711020676,
            "et": 1711035028,
        },
    )

    report = Report(input=r_input, formats=["json", "yaml", "md", "pdf"])
    yield report


@pytest.mark.asyncio
async def test_generate_report(engine, report):
    await engine.generate_report(report, API_KEY, API_URL)


@pytest.mark.asyncio
async def test_get_report(engine, report):
    await engine.generate_report(report, API_KEY, API_URL)

    retrieved = await engine.get_report(report.id, report.input.org_uid)
    assert retrieved is not None
    assert retrieved.id == report.id
    assert retrieved.input == report.input
    assert retrieved.status == report.status
    assert retrieved.change_log == report.change_log
    assert retrieved.formats == report.formats


@pytest.mark.asyncio
async def test_get_report_not_existing(engine):
    try:
        retrieved = await engine.get_report("not_existing", "test")
    except Exception as e:
        assert isinstance(e, KeyError)


@pytest.mark.asyncio
async def test_download_report(engine, report):
    await engine.generate_report(report, API_KEY, API_URL)
    for fmt in report.formats:
        chunks = []
        async for chunk in engine.download_report(
            report.id, report.input.org_uid, fmt
        ):
            chunks.append(chunk)
        assert len(chunks) > 0, f"no content for {fmt}"
        if fmt in ["md", "json", "yaml"]:
            result = b"".join(chunks).decode()
            for key, value in report.input.report_args.items():
                assert str(key) in result
                assert str(value) in result


@pytest.mark.asyncio
async def test_download_report_file_not_existing(engine, report):
    try:
        for fmt in report.formats:
            chunks = []
            async for chunk in engine.download_report(
                "i don't exist", report.input.org_uid, fmt
            ):
                pass
    except Exception as e:
        assert isinstance(e, KeyError)


@pytest.mark.asyncio
async def test_delete_report(engine, report):
    await engine.generate_report(report, API_KEY, API_URL)

    for fmt in report.formats:
        chunks = []
        async for chunk in engine.download_report(
            report.id, report.input.org_uid, fmt
        ):
            chunks.append(chunk)
        assert len(chunks) > 0, f"no content for {fmt}"

    await engine.delete_report(report.id, report.input.org_uid)

    try:
        await engine.get_report(report.id, report.input.org_uid)
    except Exception as e:
        assert isinstance(e, KeyError)
    else:
        assert False, "get_report did not raise exception"

    try:
        for fmt in report.formats:
            async for chunk in engine.download_report(
                report.id, report.input.org_uid, fmt
            ):
                pass
    except Exception as e:
        assert isinstance(e, KeyError)
    else:
        assert False, "download_report did not raise exception"


@pytest.mark.asyncio
async def test_list_reports(engine, report):
    for i in range(5):
        report.id = f"test_{i}"
        await engine.generate_report(report, API_KEY, API_URL)

    retrieved = await engine.list_reports(report.input.org_uid)
    assert len(retrieved) >= 5
    assert all([isinstance(rep, Report) for rep in retrieved])


@pytest.mark.asyncio
async def test_list_reports_v2(engine, report):
    register = []
    rep_out = []
    s3_backend.REPORTLIST_PAGE_SIZE = 5
    for i in range(s3_backend.REPORTLIST_PAGE_SIZE + 3):
        report = Report(
            input=ReportInput(
                org_uid="test",
                report_id="mocktest",
                report_args={"test": "test"},
            ),
            formats=["md"],
        )
        report.id = f"test_{i}"
        register.append(report)

    await asyncio.gather(
        *[engine.generate_report(r, API_KEY, API_URL) for r in register]
    )

    rv = await engine.list_reports_v2("test", ReportListInput())
    reports = rv.reports
    assert len(reports) == s3_backend.REPORTLIST_PAGE_SIZE
    assert all(isinstance(r, Report) for r in reports)
    assert rv.continuation_token is not None
    ct = rv.continuation_token
    rep_out.extend(reports)

    rv = await engine.list_reports_v2(
        "test", ReportListInput(continuation_token=ct)
    )
    reports = rv.reports
    assert len(reports) == 3
    assert all(isinstance(r, Report) for r in reports)
    assert rv.continuation_token is None
    rep_out.extend(reports)

    assert len(rep_out) == s3_backend.REPORTLIST_PAGE_SIZE + 3
    assert {r.id for r in rep_out} == {r.id for r in register}
