from flask import Blueprint, request, jsonify, render_template 
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema
import secrets

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    car_name = request.json['car_name']
    car_model = request.json['car_model']
    car_make = request.json['car_make']
    car_year = request.json['car_year']
    car_color = request.json['car_color']
    car_token = current_user_token.token
    print(car_token)

    print(f'BIG TESTER: {current_user_token.token}')

    car = Car(car_name, car_model, car_make, car_year, car_color, car_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars', methods = ['GET'])
@token_required
def get_car(current_user_token):
    a_user = current_user_token.token
    cars = Car.query.filter_by(car_token=a_user).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_single_car(current_user_token, id):
    car = Car.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)
    car.car_name = request.json['car_name']
    car.car_year = request.json['car_year']
    car.car_make = request.json['car_make']
    car.car_model = request.json['car_model']
    car.car_color = request.json['car_color']
    car.car_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

