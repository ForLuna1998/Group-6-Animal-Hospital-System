from datetime import datetime
from blogapp import db


class Customer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	pets = db.relationship('Pet', backref='customer', lazy='dynamic')
	phone = db.Column(db.Integer, index=True)
	firstname = db.Column(db.String(64), index=True)
	lastname = db.Column(db.String(64), index=True)

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
	appointments = db.relationship('Appointment', backref='pet', lazy='dynamic')


	def __repr__(self):
		return '<Pet {}>'.format(self.name)


class Appointment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	type = db.Column(db.String,index=True)
	date = db.Column(db.DateTime, index=True, default=datetime.utcnow())
	time = db.Column(db.String(64), index=True)
	city = db.Column(db.String(64), index=True)
	details = db.Column(db.String(120), index=True)
	pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'))
	start = db.Column(db.DateTime, index=True, default=datetime.utcnow())
	end = db.Column(db.DateTime, index=True, default=datetime.utcnow())
	status = db.Column(db.String(64), index=True, default='appointment submitted')


	def __repr__(self):
		return '<Appointment {}>'.format(self.id)




