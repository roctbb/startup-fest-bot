from .helpers import *
from models import *
from config import CURRENCIES
from objects.exceptions import *
from flask import session
from bot import bot
import uuid


def send_telegram_notification(user, text, image=None):
    if user.telegram_id:
        try:
            bot.send_message(chat_id=user.telegram_id, text=text)
            if image:
                bot.send_photo(chat_id=user.telegram_id, photo=image)
        except Exception as e:
            print(e)


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

    transaction = Transaction(user_id=user.id, amount=amount, currency=currency, description=description,
                              session_id=session_id, project_id=project_id)
    db.session.add(transaction)

    send_telegram_notification(user,
                               f"🏧 Новая операция: {transaction.amount} {transaction.currency} ({transaction.description})")
