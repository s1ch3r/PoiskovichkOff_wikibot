from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

import wikipedia
from bs4 import BeautifulSoup
import requests

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import ReplyKeyboardRemove
from keyboards import yesno_kboard


class FSMRandom(StatesGroup):
    answer = State()
    confirmation = State()


#@dp.message_handler(commands=['Random', 'random'])
async def random_command(message : types.Message, state: FSMContext):
    """
    Функция находит случайную статью в российской википедии и спрашивает пользователя хочет ли он ее прочитать
    :param message:types.Message сообщение отправленное пользователем боту в телеграмм
    :param state:FSMContext состояние взятое из машины состояний, в котором находится эта функция
    :return: возвращает название случайно полученной статьи из википедии и сообщение спрашивающее  пользователя
    о намерении ее прочесть сообщением в телеграмм
    """
    await FSMRandom.answer.set()
    await message.answer('Бим бим, бам бам, бом бом. Здесь скоро будет рандом!', reply_markup=ReplyKeyboardRemove())
    url = requests.get("https://ru.wikipedia.org/wiki/Special:Random")
    soup = BeautifulSoup(url.content, "html.parser")
    title = soup.find(class_="firstHeading").text
    async with state.proxy() as data:
        data['answer'] = title
    await FSMRandom.next()  # перевод на следующее состояние
    await message.answer(f"{title} \nВы хотите прочитать данную статью?", reply_markup=yesno_kboard)


#выход из машины состояний
async def cancel_random_command(message : types.Message, state: FSMContext):
    """
    Функция отменяет запрос пользователя о получении рандомной статьи из википедии
    :param message:types.Message сообщение отправленное пользователем боту в телеграмм
    :param state:FSMContext состояние взятое из машины состояний, в котором находится эта функция
    :return: выходит из машины состояний и отправляет пользователю сообщение об отмене запроса в телеграмм
    """
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Запрос отменен\nЧтобы продолжить введите /start или /help')


#@dp.message_handler(commands=['Да', 'Нет']) ###возможно нет надо отдельно
async def confirmation_command(message : types.Message, state: FSMContext):
    """
    Функция отправляет пользователю статью из википедии, полученную в функции random_command
    :param message:types.Message сообщение отправленное пользователем боту в телеграмм
    :param state:FSMContext состояние взятое из машины состояний, в котором находится эта функция
    :return: При подверждении от пользователя, отправляет пользователю в телеграмм 3 сообщения:
    ссылку на полученную в random_command статью, ее название и содержание, а также выходит из машины состояний
    """
    wikipedia.set_lang('ru')
    async with state.proxy() as data:
        question_wiki = wikipedia.page(str(data['answer']))
    await message.answer('Ссылка на статью: \n' + question_wiki.url)
    await message.answer('Название статьи: \n' + question_wiki.original_title)
    await message.answer('Статья: \n' + question_wiki.summary + '\nЧтобы продолжить работу введите /start или /help')
    await state.finish()



def register_handlers_random(dp : Dispatcher):
    """
    Функция регистрирует ассинхронные фунуции библиотеки aiogram в этом файле и сверяет
    сообщение пользователя со списком команд триггерящих их
    :param dp:Dispatcher диспетчер регистрирующий функции
    :return: регистрирует ассинхронные фунуции библиотеки aiogram в этом файле для последующей передачи в __init__.py
    а затем в bot_telegram.py
    """
    dp.register_message_handler(random_command, commands=['Случайная_статья', 'Рандомная_статья'])
    dp.register_message_handler(cancel_random_command, state="*", commands=['Нет'])
    dp.register_message_handler(cancel_random_command, Text(equals=['нет', 'Нет'], ignore_case=True), state="*")
    dp.register_message_handler(confirmation_command, state=FSMRandom.confirmation, commands=['Да'])
    dp.register_message_handler(confirmation_command, Text(equals=['Да', 'да'], ignore_case=True), state=FSMRandom.confirmation)

