"""Unit test for basic API functionality."""

# pylint: disable=missing-function-docstring, redefined-outer-name

import json
import os

import pytest
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

API_KEY = os.environ.get("API_KEY", "test_key")
API_URL = os.environ.get("API_URL", "https://test.url.local")
ORG = os.environ.get("ORG", "test_org")


def test_create_suppression_policy():
    pytest.skip(
        "Skipping test for now - needs to adjust to move away from elasticsearch"
    )
    data = {
        "type": "trace",
        "name": "Test Suppression Policy",
        "selectors": {
            "trigger-ancestors": ["systemd/foo/bar/baz"],
            "trigger-class": ["this/is/a/test/class"],
            "non-interactive-users": ["root"],
            "interactive_users": ["dev_*", "robert"],
        },
        "org_uid": ORG,
        "api_key": API_KEY,
        "api_url": API_URL,
    }
    print(data)
    response = client.post("/api/v1/create/suppressionpolicy", json=data)
    assert response.status_code == 200


def test_create_guardian_policy(fingerprint_list):
    data = {
        "input_objects": fingerprint_list,
        "name": "Test Policy",
        "mode": "enforce",
        "org_uid": ORG,
        "api_key": API_KEY,
        "api_url": API_URL,
    }
    response = client.post("/api/v1/create/guardianpolicy", json=data)
    assert response.status_code == 200


@pytest.mark.skip(reason="Requires live data, good for local testing only")
def test_create_guardian_policy_from_uid_list(uid_list2):
    data = {
        "input_objects": [uid_list2],
        "name": "Test Policy",
        "mode": "enforce",
        "org_uid": ORG,
        "api_key": API_KEY,
        "api_url": API_URL,
    }
    response = client.post("/api/v1/create/guardianpolicy", json=data)
    assert response.status_code == 200


def test_merge(policy, fingerprint_list):
    data = {
        "object": policy,
        "merge_objects": fingerprint_list,
        "org_uid": ORG,
        "api_key": API_KEY,
        "api_url": API_URL,
    }
    response = client.post("/api/v1/merge", json=data)
    assert response.status_code == 200


def test_diff(policy3, deviations, policy4, deviations2):
    data = {
        "object": policy3,
        "diff_objects": deviations,
        "org_uid": ORG,
        "api_key": API_KEY,
        "api_url": API_URL,
        "full_diff": True,
    }
    response = client.post("/api/v1/diff", json=data)
    data = {
        "object": policy3,
        "diff_objects": deviations,
        "org_uid": ORG,
        "api_key": API_KEY,
        "api_url": API_URL,
        "content_type": "json",
        "include_irrelevant": True,
    }
    response = client.post("/api/v1/diff", json=data)
    assert response.status_code == 200
    data = {
        "object": policy4,
        "diff_objects": deviations2,
        "org_uid": ORG,
        "api_key": API_KEY,
        "api_url": API_URL,
        "content_type": "json",
        "include_irrelevant": True,
    }
    response = client.post("/api/v1/diff", json=data)
    assert response.status_code == 200


def test_validate(policy, policy2):
    data = {"object": policy}
    response = client.post("/api/v1/validate", json=data)
    assert response.status_code == 200
    invalid_message = response.json()["invalid_message"]
    assert not invalid_message
    data = {"object": policy2}
    response = client.post("/api/v1/validate", json=data)
    assert response.status_code == 200
    invalid_message = response.json()["invalid_message"]
    assert not invalid_message


@pytest.mark.skip(reason="Requires live data, good for local testing only")
def test_uid_list(policy5, uid_list):
    data = {
        "org_uid": ORG,
        "api_key": API_KEY,
        "api_url": API_URL,
        "object": policy5,
        "diff_objects": uid_list,
    }
    response = client.post("/api/v1/diff", json=data)
    assert response.status_code == 200


@pytest.fixture
def policy():
    with open("app/testdata/test_policy.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def policy2():
    with open("app/testdata/test_policy2.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def policy3():
    with open("app/testdata/test_policy3.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def policy4():
    with open("app/testdata/test_policy4.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def policy5():
    with open("app/testdata/test_policy5.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def deviations():
    with open("app/testdata/test_deviations.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def deviations2():
    with open("app/testdata/test_deviations2.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def fingerprint_list():
    with open(
        "app/testdata/test_fingerprint_list.json", encoding="utf-8"
    ) as f:
        return json.load(f)


@pytest.fixture
def uid_list():
    with open("app/testdata/test_uid_list.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def uid_list2():
    with open("app/testdata/test_uid_list2.json", encoding="utf-8") as f:
        return json.load(f)
