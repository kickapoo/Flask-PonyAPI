"""
    Flask-PonyAPI
    -------------

    API creation for Pony ORM Entities with no effort.
    :copyright: (c) 2018 by Stavros Anastasiadis.
    :license: BSD, see LICENSE for more details.
"""
from pony.orm import Database

from .manager import RestEntity
from .exceptions import NotPonyDatabase

__version__ = '0.0.5'


class PonyAPI():
    """API Constructor for Database Entities
    """

    def __init__(self, app, db, auth=False):
        # TODO: missing .init_app()

        if not isinstance(db, Database):
            raise NotPonyDatabase

        for k, entity in db.entities.items():
            RestEntity(app, entity)
