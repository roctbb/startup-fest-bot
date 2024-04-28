from .alchemy import *


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text, nullable=True)
    link = db.Column(db.String(256), nullable=True)

    comments = db.relationship('Comment', backref=backref('project', uselist=False), lazy=False)
    investments = db.relationship('Transaction', backref=backref('project', uselist=False), lazy=False)

    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
