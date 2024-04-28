from .alchemy import *
from .relation_tables import *


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(256), nullable=False)
    code = db.Column(db.String(256), nullable=False)

    projects = db.relationship('Project', secondary=project_user, backref='users')
    transactions = db.relationship('Transaction', backref=backref('user', uselist=False), lazy=True)

    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def balance(self, currency):
        return sum(filter(lambda t: t.currency == currency, map(lambda t: t.amount, self.transactions)))

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.text,
            "balance": {
                "PC": self.balance("PC"),
                "SPC": self.balance("SPC"),
                "EPC": self.balance("EPC")
            }
        }
