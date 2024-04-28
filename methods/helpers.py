from models import db
from config import *

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

