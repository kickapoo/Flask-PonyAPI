import os
import pytest

from flask import Flask
from flask_ponyapi import PonyAPI

from pony.orm import db_session, Database
from pony.orm import Required, Optional

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _app():
    app = Flask(__name__)
    db = Database()
    return app, db

def _bind_generate_db(db):
    db.bind(provider='sqlite', filename='test-database.sqlite', create_db=True)
    db.generate_mapping(create_tables=True)
    return

@pytest.fixture
def basic_app():
    app, db = _app()

    class PersonDefault(db.Entity):
        name = Required(str)
        age = Optional(int)

    class Person(db.Entity):
        name = Required(str)
        age = Optional(int)

        class Meta:
            route_base = 'persons'
            route_prefix = '/api'

    _bind_generate_db(db)

    with db_session:
        p1 = Person(name="Doctor Aphra",  age=20)
        p2 = Person(name="Faro Argyus", age=21)
        p3 = PersonDefault(name="Shara Bey", age=34)

    api = PonyAPI(app, db)

    yield app.test_client()

    os.remove("tests/test-database.sqlite")


@pytest.fixture
def features_app():
    app, db = _app()

    class User(db.Entity):
        name = Required(str)
        age = Optional(int)
        secret = Optional(str)

        class Meta:
            route_base = 'users'
            route_prefix = '/api'
            exclude = ['secret']

    _bind_generate_db(db)

    with db_session:
        u1 = User(name="Douglas Quaid",  age=32, secret='Hauser')

    api = PonyAPI(app, db)

    yield app.test_client()

    os.remove("tests/test-database.sqlite")
