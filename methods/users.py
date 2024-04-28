from models import *
from objects.exceptions import *
from .helpers import transaction
import uuid


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

    payment_code = str(uuid.uuid4())
    registration_code = str(uuid.uuid4())

    user = User(name=name, role=role, payment_code=payment_code, registration_code=registration_code)
    db.session.add(user)
    return user
