from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Message(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    uuidString = db.Column(db.String(40), unique=True, nullable=False)
    date = db.Column(db.DateTime(), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=False, nullable=False)
    text = db.Column(db.String(120), unique=False, nullable=False)
