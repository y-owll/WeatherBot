from pyowm import OWM
from pyowm.utils import config as cfg
import telebot

config = cfg.get_default_config()
config['language'] = 'ru'
owm = OWM('key', config)
bot = telebot.TeleBot("token_bot")


@bot.message_handler(commands=['start', 'help', 'stop'])
def send_welcome(message):
    bot.reply_to(message, "погоду в каком городе вам подсказать?")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(message.text)

    w = observation.weather
    temp = w.temperature('celsius')["temp"]

    answer = "в городе " + str(message.text) + " сейчас:" + w.detailed_status + "\n"
    answer += "температура сейчас в районе:" + str(temp) + "\n\n"
    if temp < 10:
        answer += "суперхолодно"
    elif temp < 20:
        answer += "сейчас прохладно,одевайся потеплее"
    elif temp > 20:
        answer += "сейчас тепло"

    bot.reply_to(message, answer)


bot.polling() 
