from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kboard


#@dp.message_handler(commands=['start','help'])
async def command_start(message : types.Message):
    """
    Функция приветствует пользователя и показывает список возможностей бота
    :param message:types.Message сообщение отправленное пользователем боту в телеграмм
    :return: возвращает приветственное сообщение со списком команд бота
    """
    await bot.send_message(message.from_user.id, 'Привет, я бот ПоисковичкОФФ. Я могу помочь тебе узнать что угодно. Вот список моих возможностей: \n1) /start и /help - показывают список основных комманд \n2) /Запрос - позволяет задать боту вопрос на который он подскажет ответ', reply_markup=kboard)


def register_handlers_usual(dp : Dispatcher):
    """
    Функция регистрирует ассинхронные фунуции библиотеки aiogram в этом файле и сверяет
    сообщение пользователя со списком команд триггерящих их
    :param dp:Dispatcher диспетчер регистрирующий функции
    :return:регистрирует ассинхронные фунуции библиотеки aiogram в этом файле для последующей передачи в __init__.py
    а затем в bot_telegram.py
    """
    dp.register_message_handler(command_start, commands=['start', 'help'])
