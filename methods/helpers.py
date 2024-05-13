from models import db
from config import *
from manage import app
from objects.telegram_bot import bot


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
                try:
                    user = find_user_by_telegram_id(message.from_user.id)
                except:
                    user = None
                result = func(message, user)
                return result
        except Exception as e:
            raise e

    wrapper.__name__ = func.__name__
    return wrapper


def requires_user(func):
    def wrapper(message):
        from .users import find_user_by_telegram_id
        try:
            with app.app_context():
                user = find_user_by_telegram_id(message.from_user.id)

                if not user:
                    bot.send_message(message.from_user.id, "Перед началом работы необходимо пройти авторизацию.")
                    return
                result = func(message, user)
                return result
        except Exception as e:
            raise e

    wrapper.__name__ = func.__name__
    return wrapper
