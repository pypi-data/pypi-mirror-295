import asyncio
import os
import time

import aioboto3
import pytest
from moto.server import ThreadedMotoServer

import app.reports.storage.s3_backend as s3_b
from app.reports.report import Report, ReportListResult
from app.reports.report_engine import ReportEngine
from app.reports.report_lib import ReportInput, ReportListInput

file_contents = "test file contents"


@pytest.fixture
def sample_file(tmp_path):
    file_path = tmp_path / "sample_file.txt"
    file_path.write_text(file_contents)

    return file_path


@pytest.fixture()
async def mock_boto(monkeypatch):
    server = ThreadedMotoServer(port=0)
    server.start()
    port = server._server.socket.getsockname()[1]  # type: ignore
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
def s3_backend(engine):
    yield engine.backend


@pytest.fixture
def report():
    r_input = ReportInput(
        org_uid="test",
        report_id="test",
        report_args={"test": "test"},
    )
    report = Report(input=r_input, formats=["md"])
    yield report


@pytest.mark.asyncio
async def test_register_report(s3_backend, report):
    await s3_backend.register_report(report)


@pytest.mark.asyncio
async def test_get_report(s3_backend, report):
    await s3_backend.register_report(report)
    retrieved = await s3_backend.get_report(report.id, report.input.org_uid)
    assert retrieved is not None
    assert retrieved.id == report.id
    assert retrieved.input == report.input
    assert retrieved.status == report.status
    assert retrieved.change_log == report.change_log
    assert retrieved.formats == report.formats


@pytest.mark.asyncio
async def test_get_report_not_existing(s3_backend):
    try:
        retrieved = await s3_backend.get_report("not_existing", "test")
    except Exception as e:
        assert isinstance(e, KeyError)
    else:
        assert False, "get_report did not raise exception"


@pytest.mark.asyncio
async def test_update_report(s3_backend, report):
    await s3_backend.register_report(report)
    report.status = "published"
    await s3_backend.update_report(report)
    retrieved = await s3_backend.get_report(report.id, report.input.org_uid)
    assert retrieved is not None
    assert retrieved.id == report.id
    assert retrieved.input == report.input
    assert retrieved.status == report.status
    assert retrieved.change_log == report.change_log


@pytest.mark.asyncio
async def test_publish_report_file(s3_backend, report, sample_file):
    await s3_backend.publish_report_file(report, "md", sample_file)


@pytest.mark.asyncio
async def test_download_report_file(s3_backend, report, sample_file):
    await s3_backend.publish_report_file(report, "md", sample_file)

    contents = []
    async for chunk in s3_backend.download_report_file(
        report.id, report.input.org_uid, "md"
    ):
        contents.append(chunk)
    assert b"".join(contents) == file_contents.encode()


@pytest.mark.asyncio
async def test_download_report_file_not_existing(s3_backend):
    try:
        async for chunk in s3_backend.download_report_file(
            "not_existing", "test", "md"
        ):
            pass
    except Exception as e:
        assert isinstance(e, KeyError)
    else:
        assert False, "download_report_file did not raise exception"


@pytest.mark.asyncio
async def test_delete_report(s3_backend, report, sample_file):
    await s3_backend.register_report(report)
    await s3_backend.publish_report_file(report, "md", sample_file)
    await s3_backend.delete_report(report.id, report.input.org_uid)
    await s3_backend.delete_report_file(report.id, report.input.org_uid, "md")

    try:
        report = await s3_backend.get_report(report.id, report.input.org_uid)
    except Exception as e:
        assert isinstance(e, KeyError)
    else:
        assert False, "get_report did not raise exception"

    try:
        async for chunk in s3_backend.download_report_file(
            "not_existing", "test", "md"
        ):
            pass
    except Exception as e:
        assert isinstance(e, KeyError)
    else:
        assert False, "download_report_file did not raise exception"


@pytest.mark.asyncio
async def test_list_reports(s3_backend, report):
    for i in range(5):
        report.id = f"test_{i}"
        await s3_backend.register_report(report)
    retrieved = await s3_backend.list_reports("test")
    assert len(retrieved) >= 5
    assert isinstance(retrieved[0], Report)


@pytest.mark.asyncio
async def test_list_reports_v2(s3_backend, report):
    rep_in = []
    s3_b.REPORTLIST_PAGE_SIZE = 5
    for i in range(2 * s3_b.REPORTLIST_PAGE_SIZE + 3):
        r_input = ReportInput(
            org_uid="testlist2",
            report_id="test",
            report_args={"test": "test"},
        )
        test_rep = Report(input=r_input, formats=["md"])
        test_rep.id = f"test_{i}"
        await s3_backend.register_report(test_rep)
        rep_in.append(test_rep)

    rep_out = []
    rv = await s3_backend.list_reports_v2("testlist2", ReportListInput())
    reports = rv.reports
    assert len(reports) == s3_b.REPORTLIST_PAGE_SIZE
    assert all(isinstance(r, Report) for r in reports)
    assert rv.continuation_token is not None
    rep_out.extend(reports)

    rv = await s3_backend.list_reports_v2(
        "testlist2", ReportListInput(continuation_token=rv.continuation_token)
    )
    reports = rv.reports
    assert len(reports) == s3_b.REPORTLIST_PAGE_SIZE
    assert all(isinstance(r, Report) for r in reports)
    assert rv.continuation_token is not None
    rep_out.extend(reports)

    rv = await s3_backend.list_reports_v2(
        "testlist2", ReportListInput(continuation_token=rv.continuation_token)
    )
    reports = rv.reports
    assert len(reports) == 3
    assert all(isinstance(r, Report) for r in reports)
    assert rv.continuation_token is None
    rep_out.extend(reports)

    assert len(rep_out) == len(rep_in)
    assert {r.id for r in rep_out} == {r.id for r in rep_in}
