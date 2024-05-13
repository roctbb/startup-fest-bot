from .alchemy import *


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text, nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='CASCADE'), nullable=True)
    session_id = db.Column(db.String(256))
    is_auto = db.Column(db.Boolean, nullable=False, default=False)

    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
