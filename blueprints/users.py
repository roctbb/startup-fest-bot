from flask import Blueprint, render_template, redirect, request
from methods.users import *
from objects.basic_auth import *

users_blueprint = Blueprint('users', __name__)


@auth.login_required
@users_blueprint.route('/', methods=['GET'])
def user_list():
    return render_template('users/list.html', users=get_all_users())


@auth.login_required
@users_blueprint.route('/add', methods=['GET'])
def add_user_page():
    return render_template('/users/add.html')


@auth.login_required
@users_blueprint.route('/add', methods=['POST'])
def add_user():
    name = request.form.get('name')
    role = request.form.get('role')

    try:
        user = make_user(name, role)
        return redirect(f'/{user.id}')
    except:
        return render_template('/users/add.html', role=role, name=name, error="Заполните все поля.")
