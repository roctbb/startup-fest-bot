from flask import Blueprint
from objects.basic_auth import *

users_blueprint = Blueprint('users', __name__, template_folder='users')

@auth.login_required
@users_blueprint.route('/', methods=['GET'])
def user_list():
    pass

@auth.login_required
@users_blueprint.route('/add', methods=['GET'])
def add_user_page():
    pass

@auth.login_required
@users_blueprint.route('/add', methods=['POST'])
def add_user():
    pass
