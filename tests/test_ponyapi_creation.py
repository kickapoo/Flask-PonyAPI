import pytest
from flask_ponyapi.exceptions import *

def test_ponyapi_creation_not_list_of_entities():
    from flask import Flask
    from flask_ponyapi import PonyAPI
    app = Flask(__name__)

    entities = ('a', 'b')
    with pytest.raises(EntitiesNotInAList):
        PonyAPI(app, entities)
