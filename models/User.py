from .alchemy import *
from .relation_tables import *
from config import CURRENCIES


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(256), nullable=False)
    # student / expert
    role = db.Column(db.String(256), nullable=False)
    payment_code = db.Column(db.String(256), nullable=False)
    registration_code = db.Column(db.String(256), nullable=False)

    projects = db.relationship('Project', secondary=project_user, backref='users')
    transactions = db.relationship('Transaction', backref=backref('user', uselist=False), lazy=True)

    telegram_id = db.Column(db.Integer, nullable=True)

    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def balance(self, currency):
        return sum(filter(lambda t: t.currency == currency, map(lambda t: t.amount, self.transactions)))

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.text,
            "role": self.role,
            "telegram_id": self.telegram_id,
            "balance": {
                currency: self.balance(currency) for currency in CURRENCIES
            }
        }
