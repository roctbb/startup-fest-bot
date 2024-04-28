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
    comments = db.relationship('Comment', backref=backref('user', uselist=False), lazy=True)

    telegram_id = db.Column(db.Integer, nullable=True)

    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def balance(self, currency):
        print(self.transactions)
        return sum(map(lambda t: t.amount, filter(lambda t: t.currency == currency, self.transactions)))

    def investments(self):
        transactions = list(filter(lambda t: t.project_id, self.transactions))

        investments = {}
        for transaction in transactions:
            if transaction.project_id not in investments:
                investments[transaction.project_id] = {
                    "amount": -1 * transaction.amount,
                    "comment": "",
                    "title": transaction.project.name,
                    "id": transaction.project_id
                }
            else:
                investments[transaction.project_id]['amount'] -= transaction.amount

        for comment in self.comments:
            if comment.project_id in investments:
                investments[comment.project_id]['comment'] = comment.text

        return list(investments.values())

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "telegram_id": self.telegram_id,
            "registration_code": self.registration_code,
            "balance": {
                currency: self.balance(currency) for currency in CURRENCIES
            },
            "investments": self.investments()
        }
