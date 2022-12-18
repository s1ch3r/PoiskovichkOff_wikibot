from aiogram import types, Dispatcher
#from create_bot import dp, bot
from aiogram.dispatcher.filters import Text

import wikipedia
from bs4 import BeautifulSoup
import requests
#import webbrowser

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import ReplyKeyboardRemove
from keyboards import yesno_kboard


class FSMRandom(StatesGroup):
    answer = State()
    confirmation = State()


#@dp.message_handler(commands=['Random', 'random'])
async def random_command(message : types.Message, state: FSMContext):
    await FSMRandom.answer.set()
    await message.answer('Бим бим, бам бам, бом бом. Здесь скоро будет рандом!', reply_markup=ReplyKeyboardRemove())
        #question_wiki = "https://ru.wikipedia.org/wiki/Special:Random"
        #await message.answer('Ссылка на статью: \n' + question_wiki.url)
        #await message.answer('Название статьи: \n' + question_wiki.original_title)
        #await message.answer('Статья: \n' + question_wiki.summary)
    url = requests.get("https://ru.wikipedia.org/wiki/Special:Random")
    soup = BeautifulSoup(url.content, "html.parser")
    title = soup.find(class_="firstHeading").text #text
    async with state.proxy() as data:
        data['answer'] = title #str(f"{title}")
    await FSMRandom.next()  # перевод на следующее состояние
    await message.answer(f"{title} \nВы хотите прочитать данную статью?", reply_markup=yesno_kboard)  ###################################### новую клаву
      #.replace(" ", "_")
        #question_wiki = wikipedia.page(str(data['question']))


#@dp.message_handler(commands=['Да', 'Нет']) ###возможно нет надо отдельно
async def confirmation_command(message : types.Message, state: FSMContext):
    wikipedia.set_lang('ru')
    async with state.proxy() as data:
        question_wiki = wikipedia.page(str(data['answer']))
    ans = message.text
    if ans == "/Да" or ans == "Да" or ans == "да":
        await message.answer('Ссылка на статью: \n' + question_wiki.url)
        await message.answer('Название статьи: \n' + question_wiki.original_title)
        await message.answer('Статья: \n' + question_wiki.summary + '\nЧтобы продолжить работу введите /start или /help')
        await state.finish()
    else:
        await message.answer('Запрос отменен. Чтобы продолжить работу введите /start или /help')
        await state.finish()

#ans = message.text
#if ans == "/Да" or answer == "Да" or answer == "да":



def register_handlers_random(dp : Dispatcher):
    dp.register_message_handler(random_command, commands=['Случайная_статья', 'Рандомная_статья'])
    dp.register_message_handler(confirmation_command, state=FSMRandom.confirmation, commands=['Да', 'Нет'])
    dp.register_message_handler(confirmation_command, Text(equals=['Да', 'да', 'Нет', 'нет'], ignore_case=True), state=FSMRandom.confirmation)
