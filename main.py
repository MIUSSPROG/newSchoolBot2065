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

# cred = credentials.Certificate("schooltrainitskills-firebase-adminsdk-2k8f3-da15def773.json")
#
# default_app = firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://schooltrainitskills-default-rtdb.firebaseio.com/',
#     'storageBucket': 'gs://schooltrainitskills.appspot.com/'
# })


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
