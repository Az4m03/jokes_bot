import requests
import random
import telebot
from bs4 import BeautifulSoup as b

import settings


def parser(url):
    r = requests.get(url)
    soup = b(r.text, 'html.parser')
    anekdots = soup.find_all('div', class_='text')
    return [c.text for c in anekdots]


list_of_jokes = parser(settings.URL)
random.shuffle(list_of_jokes)

bot = telebot.TeleBot(settings.TOKEN)


@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, 'Здраствайте! Чтобы посмеяться введите любую цифру:')


@bot.message_handler(content_types=['text'])
def jokes(message):
    if message.text.lower() in '123456789':
        bot.send_message(message.chat.id, list_of_jokes[0])
        del list_of_jokes[0]
    else:
        bot.send_message(message.chat.id, 'Введите любую цифру:')


bot.polling()
