from flask import Flask
from pony.orm import Database, Required, Optional, db_session

from flask_ponyapi import PonyAPI

app = Flask(__name__)
db = Database()

class Person(db.Entity):
    name = Required(str)
    age = Optional(int)

    class Meta:
        route_base = 'persons'
        route_prefix = '/api'

api = PonyAPI(app, db)

if __name__ == '__main__':
    db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
    db.generate_mapping(create_tables=True)
    with db_session:
        p1 = Person(name='Almec',  age=99)
        p2 = Person(name="Amee", age=100)
    app.run(debug=True)
