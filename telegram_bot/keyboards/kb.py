from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove


b1 = KeyboardButton('/start')
b2 = KeyboardButton('/Запрос')

kboard = ReplyKeyboardMarkup(resize_keyboard=True) #, one_time_keyboard=True

kboard.add(b1).add(b2)#.insert(b2)  .row(b1, b2)
