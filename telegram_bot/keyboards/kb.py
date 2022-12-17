from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove


b1 = KeyboardButton('/start')
b2 = KeyboardButton('/Запрос')
b3 = KeyboardButton('/Отмена')
b4 = KeyboardButton('/Дополнительная_информация')

kboard = ReplyKeyboardMarkup(resize_keyboard=True) #, one_time_keyboard=True
cancel_kboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
additional_kboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kboard.add(b1).add(b2)#.insert(b2)  .row(b1, b2)
cancel_kboard.add(b3)
additional_kboard.row(b4, b3)
