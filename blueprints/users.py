from flask import Blueprint, render_template, redirect, request
from methods.users import *
from objects.basic_auth import *

users_blueprint = Blueprint('users', __name__)


@auth.login_required
@users_blueprint.route('/', methods=['GET'])
def list():
    return render_template('users/list.html', users=as_dict(get_all_users()))

@auth.login_required
@users_blueprint.route('/<id>', methods=['GET'])
def details(id):
    user = find_user_by_id(id)
    return render_template('users/details.html', user=user.as_dict())

@auth.login_required
@users_blueprint.route('/pay/<id>', methods=['GET'])
def add_funds_page(id):
    user = find_user_by_id(id)
    return render_template('users/add_funds.html', user=user.as_dict())

@auth.login_required
@users_blueprint.route('/pay/<id>', methods=['POST'])
def add_funds(id):
    user = find_user_by_id(id)
    amount = request.form.get('amount', 0)
    make_transaction(user, int(amount), "PCS", "Ручное начисление")
    return redirect(f'/users/{user.id}')

@auth.login_required
@users_blueprint.route('/add', methods=['GET'])
def add_page():
    return render_template('/users/add.html')


@auth.login_required
@users_blueprint.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    role = request.form.get('role')

    try:
        user = make_user(name, role)
        return redirect(f'/users/{user.id}')
    except Exception as e:
        return render_template('/users/add.html', role=role, name=name, error="Заполните все поля.")
