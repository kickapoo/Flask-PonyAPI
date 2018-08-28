import pytest
import os
import json


def _data(data):
    return json.loads(data)

@pytest.fixture
def app():
    # Example app
    from flask import Flask
    from flask_ponyapi import PonyAPI

    from pony.orm import db_session
    from pony.orm import Database, Required, Optional

    app = Flask(__name__)
    db = Database()

    class PersonDefault(db.Entity):
        name = Required(str)
        age = Optional(int)

    class Person(db.Entity):
        name = Required(str)
        age = Optional(int)

        class Meta:
            route_base = 'persons'
            route_prefix = '/api'

    db.bind(provider='sqlite', filename='test-database.sqlite', create_db=True)
    db.generate_mapping(create_tables=True)

    with db_session:
        p1 = Person(name='John',  age=20)
        p2 = Person(name="fda", age=123)
        p3 = PersonDefault(name="j2", age=123)


    api = PonyAPI(app, db)

    yield app.test_client()

    os.remove("test-database.sqlite")


@pytest.mark.parametrize("url, len",[
    ('/persondefault', 1),
    ('/api/persons', 2)
])
def test_list_view(app, url, len):
    r = app.get(url)
    rd = _data(r.data)
    print(rd)
    assert r.status_code == 200
    assert rd['len'] == len


@pytest.mark.parametrize("url",[
    '/persondefault/1',
    '/api/persons/1',
])
def test_get_view(app, url):
    r = app.get(url)
    assert r.status_code == 200


@pytest.mark.parametrize("url,len",[
    ('/persondefault', 2),
    ('/api/persons', 3)
])
def test_post_view(app, url, len):
    post_data = {
        'name': 'Person',
        'age': 21
    }
    r = app.post(url, data=json.dumps(post_data))
    rd = _data(r.data)
    assert r.status_code == 201
    r = app.get(url)
    rd = _data(r.data)
    assert rd['len'] == len

@pytest.mark.parametrize("url",[
    '/persondefault/1',
    '/api/persons/1',
])
def test_put_view(app, url):
    post_data = {
        'name': 'Person1',
        'age': 2
    }
    r = app.put(url, data=json.dumps(post_data))
    assert r.status_code == 204

@pytest.mark.parametrize("url,len",[
    ('/persondefault/1',0),
    ('/api/persons/1',1)
])
def test_delete_view(app, url, len):
    r = app.delete(url)
    assert r.status_code == 204
    r = app.get(url[:-2])
    rd = _data(r.data)
    assert rd['len'] == len
