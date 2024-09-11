import app.reports.report_lib as rlib
import json


def test_exists_at_time():
    model = {"valid_from": 1, "valid_to": 2}
    assert rlib.exists_at_time(model, 1)
    assert rlib.exists_at_time(model, 1.5)
    assert rlib.exists_at_time(model, 2)
    assert not rlib.exists_at_time(model, 0.5)
    assert not rlib.exists_at_time(model, 2.1)
    model = {"valid_from": 1}
    assert rlib.exists_at_time(model, 1)
    assert rlib.exists_at_time(model, 1.5)
    assert not rlib.exists_at_time(model, 0.5)


def test_exists_in_window():
    model = {"valid_from": 1, "valid_to": 2}
    assert rlib.exists_in_window(model, 1, 2)
    assert rlib.exists_in_window(model, 1, 1.5)
    assert rlib.exists_in_window(model, 1.5, 2)
    assert rlib.exists_in_window(model, 0.5, 1.5)
    assert rlib.exists_in_window(model, 0.5, 1)
    assert not rlib.exists_in_window(model, 0.5, 0.9)
    assert not rlib.exists_in_window(model, 2.1, 5)
    model = {"valid_from": 1}
    assert rlib.exists_in_window(model, 0.5, 1.5)
    assert rlib.exists_in_window(model, 1, 5)
    assert rlib.exists_in_window(model, 5, 10)
    assert not rlib.exists_in_window(model, 0.5, 0.9)


def test_slice_and_project():
    d1 = {
        "id": 1,
        "time": 1,
        "valid_from": 1,
        "valid_to": 1.8,
        "a": 4,
        "b": 2,
        "c1": {"c2": 3},
    }
    d2 = {
        "id": 2,
        "time": 2,
        "valid_from": 2,
        "valid_to": 3,
        "a": 4,
        "b": 5,
        "c1": {"c2": 6},
    }
    d3 = {"id": 3, "time": 3, "valid_from": 3, "a": 7, "b": 8, "c1": {"c2": 9}}
    last_models = {1: d1, 2: d2, 3: d3}

    sorted_data = [d1, d2, d3]
    def filter_and_project(x):
        if x["a"] != 4:
            return None
        else:
            return {"a": x["a"], "b": x["b"], "c1.c2": x["c1"]["c2"]}

    expected = [{"a": 4, "b": 2, "c1.c2": 3, "time_slice": 1.5}]
    rv = rlib.slice_and_project(last_models, 1.5, 1.9, filter_and_project)
    assert rv == expected


def test_make_slice_projections():
    def filter_and_project(model):
        if model["kind"] != "Pod":
            return None
        return {
            "id": model["id"],
            "kind": model["kind"],
            "schema": model["schema"],
            "metadata.namespace": model["metadata"]["namespace"],
            "metadata.name": model["metadata"]["name"],
            "status": model["status"],
            "time": model["time"],
            "valid_from": model["valid_from"],
            "valid_to": model.get("valid_to"),
            "status": model["status"],
        }


    data = []
    with open("app/reports/testdata/intc3-small.json", "r") as f:
        for line in f:
            data.append(json.loads(line))
    slices = rlib.make_slice_projections(
        data_sorted=sorted(data, key=lambda x: x["time"]),
        start=1722277442,
        end=1722277605,
        delta=10,
        filter_and_project=filter_and_project
    )
    valid_from = data[0]["valid_from"]
    valid_to = data[0]["valid_to"]
    assert len(slices) > 0
    slices_dict = {}
    for s in slices:
        slices_dict.setdefault(s["time_slice"], [])
        slices_dict[s["time_slice"]].append(s)
    for t, slice in slices_dict.items():
        t_start = t
        t_end = t + 10
        if t_end < valid_from:
            assert len(slice) == 0
        if t_end >= valid_from and t_end <= valid_to:
            assert len(slice) == 1
            assert slice[0]["id"] == data[0]["id"]
            assert slice[0]["status"] == "active"
        if t_end >= valid_from and t_start <= valid_to and t_end > valid_to:
            assert len(slice) == 1
            assert slice[0]["id"] == data[0]["id"]
            assert slice[0]["status"] == "closed"
        if t_start >= valid_from and t_start > valid_to and t_end > valid_to:
            assert len(slice) == 0
