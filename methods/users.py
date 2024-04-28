from models import *
from objects.exceptions import *


def find_user_by_id(id):
    return User.query.filter_by(id=id).first()


def find_user_by_payment_code(code):
    user = User.query.filter_by(payment_code=code).first()

    if not user:
        raise NotFound

    return user


def find_user_by_registration_code(code):
    user = User.query.filter_by(registration_code=code).first()

    if not user:
        raise NotFound

    return user
