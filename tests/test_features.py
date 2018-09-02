import pytest
import json


def _data(data):
    return json.loads(data)

def test_exclude_option_in_list_view(features_app):
    r = features_app.get("/api/users")
    rd = _data(r.data)

    assert r.status_code == 200
    assert rd['len'] == 1

    for data in rd['data']:
        assert 'secret' not in data.keys()

def test_exclude_option_in_list_view_with_fields(features_app):
    r = features_app.get("/api/users?fields=secret, age, name")
    rd = _data(r.data)

    assert r.status_code == 200
    assert rd['len'] == 1
    for data in rd['data']:
        assert 'secret' not in data.keys()

def test_exclude_option_in_single_view(features_app):
    r = features_app.get("/api/users/1")
    rd = _data(r.data)

    assert r.status_code == 200
    assert rd['len'] == 3 # Only 2 attributes
    assert 'secret' not in rd['data'].keys()
