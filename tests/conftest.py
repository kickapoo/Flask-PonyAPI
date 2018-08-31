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
        p1 = Person(name='John',  age=20)
        p2 = Person(name="fda", age=123)
        p3 = PersonDefault(name="j2", age=123)

    # List of Entities
    # entities = [v for k, v in db.entities.items()]
    # or
    entities = [PersonDefault, Person]
    api = PonyAPI(app, entities)

    yield app.test_client()

    os.remove("tests/test-database.sqlite")
