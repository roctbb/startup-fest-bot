from methods.users import *
from config import PRICELIST

with app.app_context():
    users = get_all_users()

    for user in filter(lambda u: u.telegram_id, users):
        send_telegram_notification(user, f"Прейкурант:\n\n{PRICELIST}", )
