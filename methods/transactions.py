from .helpers import *
from models import *
from config import CURRENCIES
from objects.exceptions import *


@transaction
def make_transaction(user, amount, currency, description=None):
    if currency not in CURRENCIES:
        raise InvalidCurrency
    if user.balance(currency) + amount < 0:
        raise InsufficientFunds

    db.session.add(Transaction(user_id=user.id, amount=amount, currency=currency, description=description))
