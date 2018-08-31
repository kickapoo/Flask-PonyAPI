"""
    Flask-PonyAPI
    -------------

    API creation for Pony ORM Entities with no effort.
    :copyright: (c) 2018 by Stavros Anastasiadis.
    :license: BSD, see LICENSE for more details.
"""
from pony.orm.core import Entity

from .manager import RestEntity
from .exceptions import EntitiesNotInAList, NotPonyEntitySubClass

__version__ = '0.0.3'



class PonyAPI():
    """API Constructor for Database Entities
    """

    def __init__(self, app, entities):

        if not isinstance(entities, list):
            raise EntitiesNotInAList

        for entity in entities:
            RestEntity(app, entity)
