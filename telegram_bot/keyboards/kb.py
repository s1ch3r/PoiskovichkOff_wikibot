from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b1 = KeyboardButton('/start')
b2 = KeyboardButton('/Запрос')
b3 = KeyboardButton('/Отмена')
b4 = KeyboardButton('/Дополнительная_информация')
b5 = KeyboardButton('/Случайная_статья')
b6 = KeyboardButton('/Да')
b7 = KeyboardButton('/Нет')

kboard = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_kboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
additional_kboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
yesno_kboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kboard.add(b1).add(b2).add(b5)#.insert(b2)  .row(b1, b2)
cancel_kboard.add(b3)
additional_kboard.add(b4).add(b3)
yesno_kboard.row(b6, b7)
