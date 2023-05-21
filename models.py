from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
import secrets 

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader 
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable=True, default='')
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String, nullable=True, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, default='', unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow )

    def __init__(self, email, first_name='', last_name='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name 
        self.last_name = last_name 
        self.password = self.set_password(password)
        self.email = email 
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)
    
    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f'{self.email} has been added!'
    
class Car(db.Model):
    id = db.Column(db.String, primary_key=True)
    car_name = db.Column(db.String(150), nullable=False)
    car_model = db.Column(db.String(100), nullable=False)
    car_make = db.Column(db.String(100), nullable=False)
    car_year = db.Column(db.String(4), nullable=False)
    car_color = db.Column(db.String(50), nullable=False)
    car_token = db.Column(db.String, db.ForeignKey('user.token'), unique=True)

    def __init__(self, car_name, car_model, car_make, car_year, car_color, car_token, id=''):
        self.id = self.set_id()
        self.car_name = car_name 
        self.car_model = car_model 
        self.car_make = car_make 
        self.car_year = car_year 
        self.car_color = car_color
        self.car_token = car_token 

    def __repr__(self):
        return f'The following cars have been added to the Inventory: {self.car_name}'
    
    def set_id(self):
        return (secrets.token_urlsafe())
    
class CarSchema(ma.Schema):
    class Meta: 
        fields = ['id', 'car_name', 'car_make', 'car_model', 'car_year', 'car_color']

car_schema = CarSchema()
cars_schema = CarSchema(many=True)



    