import telebot.types
from telebot import TeleBot
from bot.models import *
from django.core.management.base import BaseCommand
from ...models import *
import requests
import json
from time import sleep, time
from pprint import pprint
from telebot import types


request = {'ok': True,
 'result': [{'chat_join_request': {'chat': {'id': -1002101205896,
                                            'title': 'Новый бот',
                                            'type': 'channel'},
                                   'date': 1706437583,
                                   'from': {'first_name': 'Ветер в голове',
                                            'id': 952462098,
                                            'is_bot': False,
                                            'language_code': 'ru',
                                            'username': 'veter_v_golove2'},
                                   'invite_link': {'creates_join_request': True,
                                                   'creator': {'first_name': 'Кирилл',
                                                               'id': 671176962,
                                                               'is_bot': False,
                                                               'language_code': 'ru',
                                                               'username': 'kirill256'},
                                                   'invite_link': 'https://t.me/+5YtsFPKf...',
                                                   'is_primary': False,
                                                   'is_revoked': False,
                                                   'pending_join_request_count': 1},
                                   'user_chat_id': 952462098},
             'update_id': 338795002}]}

config = Config.objects.all()[0]

TOKEN = config.bot_token
chat_channel = config.chat_chanel
main_channel = config.main_chanel
admins = config.admins.split(',')

# TOKEN = '6229389421:AAEgn0UhQ5ehVrYmoeuWvffBrPNnfCYRpzk'
# chat_channel = '-1002068346046'
# main_channel = '-1002101205896'
try:
    admin = Users.objects.get(status='admin').chat_id
except:
    pass
bot = TeleBot(TOKEN)
last_update = None


def create_new_user_markup(uid):
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn_accept = types.InlineKeyboardButton(text='Принять заявку', callback_data=f'accept:{uid}')
    btn_reject = types.InlineKeyboardButton(text='Отменить заявку', callback_data=f'reject:{uid}')
    kb.add(btn_accept, btn_reject)
    return kb


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Обработка сообщений от админа
        @bot.message_handler(content_types=['text'], func=lambda message: message.chat.id == admin)
        def admin_message_handler(message):
            bot.send_message(admin, 'Бот обработал сообщение админа')

        # Обработка сообщений от пользователя
        @bot.message_handler(content_types=['text'], func=lambda message: message.chat.id != int(chat_channel))
        def user_message_handler(message):
            user, created = Users.objects.get_or_create(chat_id=message.from_user.id, username=message.from_user.username)
            if created:
                welcome_messages = Welcome.objects.all()
                for welcome in welcome_messages:
                    if welcome.type == 'text' and welcome.text != '':
                        bot.send_message(message.from_user.id, welcome.text)
            else:
                admin = Users.objects.get(status='admin')
                bot.send_message(chat_channel, f'Сообщение: {message.text}\n\nuid:{message.from_user.id}\nt.me/{message.from_user.username}')

        # Обработка сообщений админа в чате с ботом
        @bot.message_handler(content_types=['text'], func=lambda message: message.chat.id == int(chat_channel))
        def admin_message_handler(message):
            reply_message = message.reply_to_message.text.split('\n')
            to_message_id = ''
            for line in reply_message:
                if line.startswith('uid'):
                    to_message_id = line.split(':')[1]

            bot.send_message(to_message_id, message.text)

        # Обработка заявок в главный канал
        @bot.chat_join_request_handler(func= lambda message: message.chat.id == int(main_channel))
        def user_request(message: telebot.types.ChatJoinRequest):
            # Отправляем приветсвенное сообщение
            user, created = Users.objects.get_or_create(chat_id=message.from_user.id, username=message.from_user.username)
            welcome_messages = Welcome.objects.all()
            for welcome in welcome_messages:
                if welcome.type == 'text' and welcome.text != '':
                    bot.send_message(message.from_user.id, welcome.text)

            # Отправляем в чат с ботом админу информацию о новой заявке
            admin_markup = create_new_user_markup(message.from_user.id)

            bot.send_message(chat_channel, f'Новая заявка от пользователя: {message.from_user.username}\n\nuid:{message.from_user.id}\nt.me/{message.from_user.username}', reply_markup=admin_markup)
            # bot.approve_chat_join_request(chat_id=main_channel, user_id=message.from_user.id);

        @bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'accept')
        def accept_new_user(call):
            uid = call.data.split(':')[1]
            bot.approve_chat_join_request(chat_id=main_channel, user_id=uid)
            bot.send_message(uid, 'Ваша заявка в канал одобрена')
            bot.answer_callback_query(call.id)

        @bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'accept')
        def accept_new_user(call):
            uid = call.data.split(':')[1]
            bot.approve_chat_join_request(chat_id=main_channel, user_id=uid)
            bot.send_message(uid, 'Ваша заявка в канал одобрена')
            bot.answer_callback_query(call.id)

        @bot.callback_query_handler(func=lambda call: call.data.split(':')[0] == 'reject')
        def accept_new_user(call):
            uid = call.data.split(':')[1]
            bot.decline_chat_join_request(chat_id=main_channel, user_id=uid)
            bot.send_message(uid, 'Ваша заявка в канал отклонена')
            bot.answer_callback_query(call.id)


        try:
            bot.infinity_polling()
        except:
            pass






        # def get_updates(token, offset=None, limit=10, timeout=5):
        #     url = f"https://api.telegram.org/bot{token}/getUpdates"
        #     params = {
        #         "offset": offset,
        #         "limit": limit,
        #         "timeout": timeout
        #     }
        #     response = requests.get(url, params=params)
        #     data = json.loads(response.content)
        #     pprint(data)
        #     # return data["result"]
        #     return request['result']
        #
        #
        # # Замените "YOUR_BOT_TOKEN" на фактический токен вашего бота Telegram
        # bot_token = TOKEN
        #
        # try:
        #     # last_update = m.Task.objects.latest('update_id')
        #     # last_update_id = last_update.update_id
        #     last_update_id = last_update
        # except:
        #     last_update_id = None
        #
        # def handl(update):
        #     pprint(update[0]['chat_join_request']['from']['id'])
        #     user, created = Users.objects.get_or_create(chat_id=update['chat_join_request']['from']['id'], username=update['chat_join_request']['from']['username'])
        #     welcome_messages = Welcome.objects.all()
        #     for welcome in welcome_messages:
        #         if welcome.type == 'text' and welcome.text != '':
        #             bot.send_message(update['chat_join_request']['from']['id'], welcome.text)
        #
        #     Отправляем в чат с ботом админу информацию о новой заявке
        #     uid = update[0]['chat_join_request']['from']['id']
        #     username = update[0]['chat_join_request']['from']['username']
        #     try:
        #         admin_markup = create_markup_for_admin();
        #         bot.send_message(chat_channel,
        #                          f'Новая заявка от пользователя: { username } \n\nuid:{uid}\nt.me/{username}', reply_markup=admin_markup)
        #         bot.send_message(chat_channel, 'Новая заявка от пользователя\nПринять\nОтклонить', reply_markup=admin_markup)
        #         bot.approve_chat_join_request(chat_id=main_channel, user_id=update[0]['chat_join_request']['from']['id']);
        #     except:
        #         pass
        #
        # while True:
        #     print('iter ', last_update_id)
        #     updates = get_updates(bot_token, offset=last_update_id)
        #     if updates:
        #         for update in updates:
        #             last_update_id = update["update_id"] + 1
        #             # pprint(update)
        #             handl(request['result'])
        #
        #     sleep(0.1)