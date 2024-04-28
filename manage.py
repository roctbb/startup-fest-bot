import sentry_sdk
from flask import Flask
from .models import db
from flask_migrate import Migrate
from flask_cors import CORS
from sentry_sdk.integrations.flask import FlaskIntegration
from .config import *

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            FlaskIntegration(),
        ],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=0
    )

app = Flask(__name__)

db_string = "postgresql://{}:{}@{}:{}/{}".format(DB_LOGIN, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE)
app.config['SQLALCHEMY_DATABASE_URI'] = db_string
app.config['SECRET_KEY'] = APP_SECRET

app.config['MAIL_SERVER'] = EMAIL_SERVER
app.config['MAIL_PORT'] = EMAIL_PORT
app.config['MAIL_USERNAME'] = EMAIL_USERNAME
app.config['MAIL_PASSWORD'] = EMAIL_PASSWORD
app.config['MAIL_USE_TLS'] = EMAIL_USE_TLS
app.config['MAIL_USE_SSL'] = EMAIL_USE_SSL
app.config['MAIL_DEBUG'] = EMAIL_DEBUG

mail = Mail(app)
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)
