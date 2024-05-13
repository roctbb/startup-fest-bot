from flask import Blueprint, render_template, redirect, request
from methods.users import *
from objects.basic_auth import *

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/', methods=['GET'])
@auth.login_required
def list():
    return render_template('users/list.html', users=as_dict(get_all_users()))


@users_blueprint.route('/<id>', methods=['GET'])
@auth.login_required
def details(id):
    user = find_user_by_id(id)
    return render_template('users/details.html', user=user.as_dict())


@users_blueprint.route('/pay/<id>', methods=['GET'])
@auth.login_required
def add_funds_page(id):
    user = find_user_by_id(id)
    return render_template('users/add_funds.html', user=user.as_dict())


@users_blueprint.route('/pay/<id>', methods=['POST'])
@auth.login_required
def add_funds(id):
    user = find_user_by_id(id)
    amount = request.form.get('amount', 0)
    make_transaction(user, int(amount), "PCS", "Ручное начисление")
    return redirect(f'/users/{user.id}')


@users_blueprint.route('/add', methods=['GET'])
@auth.login_required
def add_page():
    return render_template('/users/add.html')


@users_blueprint.route('/add', methods=['POST'])
@auth.login_required
def add():
    name = ' '.join(map(lambda s: s.capitalize(), request.form.get('name', '').split(' ')))
    role = request.form.get('role', '')

    if name and find_user_by_name(name):
        return redirect(f'/users/{find_user_by_name(name).id}')

    try:
        user = make_user(name, role)
        return redirect(f'/users/{user.id}')
    except Exception as e:
        return render_template('/users/add.html', role=role, name=name, error="Заполните все поля.")
