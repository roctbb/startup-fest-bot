from objects.telegram_bot import *
from methods.users import *
from config import BOT_TOKEN
import requests

@bot.message_handler(content_types=['photo'])
@find_user
def task_handler(message, user):
    if user:
        bot.send_message(message.from_user.id, "Вы уже авторизированы.")
    else:
        file_id = message.photo[-1].file_id
        path = bot.get_file(file_id)
        real_path = 'https://api.telegram.org/file/bot{0}/'.format(BOT_TOKEN) + path.file_path
        url = 'http://api.qrserver.com/v1/read-qr-code/'

        res = requests.post(url, {'fileurl': real_path})
        try:
            registration_code = res.json()[0]['symbol'][0]['data']
            user = find_user_by_registration_code(registration_code)
            activate_user(user, message.from_user.id)
            bot.send_message(message.from_user.id,
                                "Успешная активация")
        except:
            bot.send_message(message.from_user.id,
                                "Не удалось провести авторизацию, попробуйте прислать другую фотографию.")


bot.polling(none_stop=True)
