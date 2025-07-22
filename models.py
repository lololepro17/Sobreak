from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    date_of_birth = db.Column(db.Date)
    weight = db.Column(db.Float)
    gender = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    drinks = db.relationship('UserDrink', backref='user', cascade="all, delete-orphan")
    alcohol_levels = db.relationship('AlcoholLevel', backref='user', cascade="all, delete-orphan")
    scores = db.relationship('Score', backref='user', cascade="all, delete-orphan")

class Drink(db.Model):
    __tablename__ = 'drinks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    alcohol_percentage = db.Column(db.Float, nullable=False)
    volume_ml = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))
    image_url = db.Column(db.String(255))
    user_drinks = db.relationship('UserDrink', backref='drink', cascade="all, delete-orphan")

class UserDrink(db.Model):
    __tablename__ = 'userdrinks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    drink_id = db.Column(db.Integer, db.ForeignKey('drinks.id', ondelete='CASCADE'))
    quantity = db.Column(db.Integer)
    consumed_at = db.Column(db.DateTime, default=datetime.utcnow)
    custom_drink_name = db.Column(db.String(80))
    notes = db.Column(db.Text)

class AlcoholLevel(db.Model):
    __tablename__ = 'alcohollevels'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    calculated_at = db.Column(db.DateTime, default=datetime.utcnow)
    estimated_bac = db.Column(db.Float)
    note = db.Column(db.Text)

class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    scores = db.relationship('Score', backref='game', cascade="all, delete-orphan")

class Score(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    game_id = db.Column(db.Integer, db.ForeignKey('games.id', ondelete='CASCADE'))
    score = db.Column(db.Integer)
    played_at = db.Column(db.DateTime, default=datetime.utcnow) 