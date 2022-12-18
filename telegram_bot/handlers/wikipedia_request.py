from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

import wikipedia
from bs4 import BeautifulSoup
import requests

from keyboards import cancel_kboard
from keyboards import additional_kboard
from aiogram.types import ReplyKeyboardRemove

from selenium import webdriver


class FSMRequest(StatesGroup):
    question = State()
    additional_question_request = State()
    additional_question = State()


#@dp.message_handler(commands='Запрос', state=None)
async def cm_start(message : types.Message):
    await FSMRequest.question.set()
    await message.answer('Введите запрос\nДля того чтобы отменить запрос напишите отмена или воспользуйтесь коммандой /Отмена', reply_markup=cancel_kboard)


#выход из машины состояний
async def cancel_command(message : types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Запрос отменен\nЧтобы продолжить введите /start или /help')


#@dp.message_handler(state=FSMRequest.question)
async def get_question(message : types.Message, state: FSMContext):
    def match(text, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')):
        return not alphabet.isdisjoint(text.lower())
    seearch = match(message.text)
    if seearch == True:
        wikipedia.set_lang('ru')
        async with state.proxy() as data:
            data['question'] = message.text
        await FSMRequest.next()  # перевод на следующее состояние
        await message.answer('Вот что нашлось по вашему запросу ' + str(data['question']) + ':', reply_markup=ReplyKeyboardRemove())  # , reply_markup=ReplyKeyboardRemove()
        question_wiki = wikipedia.page(str(data['question']))
        await message.answer('Ссылка на статью: \n' + question_wiki.url)
        await message.answer('Название статьи: \n' + question_wiki.original_title)
        await message.answer('Статья: \n' + question_wiki.summary + '\nДля того чтобы узнать дополнительную информацию введите\n/Дополнительная информация, а чтобы вернуться к главному меню /Отмена', reply_markup=additional_kboard)
    elif seearch == False:
        wikipedia.set_lang('en')
        async with state.proxy() as data:
            data['question'] = message.text
        await FSMRequest.next()  # перевод на следующее состояние
        await message.answer('Вот что нашлось по вашему запросу ' + str(data['question']) + ':', reply_markup=ReplyKeyboardRemove())  # , reply_markup=ReplyKeyboardRemove()
        question_wiki = wikipedia.page(str(data['question']))
        await message.answer('Ссылка на статью: \n' + question_wiki.url)
        await message.answer('Название статьи: \n' + question_wiki.original_title)
        await message.answer('Статья: \n' + question_wiki.summary + '\nДля того чтобы узнать дополнительную информацию введите\n/Дополнительная информация, а чтобы вернуться к главному меню /Отмена', reply_markup=additional_kboard)


#@dp.message_handler(state=FSMRequest.additional_question_request)
async def request_additional_questions(message : types.Message, state: FSMContext):
    def match(text, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')):
        return not alphabet.isdisjoint(text.lower())
    async with state.proxy() as data:
        seearch = match(str(data['question']))
        question_wiki = wikipedia.page(str(data['question']))

    if seearch == True:
        name = question_wiki.original_title
        link = "https://ru.wikipedia.org/wiki/"
        namet = match(name)
        if namet == True:
            link = requests.get(link, params=name)
            link = str(link.url).replace("?", "")
            link = link.replace("&", "")
            link = link + "#"
        else:
            link = link + name.replace(" ", "_")
        soup = BeautifulSoup(question_wiki.html(), "html.parser")
        links = soup.find("div", {"id": "toc"}).find("ul").find_all("a")
        for i in links:
            url = i.get("href")
            await message.answer(url)
    if seearch == False:
        name = question_wiki.original_title
        link = "https://en.wikipedia.org/wiki/"
        link = link + name.replace(" ", "_")
        soup = BeautifulSoup(question_wiki.html(), "html.parser")
        links = soup.find("div", {"id": "toc"}).find("ul").find_all("a")
        for i in links:
            url = i.get("href")
            await message.answer(url)
    await message.answer('Введите название подстатьи которую хотите прочитать, если вы передумали нажмите /Отмена', reply_markup=cancel_kboard)
    await FSMRequest.next()



#@dp.message_handler(state=FSMRequest.additional_question)
async def get_additional_question(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        question_wiki = wikipedia.page(str(data['question']))
    def match(text, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')):
        return not alphabet.isdisjoint(text.lower())
    answer = message.text
    await message.answer('Подстатья ' + str(answer) + ':')
    manswer = match(answer)
    if manswer == True:
        wikipedia.set_lang('ru')
        name = question_wiki.original_title
        link = 'https://ru.wikipedia.org/wiki/'
        link = requests.get(link, params=name)
        link = str(link.url).replace("?", "")
        link = link.replace("&", "")
        url = ""
        l = []
        soup = BeautifulSoup(question_wiki.html(), "html.parser")
        links = soup.find("div", {"id": "toc"}).find("ul").find_all("a")
        for i in links:
            url = i.get("href")
            l.append(url)
        numb = len(l)
        rec = ""
        for k in range(numb - 1):
            if answer == l[k]:
                urlt = match(url)
                if urlt == True:
                    rec = requests.get(link, params=l[k])
                if urlt == False:
                    rec = link + l[k]
                option = webdriver.ChromeOptions()
                option.add_argument("headless")
                driver = webdriver.Chrome(chrome_options=option)
                driver.get(rec.url)
                driver.save_screenshot("scrn.png")
                driver.close()
                photo = open("scrn.png", 'rb')
                await message.answer_photo(photo=photo)
                rurl = rec.url
                await message.answer('Ссылка на статью:' + rurl)
    if manswer == False:
        wikipedia.set_lang('en')
        name = question_wiki.original_title
        link = 'https://en.wikipedia.org/wiki/'
        link = link + name.replace(" ", "_")
        l = []
        soup = BeautifulSoup(question_wiki.html(), "html.parser")
        links = soup.find("div", {"id": "toc"}).find("ul").find_all("a")
        for i in links:
            url = i.get("href")
            l.append(url)
        for k in range(len(l) - 1):
            if answer == l[k]:
                recc = link + l[k]
                option = webdriver.ChromeOptions()
                option.add_argument("headless")
                driver = webdriver.Chrome(chrome_options=option)
                driver.get(recc)
                driver.save_screenshot("scrn.png")
                driver.close()
                photo = open("scrn.png", 'rb')
                await message.answer_photo(photo=photo)
                await message.answer('Ссылка на статью:' + recc)
    await message.answer('Если вы хотите прочитать еще одну подстатью введите ее название, если вы хотите выйти из запроса введите /Отмена')

    

def register_handlers_wikipedia_request(dp : Dispatcher):
    dp.register_message_handler(cm_start, commands=['Запрос'], state=None)
    dp.register_message_handler(cancel_command, state="*", commands=['Отмена'])
    dp.register_message_handler(cancel_command, Text(equals=['отмена', 'Отмена'], ignore_case=True), state="*")
    dp.register_message_handler(get_question, state=FSMRequest.question)
    dp.register_message_handler(request_additional_questions, state=FSMRequest.additional_question_request, commands=['Дополнительная_информация']) #, commands=['/дополнительная_информация']
    dp.register_message_handler(get_additional_question, state=FSMRequest.additional_question)
