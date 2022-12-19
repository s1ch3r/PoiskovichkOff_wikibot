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
    
    
def match(text, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')):
    """
    Объявляем функцию 'match', которая сравнивае вводимое значение и если оно совпадает с переменной 'aphabet'(Русский алфавит) -
    то оно выдаёт 'bool' значение 'True', в противном случае 'False'. Это нужно для проверки языка, на которм пользователь хочет найти информацию.
    :param text: текст исходного сообщения, отправленного пользователем боту в телеграмм
    :param alphabet: множество состоящее из букв русского алфавит
    :return: возвращает буллевое значение True, если исходное сообщение содержит буквы русского алфавита и False,
    если сообщение не содержит букв русского алфавита
    """
    return not alphabet.isdisjoint(text.lower())


# @dp.message_handler(commands='Запрос', state=None)
async def cm_start(message: types.Message):
    await FSMRequest.question.set()
    await message.answer(
        'Введите запрос\nДля того чтобы отменить запрос напишите отмена или воспользуйтесь коммандой /Отмена',
        reply_markup=cancel_kboard)


# выход из машины состояний
async def cancel_command(message: types.Message, state: FSMContext):
     """
    Функция отменяет запрос пользователя
    :param message: это сообщение получаемое от пользователя
    :param state: это сообщение получаемое от пользователя
    :return: Выводит пользователя из машины состояний и отправляет ему в телеграмм ботом сообщение об отмене запроса
    """
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Запрос отменен\nЧтобы продолжить введите /start или /help')


# @dp.message_handler(state=FSMRequest.question)
async def get_question(message: types.Message, state: FSMContext):
    '''
    В данной функции мы получаем поисковой запрос пользователя.
    Проверяем, на каком языке сделан поисковой запрос.
    Благодаря полученному ответу определяем какая часть кода будет работать.
    Когда мы опредилили какая часть кода будет работать, мы задаем язык, на котором будет выведена информация на сайте.
    После чего мы 
    :param message: это сообщение получаемое от пользователя
    :param state: FSMContext состояние, взятое из машины состояний, в котором находится эта функция
    :return: взвращает пользователю 4 сообщения в телеграмм, в которых указывается поисковой запрос пользователя, ссылка на статью,
    заголовок статьи, краткое содержание и предложение посмотреть дополнительную информацию.
    '''
    seearch = match(message.text)

    if seearch == True:
        wikipedia.set_lang('ru')
        async with state.proxy() as data:
            data['question'] = message.text

        await FSMRequest.next()  # перевод на следующее состояние
        await message.answer('Вот что нашлось по вашему запросу ' + str(data['question']) + ':',reply_markup=ReplyKeyboardRemove())
        question_wiki = wikipedia.page(str(data['question']))
        await message.answer('Ссылка на статью: \n' + question_wiki.url)
        await message.answer('Название статьи: \n' + question_wiki.original_title)
        await message.answer('Статья: \n' + question_wiki.summary + '\nДля того чтобы узнать дополнительную информацию введите\n/Дополнительная информация, а чтобы вернуться к главному меню /Отмена',reply_markup=additional_kboard)
    elif seearch == False:

        wikipedia.set_lang('en')
        async with state.proxy() as data:
            data['question'] = message.text
        await FSMRequest.next()  # перевод на следующее состояние
        await message.answer('Вот что нашлось по вашему запросу ' + str(data['question']) + ':',
                             reply_markup=ReplyKeyboardRemove())
        question_wiki = wikipedia.page(str(data['question']))
        await message.answer('Ссылка на статью: \n' + question_wiki.url)
        await message.answer('Название статьи: \n' + question_wiki.original_title)
        await message.answer('Статья: \n' + question_wiki.summary + '\nДля того чтобы узнать дополнительную информацию введите\n/Дополнительная информация, а чтобы вернуться к главному меню /Отмена',reply_markup=additional_kboard)


# @dp.message_handler(state=FSMRequest.additional_question_request)
async def request_additional_questions(message: types.Message, state: FSMContext):
    '''
    В данной функции мы получаем ответ от пользователя.
    Проверяем, на каком языке сделан поисковой запрос.
    Благодаря полученному ответу определяем какая часть кода будет работать.
    Мы присваеваем заголовок переменной 'name', которая будет использоваться для формирования ссылок, на разделы статьи
    и для вывода разделов.
    Благодаря полученному заголовку, мы формируем ссылку, путём складывания ссылки на основную страницу wikipedia и
    нашего зоголовка. После чего мы получаем HTML код страницы, в котором находим класс "div" с id "toc" и уже в нём ищем
    класс "ul", в которм собираем все классы "a", из которых получаем ссылки из класса "href".
    После проделанного действия мы отправляем пользователю список разделов страницы, которую он хотел найти.
    :param message: это сообщение получаемое от пользователя
    :param state: FSMContext состояние, взятое из машины состояний, в котором находиться эта функция
    :return: отправляет пользователю сообщениями в телеграмм список подстатей, запрошенной функцей get_question, статьи из википедии и запрос на название подстатьи
    '''
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
    await message.answer('Введите название подстатьи которую хотите прочитать, если вы передумали нажмите /Отмена',reply_markup=cancel_kboard)
    await FSMRequest.next()


# @dp.message_handler(state=FSMRequest.additional_question)
async def get_additional_question(message: types.Message, state: FSMContext):
    '''
    В данной функции мы получаем ответ от пользователя.
    Проверяем, на каком языке сделан поисковой запрос.
    Благодаря полученному ответу определяем какая часть кода будет работать.
    Мы присваеваем заголовок переменной 'name', которая будет использоваться для формирования ссылок, на разделы статьи
    и для вывода разделов.
    Благодаря полученному заголовку, мы формируем ссылку, путём складывания ссылки на основную страницу wikipedia и
    нашего зоголовка. После чего мы получаем HTML код страницы, в котором находим класс "div" с id "toc" и уже в нём ищем
    класс "ul", в которм собираем все классы "a", из которых получаем ссылки из класса "href".
    После чего мы формируем список из разделов страницы.
    сравниваем каждый элемент списка с сообщением, полученным от пользователя, если совпадение найдено, делаем скриншот
    странцы, отправляем его пользователю вместе с ссылкой на данный раздел, если же совпадение не найдено, отправляем 
    пользователю ответ с сообщением, что такой раздел не найден.
    :param message: это сообщение получаемое от пользователя
    :param state: FSMContext состояние, взятое из машины состояний, в котором находиться эта функция
    :return: отправляет пользователю скриншот в телеграмм подстатьи, если она найдена, или сообщение об отсутствии подстатьи если она не найдена.
    Также отправляет пользователю в телеграмм сообщение с запросом новой новой подстатьи или выходом из запроса
    '''
    async with state.proxy() as data:
        question_wiki = wikipedia.page(str(data['question']))
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
                #Данный участок кода был взят из этого видео:https://www.youtube.com/watch?v=KuQZN2kxftg
                option = webdriver.ChromeOptions()
                option.add_argument("headless")
                driver = webdriver.Chrome(chrome_options=option)
                driver.get(rec.url)
                driver.save_screenshot("scrn.png")
                driver.close()
                photo = open("scrn.png", 'rb')
                #конец заимствования
                await message.answer_photo(photo=photo)
                rurl = rec.url
                await message.answer('Ссылка на статью:' + rurl)
            else:
                await message.answer("Такой раздел не найден")
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
            else:
                await message.answer("Такой раздел не найден")
    await message.answer('Если вы хотите прочитать еще одну подстатью введите ее название, если вы хотите выйти из запроса введите /Отмена')


def register_handlers_wikipedia_request(dp: Dispatcher):
    """
    Функция регистрирует ассинхронные фунуции библиотеки aiogram в этом файле и сверяет
    сообщение пользователя со списком команд триггерящих их
    :param dp:Dispatcher диспетчер регистрирующий функции
    :return: регистрирует ассинхронные фунуции библиотеки aiogram в этом файле для последующей передачи в __init__.py
    а затем в bot_telegram.py
    """
    dp.register_message_handler(cm_start, commands=['Запрос'], state=None)
    dp.register_message_handler(cancel_command, state="*", commands=['Отмена'])
    dp.register_message_handler(cancel_command, Text(equals=['отмена', 'Отмена'], ignore_case=True), state="*")
    dp.register_message_handler(get_question, state=FSMRequest.question)
    dp.register_message_handler(request_additional_questions, state=FSMRequest.additional_question_request,commands=['Дополнительная_информация'])
    dp.register_message_handler(get_additional_question, state=FSMRequest.additional_question)
