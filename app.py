from manage import *
from blueprints import *

app.register_blueprint(payments_blueprint, url_prefix='/payments')
app.register_blueprint(users_blueprint, url_prefix='/users')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(HOST, PORT, debug=DEBUG)
