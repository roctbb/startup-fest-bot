import os
from dotenv import load_dotenv

load_dotenv()

CURRENCIES = ['PC', 'PCE', 'PCS']

DB_HOST = os.environ.get('DB_HOST')
DB_DATABASE = os.environ.get('DB_DATABASE')
DB_PORT = os.environ.get('DB_PORT')
DB_LOGIN = os.environ.get('DB_LOGIN')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
APP_SECRET = os.environ.get('APP_SECRET')

HOST = "0.0.0.0"
PORT = 1561

START_MONEY = 100000

DEBUG = bool(os.environ.get('DEBUG'))

ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'editor')
ADMIN_PASSWORD_HASH = os.environ.get('ADMIN_PASSWORD_HASH',
                                     'pbkdf2:sha256:600000$0R5mehSek6l3xXgW$c5c7e16cf6fd4b7313093e3aac9b261dcd70eaaadd2262ec1c4ae56de79a976c')
