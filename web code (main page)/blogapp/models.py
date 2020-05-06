from datetime import datetime
from blogapp import db


class Customer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	pets = db.relationship('Pet', backref='customer', lazy='dynamic')

	def __repr__(self):
		return '<User {}>'.format(self.username)


class Employee(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	key = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))

	def __repr__(self):
		return '<Employee {}>'.format(self.username)


class Pet(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True)
	type = db.Column(db.String(64), index=True)
	old = db.Column(db.Integer, index=True)
	gender = db.Column(db.String(64), index=True)
	customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
	standards = db.relationship('StandardAppointment', backref='pet', lazy='dynamic')
	emergencies = db.relationship('EmergencyAppointment', backref='pet', lazy='dynamic')

	def __repr__(self):
		return '<Pet {}>'.format(self.name)


class StandardAppointment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, index=True, default=datetime.utcnow())
	slot = db.Column(db.String(64), index=True)
	city = db.Column(db.String(64), index=True)
	details = db.Column(db.String(120), index=True)
	pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'))


class EmergencyAppointment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, index=True, default=datetime.utcnow())
	arrive = db.Column(db.Integer, index=True)
	city = db.Column(db.String(64), index=True)
	details = db.Column(db.String(120), index=True)
	pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'))


