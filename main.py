import os
import telebot
from telebot import types
from flask import Flask, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import uuid
from datetime import date
import json

TOKEN = '2090856829:AAEpFZJPrnJrC2qC_d6aTiSUHv1rbce272M'
APP_URL = f'https://trainin-it-skills-2065.herokuapp.com/{TOKEN}'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

fullname = ''
task_text_to_answer = ''

cred = credentials.Certificate("schooltrainitskills-firebase-adminsdk-2k8f3-da15def773.json")

default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://schooltrainitskills-default-rtdb.firebaseio.com/',
    'storageBucket': 'gs://schooltrainitskills.appspot.com/'
})


@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(message.from_user.id,
                     "✋ Добро пожаловать в систему проверки знаний ГБОУ Школа 2065!")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item0 = types.KeyboardButton('Введите ФИО и класс')
    item1 = types.KeyboardButton('1')
    item2 = types.KeyboardButton('2')
    item3 = types.KeyboardButton('3')
    item4 = types.KeyboardButton('4')
    item5 = types.KeyboardButton('5')
    item6 = types.KeyboardButton('6')
    item7 = types.KeyboardButton('7')
    item8 = types.KeyboardButton('8')
    item9 = types.KeyboardButton('9')
    markup.add(item0, item1, item2, item3, item4, item5, item6, item7, item8, item9)
    bot.send_message(message.chat.id,
                     'Привет, {0.first_name}! Выбери номер задачи'.format(message.from_user),
                     reply_markup=markup)

# ------------------------------


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == '1':
            # sti = open('1.png', 'rb')
            task_text = 'Что такое декомпозиция?'
            show_task(1, message, None, task_text)
        elif message.text == 'Введите ФИО и класс':
            task_text = 'Введите ФИО и класс'
            show_task(-1, message, None, task_text)
        elif message.text == '2':
            # sti = open('2.png', 'rb')
            task_text = 'Что такое СУБД?'
            show_task(2, message, None, task_text)
        elif message.text == '3':
            # sti = open('3.png', 'rb')
            task_text = 'Что такое база данных?'
            show_task(3, message, None, task_text)
        elif message.text == '4':
            # sti = open('4.png', 'rb')
            task_text = 'Перечислите популярные СУБД'
            show_task(4, message, None, task_text)
        elif message.text == '5':
            task_text = 'В какой нормальной форме находится следующая таблица(Модель-Фирма - Составной первичный ключ)'
            sti = open('db5.png', 'rb')
            show_task(5, message, sti, task_text)
        elif message.text == '6':
            task_text = 'В какой нормальной форме находится следующая таблица(Модель - первичный ключ)'
            sti = open('db6.png', 'rb')
            show_task(6, message, sti, task_text)
        elif message.text == '7':
            task_text = 'В какой нормальной форме находится следующая таблица(Сотрудник - Первичный ключ)'
            sti = open('db7.png', 'rb')
            show_task(7, message, sti, task_text)
        elif message.text == '8':
            task_text = 'В какой нормальной форме находится следующая таблица(Первичный составной ключ - StudentId, CourseId)'
            sti = open('db8.png', 'rb')
            show_task(8, message, sti, task_text)
        elif message.text == '9':
            task_text = 'В какой нормальной форме находится следующая таблица'
            sti = open('db9.png', 'rb')
            show_task(9, message, sti, task_text)

        elif message.text == '/get':
            all_answers_json = db.reference("schooltrainitskills-default-rtdb").get()
            mas = str(all_answers_json).split("correct': ")
            res = []
            for el in mas:
                res.append(el[0])
            # res = []
            # for item in mas:
            #     print(item)
            #     start = item.find('question')
            #     item_clean = item[start + 12:].split("'}")[0]
            #     print(item_clean)
            #     res.append(item_clean)
            # res = ['Копилка вопросов ======>'] + res
            # print(res)
            bot.send_message(message.from_user.id, ', '.join(res))


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'yes':
        bot.send_message(call.message.chat.id, "Введите ответ =>")
        bot.register_next_step_handler(call.message, get_answer)
    elif call.data == 'no':
        bot.send_message(call.message.chat.id, "Возможно позже...")


def show_task(n, message, sti, task_text):
    global num
    global fullname
    global task_text_to_answer

    task_text_to_answer = task_text

    if n == -1:
        fullname = 'true'
    else:
        fullname = ''

    if sti is not None:
        bot.send_photo(message.chat.id, sti)
    bot.send_message(message.from_user.id, text=task_text)

    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    bot.send_message(message.from_user.id, text="Готовы ответить?", reply_markup=keyboard)
    num = n


def get_answer(message):
    global answer
    global userName
    global fullname
    global task_text_to_answer
    try:
        if fullname == 'true':
            fullname = message.text
        else:
            fullname = userName
            answer = message.text
            userName = message.from_user.first_name
            new_answer = {
                "question": task_text_to_answer,
                "answer": answer
            }
            db.reference(f"schooltrainitskills-default-rtdb/{fullname}/" + str(num)).set(new_answer)
            bot.send_message(message.chat.id, f"Ответ принят!")
    except Exception as ex:
        print(ex)
    # if num == 1:
    #     if answer == 'zyxw':
    #         new_answer1 = {
    #             "correct": 1
    #         }
    #     else:
    #         new_answer1 = {
    #             "correct": 0
    #         }
    #     db.reference(f"schooltrainitskills-default-rtdb/{userName}/" + str(num)).set(new_answer1)
    #     bot.send_message(message.chat.id, f"Ответ принят!")
    # if num == 2:
    #     if answer == 'xzy':
    #         new_answer2 = {
    #             "correct": 1
    #         }
    #     else:
    #         new_answer2 = {
    #             "correct": 0
    #         }
    #     db.reference(f"schooltrainitskills-default-rtdb/{userName}/" + str(num)).set(new_answer2)
    #     bot.send_message(message.chat.id, f"Ответ принят!")
    # if num == 3:
    #     if answer == 'yxz':
    #         new_answer3 = {
    #             "correct": 1
    #         }
    #     else:
    #         new_answer3 = {
    #             "correct": 0
    #         }
    #     db.reference(f"schooltrainitskills-default-rtdb/{userName}/" + str(num)).set(new_answer3)
    #     bot.send_message(message.chat.id, f"Ответ принят!")
    # if num == 4:
    #     if answer == 'zyxw':
    #         new_answer4 = {
    #             "correct": 1
    #         }
    #     else:
    #         new_answer4 = {
    #             "correct": 0
    #         }
    #     db.reference(f"schooltrainitskills-default-rtdb/{userName}/" + str(num)).set(new_answer4)
    #     bot.send_message(message.chat.id, f"Ответ принят!")


def count_correct_answers():
    all_answers_json = str(db.reference("schooltrainitskills-default-rtdb").get())
    pos = all_answers_json.find('}')
    res = all_answers_json[pos - 1:pos]
    return int(res)


def check_answer():
    all_answers_json = db.reference("schooltrainitskills-default-rtdb").get()
    mas = str(all_answers_json).split(',')


# ------------------------------
@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    return '!', 200


@server.route("/")
def index():
    return "<h1>Hello!</h1>"


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
