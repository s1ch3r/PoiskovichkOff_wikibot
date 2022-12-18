from aiogram import types, Dispatcher
from create_bot import dp, bot


#@dp.message_handler()
async def echo_send(message : types.Message):
    #await message.answer(message.text)
    await bot.send_message(message.from_user.id, 'Я ничего не понял. Пожалуйста, введите корректную команду. Список комманд можно узнать воспользовавшись коммандами /start или /help')


def register_handlers_non_commands(dp : Dispatcher):
    dp.register_message_handler(echo_send)