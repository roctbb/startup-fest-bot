from manage import app
from methods.projects import *
from methods.users import *
import segno

with app.app_context():
    with open('users.txt') as file:
        for line in file:
            if line:
                name = ' '.join(line.strip().split(' ')[:2])
                make_user(name, 'student')

