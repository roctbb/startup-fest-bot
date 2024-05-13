from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from config import *

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    print("checking")
    if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
        return username
