#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

# Each view should display all attributes as line items (ul). 
# If there is a one-to-many relationship, each of the many should have its own line item.

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()

    if not animal:
        response_body = "<h1>404 animal not found</h1>"
        response = make_response(response_body, 404)

    print(animal)
    
    response_body = f"""
        <ul>ID: {animal.id}</ul>
        <ul>Name: {animal.name}</ul>
        <ul>Species: {animal.species}</ul>
        <ul>Zookeeper: {animal.zookeeper.name}</ul>
        <ul>Enclosure: {animal.enclosure.environment}</ul>
    """

    response = make_response(response_body, 200)
    
    return response


@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()

    if not zookeeper:
        response_body = "<h1>404 zookeeper not found</h1>"
        response = make_response(response_body, 404)

    # print(zookeeper.animals)

    animal_names = [ animal.name for animal in zookeeper.animals]
    print(animal_names)

    response_animal_name = ""

    if not animal_names:
        response_animal_name += f"Has no animal at this time"
    else:
        for animal_name in animal_names:
            response_animal_name += f"<ul>Animal: {animal_name}</ul>"  

    response_body = f"""
        <ul>ID: {zookeeper.id}</ul>
        <ul>Name: {zookeeper.name}</ul>
        <ul>Birthday: {zookeeper.birthday}</ul>
        <ul>{response_animal_name}</ul>
    """
    
    response = make_response(response_body, 200)
    
    return response


@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    environment = Enclosure.query.filter(Enclosure.id == id).first()

    if not environment:
        response_body = "<h1>404 environment not found</h1>"
        response = make_response(response_body, 404)

    animal_names = [ animal.name for animal in environment.animals]
    print(animal_names)

    response_animal_name = ""

    if not animal_names:
        response_animal_name += f"Has no animal at this time"
    else:
        for animal_name in animal_names:
            response_animal_name += f"<ul>Animal: {animal_name}</ul>"  

    response_body = f"""
        <ul>ID: {environment.id}</ul>
        <ul>Environment: {environment.environment}</ul>
        <ul>Open to Visitors: {environment.open_to_visitors}</ul>
        <ul>{response_animal_name}</ul>
    """

    response = make_response(response_body, 200)

    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
