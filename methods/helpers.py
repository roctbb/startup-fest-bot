from models import db
from config import *
from manage import app

def transaction(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            db.session.commit()
            return result
        except Exception as e:
            raise e

    wrapper.__name__ = func.__name__
    return wrapper


def find_user(func):
    def wrapper(message):
        from .users import find_user_by_telegram_id
        try:
            with app.app_context():
                user = find_user_by_telegram_id(message.from_user.id)
                result = func(message, user)
                return result
        except Exception as e:
            raise e


    wrapper.__name__ = func.__name__
    return wrapper
