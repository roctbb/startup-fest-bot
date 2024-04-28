from models import *
from objects.exceptions import *
from .helpers import transaction


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


def get_all_users():
    return User.query.all()


@transaction
def make_user(name, role):
    if role not in ['student', 'expert']:
        raise InvalidRole
    if not name:
        raise InsufficientData

    user = User(name=name, role=role)
    db.session.add(user)
    return user
