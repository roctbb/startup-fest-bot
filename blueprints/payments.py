from flask import Blueprint
from objects.basic_auth import *

payments_blueprint = Blueprint('payments', __name__, template_folder='payments')


@auth.login_required
@payments_blueprint.route('/', methods=['GET'])
def start_payment():
    # TODO: отправить страницу начала платежа с вводом суммы и валюты, считыванием QR кода
    pass


@auth.login_required
@payments_blueprint.route('/payment', methods=['POST'])
def make_payment():
    # TODO: получить сумму, валюту, платежный код, вернуть редирект на страницу с текстом результата
    pass


@auth.login_required
@payments_blueprint.route('/success', methods=['GET'])
def payment_successful():
    pass


@auth.login_required
@payments_blueprint.route('/insufficient_funds', methods=['GET'])
def insufficient_funds():
    pass


@auth.login_required
@payments_blueprint.route('/not_found', methods=['GET'])
def not_found():
    pass
