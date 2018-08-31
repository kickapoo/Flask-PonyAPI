import pytest
import os
import json


def _data(data):
    return json.loads(data)

@pytest.mark.parametrize("url, len",[
    ('/persondefault', 1),
    ('/api/persons', 2)
])
def test_list_view(basic_app, url, len):
    # Test List view
    r = basic_app.get(url)
    rd = _data(r.data)
    assert r.status_code == 200
    assert rd['len'] == len


@pytest.mark.parametrize("url",[
    '/persondefault/1',
    '/api/persons/1',
])
def test_get_view(basic_app, url):
    r = basic_app.get(url)
    assert r.status_code == 200


@pytest.mark.parametrize("url,len",[
    ('/persondefault', 2),
    ('/api/persons', 3)
])
def test_post_view(basic_app, url, len):
    post_data = {
        'name': 'Person',
        'age': 21
    }
    r = basic_app.post(url, data=json.dumps(post_data))
    rd = _data(r.data)
    assert r.status_code == 201
    r = basic_app.get(url)
    rd = _data(r.data)
    assert rd['len'] == len

@pytest.mark.parametrize("url",[
    '/persondefault/1',
    '/api/persons/1',
])
def test_put_view(basic_app, url):
    post_data = {
        'name': 'Person1',
        'age': 2
    }
    r = basic_app.put(url, data=json.dumps(post_data))
    assert r.status_code == 204

@pytest.mark.parametrize("url,len",[
    ('/persondefault/1',0),
    ('/api/persons/1',1)
])
def test_delete_view(basic_app, url, len):
    r = basic_app.delete(url)
    assert r.status_code == 204
    r = basic_app.get(url[:-2])
    rd = _data(r.data)
    assert rd['len'] == len
