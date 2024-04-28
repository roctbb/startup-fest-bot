from .helpers import *
from models import *
from config import CURRENCIES
from objects.exceptions import *
from flask import session
import uuid


@transaction
def make_transaction(user, amount, currency, description=None, project_id=None):
    try:
        if "session_id" not in session:
            session['session_id'] = str(uuid.uuid4())
        session_id = session['session_id']
    except:
        session_id = None

    if currency not in CURRENCIES:
        raise InvalidCurrency
    if user.balance(currency) + amount < 0:
        raise InsufficientFunds

    db.session.add(Transaction(user_id=user.id, amount=amount, currency=currency, description=description,
                               session_id=session_id, project_id=project_id))
