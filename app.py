from manage import *
from blueprints import *

app.register_blueprint(payments_blueprint, url_prefix='/payments')
app.register_blueprint(users_blueprint, url_prefix='/users')


if __name__ == '__main__':
    app.run(HOST, PORT)