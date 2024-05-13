from flask import Blueprint, render_template, request, redirect
from methods.users import *
from methods.transactions import *
from objects.basic_auth import *

payments_blueprint = Blueprint('payments', __name__)


@payments_blueprint.route('/', methods=['GET'])
@auth.login_required
def start_payment():
    return render_template('payments/payment.html')


@payments_blueprint.route('/payment', methods=['POST'])
@auth.login_required
def make_payment():
    try:
        user = find_user_by_payment_code(request.form.get('payment_code'))
    except:
        return redirect('/payments/not_found')

    try:
        make_transaction(user, -1 * int(request.form.get('amount')), request.form.get('currency'), 'Покупка в магазине')
    except Exception as e:
        print(e)
        return redirect('/payments/insufficient_funds')

    return redirect('/payments/success')


@payments_blueprint.route('/success', methods=['GET'])
@auth.login_required
def payment_successful():
    return render_template('payments/success.html')


@payments_blueprint.route('/insufficient_funds', methods=['GET'])
@auth.login_required
def insufficient_funds():
    return render_template('payments/error.html', error='Недостаточно средств для проведения платежа.')


@payments_blueprint.route('/not_found', methods=['GET'])
@auth.login_required
def not_found():
    return render_template('payments/error.html', error='Пользователь не найден.')
