from aiogram import types, Dispatcher
from create_bot import dp, bot


#@dp.message_handler()
async def echo_send(message : types.Message):
    """
    Функция сообщает о том что пользователь ввел некорректную команду
    :param message:types.Message сообщение отправленное пользователем боту в телеграмм
    :return: возвращает сообщение о вводе корректной команды и их список пользователю в телеграмм
    """
    await bot.send_message(message.from_user.id, 'Я ничего не понял. Пожалуйста, введите корректную команду. Список комманд можно узнать воспользовавшись коммандами /start или /help')


def register_handlers_non_commands(dp : Dispatcher):
    """
    Функция регистрирует ассинхронные фунуции библиотеки aiogram в этом файле
    :param dp:Dispatcher диспетчер регистрирующий функции
    :return:регистрирует ассинхронные фунуции библиотеки aiogram в этом файле для последующей передачи в __init__.py
    а затем в bot_telegram.py
    """
    dp.register_message_handler(echo_send)
