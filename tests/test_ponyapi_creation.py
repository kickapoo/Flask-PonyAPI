import os
import pytest
from conftest import _app, _bind_generate_db

from flask_ponyapi import PonyAPI
from flask_ponyapi.exceptions import *

from pony.orm import Required


def test_ponyapi_creation_not_list_of_entities():
    app, db = _app()
    db = ('a', 'b')

    with pytest.raises(NotPonyDatabase):
        PonyAPI(app, db)

def test_ponyapi_init_when_routeprefix_options_not_str():
    app, db = _app()

    class User(db.Entity):
        name = Required(str)

        class Meta:
            route_prefix = ('secret',)

    _bind_generate_db(db)

    with pytest.raises(InvalidMetaOption):
        PonyAPI(app, db)
    os.remove("tests/test-database.sqlite")


def test_ponyapi_init_when_baseroute_options_not_str():
    app, db = _app()

    class User(db.Entity):
        name = Required(str)

        class Meta:
            route_base = ('secret', )

    _bind_generate_db(db)

    with pytest.raises(InvalidMetaOption):
        PonyAPI(app, db)
    os.remove("tests/test-database.sqlite")

def test_ponyapi_init_when_exclude_options_not_list():
    app, db = _app()

    class User(db.Entity):
        name = Required(str)

        class Meta:
            exclude = ('secret', )

    _bind_generate_db(db)

    with pytest.raises(InvalidMetaOption):
        PonyAPI(app, db)
    os.remove("tests/test-database.sqlite")
