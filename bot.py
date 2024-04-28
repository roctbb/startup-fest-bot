import sys

from telebot.types import InlineKeyboardMarkup

import bot
from objects.telegram_bot import *
from methods.users import *
from methods.projects import *
from config import BOT_TOKEN
import requests

WELCOME_TEXT = """👋 Привет!

🗳 Этот бот позволит Вам проголосовать за проекты на 1561 StartUpFest, инвестировав в них нашу внутреннюю валюту. В конце мероприятия инвестированные средства можно будет потратить.

💪 Если Вы автор проекта - постарайтесь максимально подробно рассказать о своей идее и результатах, чтобы убедить зрителей, что инвестировать нужно именно в ваш проект!

🦸 Если Вы эксперт или гость - постарайтесь внимательно изучить все проекты и сделать разумный выбор - какой проект Вы хотели бы поддержать?

🍰 Кстати, гости, внимательно изучившие проекты в конце мероприятия тоже смогут побороться за призы в проектном квизе!"""

NEW_INVESTMENT_TEXT = f"➕ Новая инвестиция"
CHANGE_INVESTMENT_TEXT = f"✏️ Изменить инвестиции"
CANCEL_INVESTMENT_TEXT = 'Я передумал!'

INPROGRESS_INVESTMENTS = {}


@bot.message_handler(commands=['start', 'help'])
@find_user
def send_welcome(message, user):
    bot.send_message(message.from_user.id, ".")
    bot.send_message(message.from_user.id, WELCOME_TEXT)
    if not user:
        bot.send_message(message.from_user.id,
                         "Для начала работы нужно пройти авторизацию. Пришлите мне фотографию вашего QR кода со стойки регистрации.")
    else:
        send_investment_menu(message, user)


def send_investment_menu(message, user):
    keyboard = types.ReplyKeyboardMarkup()

    button = types.KeyboardButton(text=NEW_INVESTMENT_TEXT)
    keyboard.add(button)

    button = types.KeyboardButton(text=CHANGE_INVESTMENT_TEXT)
    keyboard.add(button)

    current_investments = ""
    for investment in user.investments():
        current_investments += f"\n👍 {investment['title']}: 💸 {investment['amount']}"

    text = "Добро пожаловать, {0}! В кого инвестируем?".format(user.name)

    text += f'\n\n 💰 Доступно для инвестирования: {user.balance("PC")} PC.'

    if current_investments:
        text += '\n\n 🚀 Текущие инвестиции: \n' + current_investments

    bot.send_message(message.from_user.id, text,
                     reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
@requires_user
def process_message(message, user):
    if message.text.strip() == NEW_INVESTMENT_TEXT:
        keyboard = types.ReplyKeyboardMarkup()

        for name in map(lambda p: p.name, get_all_projects()):
            keyboard.add(types.KeyboardButton(text=name))

        keyboard.add(types.KeyboardButton(text='Я передумал!'))

        message = bot.send_message(message.from_user.id, 'В какой проект Вы хотите инвестировать?',
                                   reply_markup=keyboard)

        bot.register_next_step_handler(message, choose_project)

    elif message.text == CHANGE_INVESTMENT_TEXT:
        keyboard = types.ReplyKeyboardMarkup()

        for name in map(lambda i: i['title'], user.investments()):
            keyboard.add(types.KeyboardButton(text=name))

        keyboard.add(types.KeyboardButton(text='Я передумал!'))

        message = bot.send_message(message.from_user.id, 'Размер какой инвестиции вы хотите изменить?',
                                   reply_markup=keyboard)

        bot.register_next_step_handler(message, choose_project)
    else:
        bot.send_message(message.from_user.id, "Для продолжения введите /start.", reply_markup=types.ReplyKeyboardRemove())


@requires_user
def choose_project(message, user):
    project_name = message.text
    if message.text == CANCEL_INVESTMENT_TEXT:
        send_investment_menu(message, user)
        return

    try:
        project = find_project_by_name(project_name)

        INPROGRESS_INVESTMENTS[user.id] = project.id

        message = bot.send_message(message.from_user.id, f"Сколько хотите инвестировать? Введите 0 для отмены.",
                                   reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, choose_amount)

    except:
        bot.send_message(message.from_user.id, "Такой проект не найден.")
        send_investment_menu(message, user)


@requires_user
def choose_amount(message, user):
    try:
        if int(message.text) <= 0:
            raise InvalidData

        project = find_project_by_id(INPROGRESS_INVESTMENTS[user.id])
        had_investmenents = has_investmensts_from(project, user)
        make_investment(project, user, int(message.text))

        if not had_investmenents:
            message = bot.send_message(message.from_user.id,
                                       f"Расскажите, почему Вы решили инвестировать в проект? Постарайтесь ответить развернуто, мы передадим Ваши комментарии авторам.")
            bot.register_next_step_handler(message, choose_comment)
        else:
            bot.send_message(message.from_user.id, "Изменения сохранены!")
            send_investment_menu(message, user)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(e)
        bot.send_message(message.from_user.id, "Невозможно провести операцию.")
        send_investment_menu(message, user)


@requires_user
def choose_comment(message, user):
    if not message.text or len(message.text) < 10:
        message = bot.send_message(message.from_user.id,
                                   f"Слишком короткий комментарий...")
        bot.register_next_step_handler(message, choose_comment)
    try:
        project = find_project_by_id(INPROGRESS_INVESTMENTS[user.id])
        add_comment(project, user, message.text)

        bot.send_message(message.from_user.id, "Инвестиция проведена упешно!")
        send_investment_menu(message, user)

        del INPROGRESS_INVESTMENTS[user.id]
    except:
        bot.send_message(message.from_user.id, "Невозможно провести операцию.")
        send_investment_menu(message, user)


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
