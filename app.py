import telebot
from extensions import APIException, Convertor
from config import TOKEN, exchanges
import traceback


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    bot.reply_to(message, f"Добро пожаловать, {message.chat.username}! "
                          f"Данный бот поможет узнать стоимость разных валют."
                          f"Чтобы приступить, введите команду в следующем формате:\n"
                          f"<из какой валюты> <в какую валюту перевести> <количество переводимой валюты>, "
                          f"например:\n"
                          f"рубль доллар 3000\n"
                          f"Нажмите или введите /values, чтобы увидеть доступные для преобразования валюты.\n"
                          f"Нажмите или введите /help для справки.")


@bot.message_handler(commands=['help'])
def start(message: telebot.types.Message):
    bot.reply_to(message, f"Чтобы приступить, введите команду в следующем формате:\n"
                          f"<из какой валюты> <в какую валюту перевести> <количество>"
                          f" через пробел, например:\n"
                          f"доллар евро 45 ")


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in exchanges.keys():
         text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров, их должно быть 3.')

        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling(none_stop=True)
