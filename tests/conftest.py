import os
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print(BASE_DIR)

@pytest.fixture
def basic_app():
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
        p1 = Person(name="Doctor Aphra",  age=20)
        p2 = Person(name="Faro Argyus", age=21)
        p3 = PersonDefault(name="Shara Bey", age=34)

    api = PonyAPI(app, db)

    yield app.test_client()

    os.remove("tests/test-database.sqlite")


@pytest.fixture
def app_with_all_features:
    from flask import Flask
    from flask_ponyapi import PonyAPI

    from pony.orm import db_session
    from pony.orm import Database, Required, Optional

    app = Flask(__name__)
    db = Database()

    class User(db.Entity):
        username = Required(str)
        points = Optional(int)
        secret = Optional(str)

        class Meta:
            route_base = 'users'
            route_prefix = '/api'
            exclude = ['secret']

    db.bind(provider='sqlite', filename='test-database.sqlite', create_db=True)
    db.generate_mapping(create_tables=True)

    with db_session:
        u1 = User(name="Douglas Quaid",  age=32, secret='Hauser')

    api = PonyAPI(app, db)

    yield app.test_client()

    os.remove("tests/test-database.sqlite")
