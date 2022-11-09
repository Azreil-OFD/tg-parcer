import telebot
from telebot import types
from time import sleep
import parcer
import datetime
import pand
token = "5615465282:AAEO3poSlY26esEM-4QzeVXwp-htt32tRag"

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id, "Привет ✌️ \nМеня зовут Nopik!\nВведи >rasp< ")


@bot.message_handler(commands=['button'])
def button_message(message):
    markup_clear = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Подготовка...',
                     reply_markup=markup_clear)
    sleep(2)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in parcer.groups.keys():
        item1 = types.KeyboardButton(i)
        markup.add(item1)
    bot.send_message(
        message.chat.id, 'Выберите специальность:', reply_markup=markup)


meta = {}


@bot.message_handler()
def button_message(message: types.Message):
    if (message.text in parcer.groups.keys()):
        meta[message.from_user.id] = message.text
        markup_clear = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Подготовка...',
                         reply_markup=markup_clear)
        sleep(2)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in parcer.groups[message.text]:
            item1 = types.KeyboardButton(i)
            markup.add(item1)
        bot.send_message(message.chat.id, 'Выберите группу:',
                         reply_markup=markup)
    elif (meta[message.from_user.id] in parcer.groups.keys()):
        meta[str(message.from_user.id) +
             "_group"] = meta[message.from_user.id] + " " + message.text
        meta[message.from_user.id] = None
        markup_clear = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Ваша группа:' +
                         meta[str(message.from_user.id) + "_group"], reply_markup=markup_clear)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in [
            'сегодня',
            'завтра',
            'неделя'
        ]:
            item1 = types.KeyboardButton(i)
            markup.add(item1)
        bot.send_message(
            message.chat.id, 'На какой периуд хотите получть расписание:', reply_markup=markup)
    elif (meta[str(message.from_user.id) + "_group"] != None):
        if (message.text in [
            'сегодня',
            'завтра',
            'неделя'
        ]):
            markup_clear = types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, 'Получение расписания: ' + meta[str(
                message.from_user.id) + "_group"] + " на " + message.text, reply_markup=markup_clear)
            i = message.text
            if i == 'сегодня':
                date = datetime.datetime.now().strftime('%d.%m.%Y')
                data = {
                    "group_id" : meta[str(message.from_user.id) + "_group"],
                    "date" : date
                }
                day_gen = pand.day_generate(data)
                photo = open(day_gen[0], 'rb')
                bot.send_photo(message.from_user.id, photo)

            elif i == 'завтра':
                date = (datetime.datetime.now() +
                        datetime.timedelta(days=1)).strftime('%d.%m.%Y')
                data = {
                    "group_id" : meta[str(message.from_user.id) + "_group"],
                    "date" : date
                }
                day_gen = pand.day_generate(data)
                photo = open(day_gen[0], 'rb')
                bot.send_photo(message.from_user.id, photo)
            elif i == 'неделя':
                
                date = datetime.datetime.now().strftime('%d.%m.%Y')
                data = {
                    "group_id" : meta[str(message.from_user.id) + "_group"],
                    "date" : date
                }
        else:
            bot.send_message(message.chat.id , 'Я вас не понимаю')


bot.polling()
