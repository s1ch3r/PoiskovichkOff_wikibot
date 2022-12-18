from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kboard


#@dp.message_handler(commands=['start','help'])
async def command_start(message : types.Message):
    await bot.send_message(message.from_user.id, 'Привет, я бот ПоисковичкОФФ. Я могу помочь тебе узнать что угодно. Вот список моих возможностей: \n1) /start и /help - показывают список основных комманд \n2) /Запрос - позволяет задать боту вопрос на который он подскажет ответ', reply_markup=kboard)

#@dp.message_handler(commands=['Вопрос'])
'''
async def request_command(message : types.Message):
    await bot.send_message(message.from_user.id, 'Скоро ты сможешь получить здесь ответ на любой свой вопрос.') #, reply_markup=ReplyKeyboardRemove()                         #    await bot.send_message(message.from_user.id, 'Скоро ты сможешь получить сдесь ответ на любой свой вопрос.')
    await message.reply('Вот что нашлось в википедии по вашему запросу:')
'''
def register_handlers_usual(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    #dp.register_message_handler(request_command, commands=['Вопрос', 'вопрос'])