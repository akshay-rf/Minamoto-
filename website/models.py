from . import db
from sqlalchemy.sql import func
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType
from flask_login import UserMixin

class Book(db.Model):
    bid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    author = db.Column(db.String(150))
    category = db.Column(db.String(150))
    tags = db.Column(MutableList.as_mutable(PickleType))
    status = db.Column(db.String(150))
    issuedId = db.Column(db.Integer, db.ForeignKey('user.id'))

class TransactionBorrow(db.Model):
    tid = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    bookId = db.Column(db.Integer, db.ForeignKey('book.bid'))
    time = db.Column(db.DateTime, default=func.now())
    due = db.Column(db.Integer)

class ActiveLoans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    transID = db.Column(db.Integer, db.ForeignKey(TransactionBorrow.tid))

class ExpiredLoans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    transID = db.Column(db.Integer, db.ForeignKey(TransactionBorrow.tid))
    daysPastDue = db.Column(db.Integer)

class TransactionReturn(db.Model):
    tid = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    bookId = db.Column(db.Integer, db.ForeignKey('book.bid'))
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    overDue = db.Column(db.Integer)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    notes = db.relationship('Book')