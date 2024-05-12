from methods.users import *
from config import QUIZ

with app.app_context():
    users = get_all_users()

    for user in filter(lambda u: u.telegram_id, users):
        send_telegram_notification(user, f"Ссылка на квиз:\n\n{QUIZ}", )
