from methods.users import *
from config import QUIZ

print(QUIZ)

with app.app_context():
    users = get_all_users()

    for user in filter(lambda u: u.telegram_id, users):
        print(f"sent to {user.name} - {user.telegram_id}")
        send_telegram_notification(user, f"Ссылка на квиз:\n\n{QUIZ}", )
