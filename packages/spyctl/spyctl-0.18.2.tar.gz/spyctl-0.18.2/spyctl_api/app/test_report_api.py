import os

import aioboto3
import pytest
from fastapi.testclient import TestClient
from moto.server import ThreadedMotoServer

from app.reports.report_engine import ReportEngine

from .main import app

formats = ["json", "yaml", "md", "pdf"]


@pytest.fixture
async def mock_boto(monkeypatch):
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
    os.environ["REPORT_BUCKET"] = bucket
    yield bucket


@pytest.fixture
def engine(bucket):
    yield ReportEngine(config={"backend": {"kind": "s3", "bucket": bucket}})


@pytest.fixture
def client(engine):
    yield TestClient(app)


@pytest.fixture
def reportid(client):
    response = client.post(f"/api/v1/org/{ORG}/report", json=report_input)
    id = response.json()["id"]
    yield id


@pytest.fixture
def inventory(client):
    response = client.get(f"/api/v1/org/{ORG}/report/inventory")
    yield response.json()


API_KEY = "TEST_KEY"
API_URL = "TEST_URL"
ORG = "TEST_ORG"
CLUSTER = "TEST_CLUSTER"
report_input = {
    "report_id": "mocktest",
    "api_key": API_KEY,
    "api_url": API_URL,
    "report_args": {
        "cluid": CLUSTER,
        "st": 1711020676,
        "et": 1711035028,
    },
    "report_tags": {"test1": "test1", "test2": 2},
}


def test_get_inventory(inventory):
    assert "inventory" in inventory
    assert len(inventory["inventory"]) > 0
    arg = inventory["inventory"][0]["args"][1]
    assert "required" in arg
    assert "default" in arg


def test_generate_report(client):
    response = client.post("/api/v1/org/{ORG}/report", json=report_input)
    if response.status_code != 200:
        print(f"input was: ", report_input)
        print(f"api response text: ", response.text)
    assert response.status_code == 200
    result = response.json()

    assert result["id"] != ""
    assert result["input"]["report_args"] == report_input["report_args"]
    assert all(
        result["input"]["report_tags"][key] == value
        for key, value in report_input["report_tags"].items()
    )
    assert "time_scheduled" in result["input"]["report_tags"]
    assert result["status"] == "scheduled"
    assert all(fmt in result["formats"] for fmt in formats)


def test_status_report_existing(client, reportid):
    response = client.get(f"/api/v1/org/{ORG}/report/status/{reportid}")
    assert response.status_code == 200
    result = response.json()
    assert result["id"] == reportid
    assert result["status"] == "published"
    assert result["input"]["report_args"] == report_input["report_args"]
    assert all(
        result["input"]["report_tags"][key] == value
        for key, value in report_input["report_tags"].items()
    )
    assert "time_scheduled" in result["input"]["report_tags"]
    assert "time_published" in result["input"]["report_tags"]


def test_status_report_not_existing(client):
    response = client.get(f"/api/v1/org/{ORG}/report/status/nope")
    assert response.status_code == 404


def test_download_report_existing(client, reportid):
    for fmt in formats:
        response = client.get(
            f"/api/v1/org/{ORG}/report/download/{reportid}.{fmt}"
        )
        assert response.status_code == 200
        result = response.text
        assert len(result) > 0
        if fmt != "pdf":
            for key, value in report_input["report_args"].items():
                assert str(key) in result
                assert str(value) in result


def test_download_report_not_existing(client):
    response = client.get((f"/api/v1/org/{ORG}/report/download/nope.json"))
    assert response.status_code == 404


def test_download_sample_report(client, inventory):
    for report_type in inventory["inventory"]:
        response = client.get(
            f"/api/v1/org/{ORG}/report/download/sample-{report_type['id']}.md"
        )
        if response.status_code == 404:
            response = client.get(
                f"/api/v1/org/{ORG}/report/download/sample-{report_type['id']}.mdx"
            )
        assert response.status_code == 200
        result = response.text
        assert len(result) > 0


def test_download_sample_report_not_existing(client):
    response = client.get(f"/api/v1/org/{ORG}/report/download/sample-bogus.md")
    assert response.status_code == 404


def test_delete_report_existing(client, reportid):
    response = client.delete(f"/api/v1/org/{ORG}/report/{reportid}")
    assert response.status_code == 200

    response = client.get(f"/api/v1/org/{ORG}/report/status/{reportid}")
    assert response.status_code == 404


def test_list_reports(client):
    for i in range(5):
        response = client.post(f"/api/v1/org/{ORG}/report", json=report_input)

    response = client.get(f"/api/v1/org/{ORG}/report/")
    assert response.status_code == 200
    result = response.json()["reports"]
    assert len(result) >= 5
    assert "id" in result[0]
    assert "status" in result[0]
    assert "input" in result[0]
    assert result[0]["input"]["report_args"] == report_input["report_args"]
    assert all(
        result[0]["input"]["report_tags"][key] == value
        for key, value in report_input["report_tags"].items()
    )
    assert "time_scheduled" in result[0]["input"]["report_tags"]
    assert "time_published" in result[0]["input"]["report_tags"]


def test_list_reports_v2(client):
    for i in range(5):
        response = client.post(f"/api/v1/org/{ORG}/report", json=report_input)

    response = client.post(f"/api/v1/org/{ORG}/report/")
    assert response.status_code == 200
    assert "continuation_token" not in response.json()
    result = response.json()["reports"]
    assert len(result) >= 5
    assert "id" in result[0]
    assert "status" in result[0]
    assert "input" in result[0]
    assert result[0]["input"]["report_args"] == report_input["report_args"]
    assert all(
        result[0]["input"]["report_tags"][key] == value
        for key, value in report_input["report_tags"].items()
    )
    assert "time_scheduled" in result[0]["input"]["report_tags"]
    assert "time_published" in result[0]["input"]["report_tags"]
