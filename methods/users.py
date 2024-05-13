from models import *
from objects.exceptions import *
from methods.transactions import *
from .helpers import transaction
import uuid


def find_user_by_id(id):
    return User.query.filter_by(id=id).first_or_404()


def find_user_by_name(name):
    return User.query.filter_by(name=name).first_or_404()


def find_user_by_telegram_id(id):
    return User.query.filter_by(telegram_id=id).first_or_404()


@transaction
def activate_user(user, telegram_id):
    try:
        another_user = find_user_by_telegram_id(telegram_id)

        if another_user:
            raise Confuse
    except:
        pass

    user.telegram_id = telegram_id
    make_transaction(user, START_MONEY, "PC", "Регистрация пользователя")



def find_user_by_payment_code(code):
    return User.query.filter_by(payment_code=code).first_or_404()

def find_user_by_registration_code(code):
    return User.query.filter_by(registration_code=code).first_or_404()


def get_all_users():
    return User.query.order_by(User.name).get()

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
