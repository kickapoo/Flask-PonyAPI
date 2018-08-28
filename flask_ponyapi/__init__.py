"""
    Flask-PonyAPI
    -------------

    API creation for Pony ORM Entities with no effort.
    :copyright: (c) 2018 by Stavros Anastasiadis.
    :license: BSD, see LICENSE for more details.
"""
from .manager import RestEntity


__version__ = '0.0.3'


class PonyAPI():
    """API Constructor for Database Entities
    """

    def __init__(self, app, db):
        # TODO
        for k, v in db.entities.items():
            RestEntity(app, v)
