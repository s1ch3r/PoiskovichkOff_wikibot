from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp
import wikipedia
from bs4 import BeautifulSoup
import requests

from keyboards import kboard
from aiogram.types import ReplyKeyboardRemove


wikipedia.set_lang('ru')
'''
a = str(input())
b = wikipedia.page(a)
print(b.url)
print(b.original_title)
print(b.summary)
'''

class FSMRequest(StatesGroup):
    question = State()
    #additional_question = State()

#@dp.message_handler(commands='Запрос', state=None)
async def cm_start(message : types.Message):
    await FSMRequest.question.set()
    await message.answer('Введите запрос')

#@dp.message_handler(state=FSMRequest.question)
async def get_question(message : types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['question'] = message.text
    await message.answer('Вот что нашлось по вашему запросу ' + str(data['question']) + ':') #, reply_markup=ReplyKeyboardRemove()
    question_wiki = wikipedia.page(str(data['question']))
    await message.answer('Ссылка на статью: \n' + question_wiki.url)
    await message.answer('Название статьи: \n' + question_wiki.original_title)
    await message.answer('Статья: \n' + question_wiki.summary + '\nДля того чтобы продолжить введитие /start или /help')
    await state.finish() #эта тема выходит из машины состояний
    '''
    #url = question_wiki.url
    request = requests.get(question_wiki.url)
    soup = BeautifulSoup(request.text, 'html.parser')
    links = soup.find_all('div', class_= 'toctitle')
    url = question_wiki.url + links[0].find('a')['href']
    await message.answer("что-то",url )
    #await message.answer('Представь что тут статья из вики')
    #здесь собственно будет обрабатываться запрос и затем выдаваться в следующей строке
    await state.finish() #эта тема выходит из машины состояний
    '''
##@dp.message_handler()
#async def get_add_questions(message : types.Message, state=FSMContext):




def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(cm_start, commands=['Запрос'], state=None)
    dp.register_message_handler(get_question, state=FSMRequest.question)
