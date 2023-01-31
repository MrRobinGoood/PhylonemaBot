import pandas as pd

import asyncio
import random
from typing import List
import re
import pymorphy2

morph = pymorphy2.MorphAnalyzer()
from nltk.tokenize import word_tokenize

import os

import aiogram.utils.exceptions

from aiogram import types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import dp, bot
from keyboards import keyboards_client

from Cinema.CinemaCard import CinemaCard

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import random
from typing import List

import json
import hashlib

# Значения: [С какого файла(строки) начинать, Сколько файлов(inline кнопок) выводить]
DEFAULT_PAGES_PARAMS = [0, 5]
PHILOSOPHY_COURSE_PATH = 'resources/philosophy_course'
LITERATURE_COURSE_PATH = 'resources/literature'
TEMP_ID_PATH = 'resources/temp/temp_id.json'

ADMINS = {828256665: 'Бартенев Андрей', 1144869308: 'Авдошин Максим', 1048347854: 'Василиса',
          703787945: 'Малышев Владислав Борисович'}
global temp_message_quote
global temp_delete_message
global new_film


async def open_file(name: str, directory_in_resources: str, sep: str) -> List:
    try:
        with open(f'resources/{directory_in_resources}/{name}', encoding='utf8') as opened_file:
            result = [x.strip() for x in opened_file.read().split(sep)]
            return result
    except OSError as e:
        print(e)


async def read_file(name: str, directory_in_resources: str) -> List:
    try:
        with open(f'resources/{directory_in_resources}/{name}', encoding='utf8') as opened_file:
            result = [x.strip() for x in opened_file.read()]
            return result
    except OSError as e:
        print(e)


async def append_with_sep_to_file(input: str, name: str, directory_in_resources: str, sep: str):
    try:
        with open(f'resources/{directory_in_resources}/{name}', 'a', encoding='utf8') as opened_file:
            opened_file.write(f'\n{sep}\n{input}')
    except OSError as e:
        print(e)


async def append_to_file(input: str, name: str, directory_in_resources: str):
    try:
        with open(f'resources/{directory_in_resources}/{name}', 'a', encoding='utf8') as opened_file:
            opened_file.write(input)
    except OSError as e:
        print(e)


async def callback_encode(sep: str, input_str: str, path_to_json: str) -> str:
    input_str_id = f'{sep}{str(int(hashlib.sha1(input_str.encode("utf-8")).hexdigest(), 16) % (10 ** 8))}'
    result = ''
    try:
        with open(path_to_json) as js_read:
            opened_json = json.load(js_read)
            if input_str_id not in opened_json:
                opened_json[input_str_id] = input_str
        with open(path_to_json, 'w') as js_write:
            json.dump(opened_json, js_write)
        result = input_str_id
    except OSError as e:
        print(e)
    return result


async def callback_decode(str_id: str, path_to_json: str) -> str:
    result = ''
    try:
        with open(path_to_json) as js_read:
            opened_json = json.load(js_read)
            result = str(opened_json[str_id])
    except OSError as e:
        print(e)
    return result


async def format_quotes_from_list(quotes_list: List[str]) -> List[str]:
    quotes = [x.replace(' (', "©").replace(")", "") for x in quotes_list]
    result = [quote for quote in quotes]
    return result


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id,
                               'Привет, я бот Филонема👋. Моё имя образовано от двух слов - философия и синема(кино).',
                               reply_markup=keyboards_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nt.me/PhilonemaBot')


@dp.message_handler(commands='Инструкция')
async def manual(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Функционал бота", callback_data='manual0'))
    keyboard.add(types.InlineKeyboardButton(text="Раздел цитаты", callback_data='manual1'))
    keyboard.add(types.InlineKeyboardButton(text="Раздел кино", callback_data='manual2'))
    keyboard.add(types.InlineKeyboardButton(text="Раздел литература", callback_data='manual3'))
    keyboard.add(types.InlineKeyboardButton(text="Раздел курс философии", callback_data='manual4'))
    keyboard.add(types.InlineKeyboardButton(text="Раздел словарь", callback_data='manual5'))
    keyboard.add(types.InlineKeyboardButton(text="Раздел общая информация", callback_data='manual6'))
    await message.answer("Инструкция бота\n", reply_markup=keyboard)

@dp.callback_query_handler(text=['manual0', 'manual1', 'manual2', 'manual3', 'manual4', 'manual5', 'manual6'])
async def manual_catch(call: types.CallbackQuery):
    if call.data == 'manual0':
        mes = 'Функционал бота\nБот создан для нужд киноклуба «Философия кино», а также для помощи студентам в изучении дисциплины «Философия». С его помощью вы можете: \n1. Получить случайную цитату или стихотворение (нажмите кнопку «/Цитаты» на клавиатуре в нижней части экрана);\n2. Ознакомиться со списком фильмов, рассмотренных или планируемых к рассмотрению киноклубом, а также посмотреть каждый по приложенной ссылке, оценить его или написать рецензию (нажмите кнопку «/Кино» на клавиатуре в нижней части экрана);\n3. Ознакомиться со списком литературы, полезной для углубленного погружения в предмет, а также скачать любую книгу по приложенной ссылке (нажмите кнопку «/Литература» на клавиатуре в нижней части экрана);\n4. Получить краткие заметки по всем темам, рассматриваемым в течение курса философии (нажмите кнопку «/Курс_философии» на клавиатуре в нижней части экрана);\n5. Получить информацию о разработчиках бота и списке использованной литературы, а также ссылку на чат киноклуба (нажмите кнопку «/Общая_информация» на клавиатуре в нижней части экрана);\n6. Воспользоваться встроенным словарем философских терминов и понятий (нажмите кнопку «/Словарь» на клавиатуре в нижней части экрана)'
        await call.message.answer(mes)
    elif call.data == 'manual1':
        mes = 'Раздел цитаты\nДля получения случайной цитаты или стихотворения выберите интересующую вас тему, нажав одну из кнопок под сообщением.'
        if call.from_user.id in list(ADMINS.keys()):
            mes += '\nЕсли вы хотите добавить новую цитату или стихотворение, нажмите кнопку «Добавить новую цитату», затем выберите категорию, далее сначала отправьте боту сообщение с текстом цитаты, которую вы хотите добавить, а после еще одно с автором этой цитаты. Если вы хотите добавить еще одну цитату или получить случайную, нажмите кнопку «/Цитаты» в нижней части экрана.'
        await call.message.answer(mes)
    elif call.data == 'manual2':
        mes = 'Раздел кино\nДля получения информации о фильме, сначала выберите режиссера, фильм или фильмы которого вас интересуют, нажав одну из кнопок под этим сообщением, далее выберите один из фильмов выбранного режиссера, нажав одну из кнопок под появившимся сообщением. Если вы хотите оценить фильм, нажмите соответствующую кнопку под сообщением с информацией о фильме и следуйте подсказкам в следующих сообщениях. Если вы хотите оставить рецензию, нажмите соответствующую кнопку под сообщением с информацией о фильме, отправьте боту сообщение с текстом рецензии, и нажмите кнопку «Сохранить».  Чтобы просмотреть прошедшие модерацию рецензии, нажмите кнопку «Показать рецензии» под сообщением с информацией о фильме, после чего вы увидите автора и текст первой рецензии. Чтобы посмотреть следующую рецензию, нажмите соответствующую кнопку, чтобы прекратить просмотр рецензий – кнопку «Назад».'
        if call.from_user.id in list(ADMINS.keys()):
            mes += '\nЧтобы модерировать рецензии, нажмите соответствующую кнопку под сообщением с информацией о фильме, вам будет показана первая нерассмотренная вами рецензия. Чтобы принять или отклонить ее, нажмите соответствующую кнопку под сообщением с текстом рецензии, далее вы увидите сообщение об успешности операции. Чтобы посмотреть следующую рецензию, нажмите кнопку «Продолжить», чтобы прекратить и вернуться – кнопку «Назад».'
        await call.message.answer(mes)
    elif call.data == 'manual3':
        mes = 'Раздел литература\nЧтобы получить ссылку на скачивание интересующей вас книги, сначала выберите нужную вам категорию при помощи кнопок под сообщением, затем в списке кнопок с названиями книг найдите нужную вам, пользуясь кнопками навигации «Назад» и «Вперед», при нажатии которых вам будет показана соответственно предыдущая или следующая часть списка книг в выбранной категории.'
        await call.message.answer(mes)
    elif call.data == 'manual4':
        mes = 'Раздел курс философии\nЧтобы получить заметку на интересующую вас тему, сначала выберите нужный вам раздел курса философии при помощи кнопок под сообщением, пользуясь кнопками навигации «Назад» и «Вперед», при нажатии которых вам будет показана соответственно предыдущая или следующая часть списка разделов курс, затем в списке кнопок с названиями тем выбранного раздела выберите нужную вам тему.'
        await call.message.answer(mes)
    elif call.data == 'manual5':
        mes = 'Раздел словарь\nЧтобы получить определение слова, нажмите на кнопку «Ввести фразу», после чего отправьте боту сообщение с термином, определение которого вам нужно. '
        await call.message.answer(mes)
    elif call.data == 'manual6':
        mes = 'Раздел общая информация\nДля получения ссылки на чат киноклуба нажмите на кнопку «Киноклуб “Философия кино”» под сообщением. Для получения ссылок на использованную литературу нажмите на кнопку «Список литературы» под сообщением. Для получения информации о разработчиках бота нажмите на кнопку «Разработчики бота» под сообщением'
        await call.message.answer(mes)






@dp.message_handler(commands=['Кино', "Цитаты", "Курс_философии", "Литература", 'Общая_информация'])
async def give_category(message: types.Message):
    if message.text == '/Кино':
        await give_cinema(message)
    elif message.text == '/Цитаты':
        await give_quote(message)
    elif message.text == '/Курс_философии':
        await give_course(message)
    elif message.text == '/Литература':
        await give_literature(message)
    else:
        await give_info(message)


@dp.message_handler(commands=['Кино'])
async def give_cinema(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    directors = set(CinemaCard.cinema_cards_base['Режиссер'])
    if message.from_user.id in list(ADMINS.keys()):
        keyboard.add(types.InlineKeyboardButton(text='Добавить карточку фильма', callback_data='add_card'))
    for i in directors:
        callback_data = await asyncio.create_task(callback_encode('director|',
                                                                  f'{i}|{message.from_user.id}',
                                                                  TEMP_ID_PATH))
        keyboard.add(types.InlineKeyboardButton(text=i, callback_data=callback_data))
    _ = "В этом разделе можно найти информацию о фильмах, рассмотренных или планируемых к рассмотрению нашим киноклубом"
    __ = 'Выберите режиссера, фильмы которого вас интересуют'
    await message.answer(text=f'{_}.\n{__}:', reply_markup=keyboard)


global temp_film_info
global temp_delete_message
global temp_review_info
global temp_review_message
fields = ('название', 'режиссера', 'реперные точки', 'ссылку')


@dp.callback_query_handler(text='add_card')
async def input_name(call: types.CallbackQuery):
    await Form_films.card.set()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Отменить ввод", callback_data="cancel_input_card"))
    global temp_film_info
    temp_film_info = []
    await call.message.edit_text(f"Введите название фильма:", reply_markup=keyboard)


class Form_films(StatesGroup):
    card = State()
    director = State()
    timecodes = State()
    link = State()


@dp.callback_query_handler(text='cancel_input_card', state=[Form_films.card, Form_films.director,
                                                            Form_films.timecodes, Form_films.link])
async def cancel_input_card(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('Ввод отменен, пожалуйста, выберите категорию при помощи клавиатуры внизу экрана.')


@dp.message_handler(state=Form_films.card)
async def input_author(message: types.Message, state: FSMContext):
    await state.finish()
    global temp_film_info
    temp_film_info.append(message.text)
    await message.delete()
    await Form_films.director.set()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Отменить ввод", callback_data="cancel_input_card"))
    global temp_delete_message
    temp_delete_message = await message.answer(f"Введите режиссера:", reply_markup=keyboard)


@dp.message_handler(state=Form_films.director)
async def input_timecodes(message: types.Message, state: FSMContext):
    await state.finish()
    global temp_film_info
    temp_film_info.append(message.text)
    await message.delete()
    await Form_films.timecodes.set()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Отменить ввод", callback_data="cancel_input_card"))
    global temp_delete_message
    temp_delete_message = await message.answer(f"Введите реперные точки:", reply_markup=keyboard)


@dp.message_handler(state=Form_films.timecodes)
async def input_link(message: types.Message, state: FSMContext):
    await state.finish()
    global temp_film_info
    temp_film_info.append(message.text)
    await message.delete()
    await Form_films.link.set()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Отменить ввод", callback_data="cancel_input_card"))
    global temp_delete_message
    temp_delete_message = await message.answer(f"Введите ссылку:", reply_markup=keyboard)


@dp.message_handler(state=Form_films.link)
async def accept_quote_and_author(message: types.Message, state: FSMContext):
    await state.finish()
    global temp_delete_message
    await temp_delete_message.delete()
    global temp_film_info
    temp_film_info.append(message.text)
    film = CinemaCard.add_card_to_csv(temp_film_info[0], temp_film_info[1], temp_film_info[2], temp_film_info[3])
    text = f'{film.name}\n{film.director}\n{film.timecodes}\nСсылка на просмотр фильма: {film.link}'
    await message.answer(text)
    await message.delete()


@dp.callback_query_handler(lambda call: True if re.fullmatch(r'director\|[^|]*', call.data) else False)
async def give_films(call: types.CallbackQuery):
    callback_id = call.data
    data = await asyncio.create_task(callback_decode(callback_id, TEMP_ID_PATH))
    *_, director, user_id = data.split('|')
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    films = set(CinemaCard.cinema_cards_base['Название'].loc[CinemaCard.cinema_cards_base['Режиссер'] == director])
    for i in films:
        callback_data = await asyncio.create_task(callback_encode('film|',
                                                                  f'{user_id}|{i}|{director}',
                                                                  TEMP_ID_PATH))
        keyboard.add(types.InlineKeyboardButton(text=i, callback_data=callback_data))
    await call.message.answer(text=f'Выберите фильм режиссера {director}', reply_markup=keyboard)


@dp.callback_query_handler(lambda call: True if re.fullmatch(r'rate\|[^|]*', call.data) else False)
async def rate_beginning(call: types.CallbackQuery):
    callback_id = call.data
    data = await asyncio.create_task(callback_decode(callback_id, TEMP_ID_PATH))
    callback_data = await asyncio.create_task(callback_encode('rate proc|', f'{data}|', TEMP_ID_PATH))
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Продолжить', callback_data=callback_data))
    text = 'Вам будут предложены 8 категорий, по каждой из которых можно поставить оценку от 1 до 10'
    await call.message.answer(text=text, reply_markup=keyboard)


@dp.callback_query_handler(lambda call: True if re.fullmatch(r'film\|[^|]*', call.data) else False)
async def give_film_card(call: types.CallbackQuery):
    callback_id = call.data
    data = await asyncio.create_task(callback_decode(callback_id, TEMP_ID_PATH))
    user_id, film_name, director = data.split('|')
    user_id = int(user_id)
    film = await asyncio.create_task(CinemaCard.get_card_from_csv(film_name, director))
    callback_keys = {'Оценить фильм': 'rate', 'Оставить рецензию': 'leave review', 'Показать рецензии': 'show reviews'}
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    data = f'{user_id}|{film_name}|{director}'
    if user_id in list(ADMINS.keys()):
        data_reviews = f'{data}|0'
        callback_data = await asyncio.create_task(callback_encode('moderate|', data_reviews, TEMP_ID_PATH))
        keyboard.add(types.InlineKeyboardButton(text='Модерировать рецензии',
                                                callback_data=callback_data))
    for i in callback_keys.keys():
        if i == 'Показать рецензии':
            data_reviews = f'{data}|0'
            callback_data = await asyncio.create_task(
                callback_encode(f'{callback_keys[i]}|', data_reviews, TEMP_ID_PATH))
        else:
            callback_data = await asyncio.create_task(callback_encode(f'{callback_keys[i]}|', data, TEMP_ID_PATH))
        keyboard.add(types.InlineKeyboardButton(text=i, callback_data=callback_data))
    text = f'{film.name}\n{film.director}\n{film.timecodes}\nСсылка на просмотр фильма: {film.link}'
    rating = f'Оценки:\n'
    for i in film.rating.keys():
        rating = f'{rating}{i}: {film.rating[i]}\n'
    await call.message.answer(text=f'{text}\n{rating}', reply_markup=keyboard)


class FormReview(StatesGroup):
    text = State()
    author = State()


@dp.callback_query_handler(
    lambda call: True if re.fullmatch(r'leave review\|[^|]*', call.data) else False)
async def input_review(call: types.CallbackQuery):
    await FormReview.text.set()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Отменить ввод", callback_data="cancel_input_review"))
    await call.message.edit_text(f"Введите рецензию:", reply_markup=keyboard)
    global temp_review_info
    temp_review_info = call.data

@dp.callback_query_handler(text='cancel_input_review', state=[FormReview.text, FormReview.author])
async def cancel_input_review(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('Ввод отменен, пожалуйста, выберите категорию при помощи клавиатуры внизу экрана.')

@dp.message_handler(state=FormReview.text)
async def input_text(message: types.Message, state: FSMContext):
    await state.finish()
    global temp_review_info
    data = await asyncio.create_task(callback_decode(temp_review_info, TEMP_ID_PATH))
    data = data.split('|')
    data.append(message.text)
    temp_review_info = data
    await message.delete()
    await FormReview.author.set()
    return_callback_data = await asyncio.create_task(callback_encode('film|',
                                                                     f'{temp_review_info[0]}|{temp_review_info[1]}|'
                                                                     f'{temp_review_info[2]}',
                                                                     TEMP_ID_PATH))
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text="Сохранить", callback_data=f"save_new_review"),
        types.InlineKeyboardButton(text="Отмена", callback_data=return_callback_data))
    await message.answer(
        f"Окончательный вид рецензии:\n{message.text}\nСохранить данную рецензию?",
        reply_markup=keyboard)


@dp.callback_query_handler(text='save_new_review', state=FormReview.author)
async def save_new_review(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    global temp_review_info
    film = await CinemaCard.get_card_from_csv(temp_review_info[1], temp_review_info[2])
    film.add_review_to_csv(temp_review_info[0], temp_review_info[3], CinemaCard.path_to_unseen_reviews)
    await call.message.edit_text('Рецензия успешно сохранена!')
    temp_review_info = []


@dp.callback_query_handler(text='cancel_save_review', state=FormReview.author)
async def cancel_save_review(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    global temp_review_info
    temp_review_info = []
    await call.message.edit_text('Рецензия не сохранена!')


@dp.callback_query_handler(
    lambda call: True if re.fullmatch(r'show reviews\|[^|]*', call.data) else False)
async def show_reviews(call: types.CallbackQuery):
    data = await asyncio.create_task(callback_decode(call.data, TEMP_ID_PATH))
    user_id, film_name, director, iteration = data.split('|')
    iteration = int(iteration)
    film = await asyncio.create_task(CinemaCard.get_card_from_csv(film_name, director))
    return_callback_data = await asyncio.create_task(callback_encode('film|',
                                                                     f'{user_id}|{film_name}|{director}',
                                                                     TEMP_ID_PATH))
    next_callback_data = await asyncio.create_task(callback_encode('show reviews|',
                                                                   f'{user_id}|{film_name}|{director}|{iteration + 1}',
                                                                   TEMP_ID_PATH))
    try:
        id_, text = film.get_next_applied_review(iteration)
    except IndexError:
        end_keyboard = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text='Назад',
                                                                                   callback_data=return_callback_data))
        await call.message.answer(text=f'Больше рецензий нет.', reply_markup=end_keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(text='Показать следующую',
                                                callback_data=next_callback_data),
                     types.InlineKeyboardButton(text='Назад',
                                                callback_data=return_callback_data))
        await call.message.answer(text=f'Рецензия пользователя {id_}:\n{text}', reply_markup=keyboard)


@dp.callback_query_handler(lambda call: True if re.fullmatch(r'rate proc\|[^|]*', call.data) else False)
async def rate_processing(call: types.CallbackQuery):
    callback_id = call.data
    data = await asyncio.create_task(callback_decode(callback_id, TEMP_ID_PATH))
    user_id, film_name, director, rates = data.split('|')
    user_id = int(user_id)
    categories = ('Философская глубина',
                  'Острота постановки проблемы',
                  'Наличие категориального аппарата',
                  'Эстетическое удовольствие',
                  'Насколько берет за душу',
                  'Раскрытие мировоззрения автора',
                  'Художественная глубина',
                  'Общее впечатление')
    length = len(rates)
    if length == 8:
        text = 'Ваши оценки:\n'
        for i in categories:
            text = f'{text}{i}: {int(rates[categories.index(i)]) + 1}\n'
        callback_data = await asyncio.create_task(callback_encode('rate apply|',
                                                                  f'{user_id}|{film_name}|{director}|{rates}',
                                                                  TEMP_ID_PATH))
        retry_callback_data = await asyncio.create_task(callback_encode('rate proc|',
                                                                        f'{user_id}|{film_name}|{director}|',
                                                                        TEMP_ID_PATH))
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(text='Продолжить', callback_data=callback_data),
                     types.InlineKeyboardButton(text='Выставить заново',
                                                callback_data=retry_callback_data))
        await call.message.answer(text=text, reply_markup=keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        for i in range(10):
            callback_data = await asyncio.create_task(callback_encode('rate proc|',
                                                                      f'{user_id}|{film_name}|{director}|{rates}{i}',
                                                                      TEMP_ID_PATH))
            keyboard.add(types.InlineKeyboardButton(text=f'{i + 1}', callback_data=callback_data))
        await call.message.answer(text=f'{categories[length]}', reply_markup=keyboard)


@dp.callback_query_handler(lambda call: True if re.fullmatch(r'rate apply\|[^|]*', call.data) else False)
async def rate_apply(call: types.CallbackQuery):
    callback_id = call.data
    data = await asyncio.create_task(callback_decode(callback_id, TEMP_ID_PATH))
    user_id, film_name, director, rates = data.split('|')
    int_rates = [int(x) + 1 for x in rates]
    film = await asyncio.create_task(CinemaCard.get_card_from_csv(film_name, director))
    film.add_rating(int_rates)
    await call.message.answer(text='Оценка успешно добавлена!')


@dp.callback_query_handler(lambda call: True if re.fullmatch(r'moderate\|[^|]*', call.data) else False)
async def moderate_reviews(call: types.CallbackQuery):
    data = await asyncio.create_task(callback_decode(call.data, TEMP_ID_PATH))
    user_id, film_name, director, iteration, *_ = data.split('|')
    iteration = int(iteration)
    film = await asyncio.create_task(CinemaCard.get_card_from_csv(film_name, director))
    return_callback_data = await asyncio.create_task(callback_encode('film|',
                                                                     f'{user_id}|{film_name}|{director}',
                                                                     TEMP_ID_PATH))
    try:
        id_, text = film.get_next_unseen_review(iteration)
        apply_callback_data = await asyncio.create_task(callback_encode('apply|',
                                                                        f'{user_id}|{film_name}|{director}'
                                                                        f'|{iteration}|{id_}',
                                                                        TEMP_ID_PATH))
        decline_callback_data = await asyncio.create_task(callback_encode('decline|',
                                                                          f'{user_id}|{film_name}|{director}'
                                                                          f'|{iteration}|{id_}',
                                                                          TEMP_ID_PATH))
    except IndexError as e:
        end_keyboard = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text='Назад',
                                                                                   callback_data=return_callback_data))
        await call.message.answer(text=f'Больше рецензий нет.', reply_markup=end_keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(text='Одобрить рецензию и показать следующую',
                                                callback_data=apply_callback_data),
                     types.InlineKeyboardButton(text='Отклонить рецензию и показать следующую',
                                                callback_data=decline_callback_data),
                     types.InlineKeyboardButton(text='Назад', callback_data=return_callback_data))
        await call.message.answer(text=f'Рецензия пользователя {id_}:\n{text}', reply_markup=keyboard)


@dp.callback_query_handler(lambda call: True if re.fullmatch(r'apply\|[^|]*|decline\|[^|]*', call.data) else False)
async def apply_or_decline_review(call: types.CallbackQuery):
    _, data = call.data.split('|')
    data = await asyncio.create_task(callback_decode(f'{_}|{data}', TEMP_ID_PATH))
    user_id, film_name, director, iteration, id_ = data.split('|')
    iteration = int(iteration)
    film = await asyncio.create_task(CinemaCard.get_card_from_csv(film_name, director))
    if _ == 'apply':
        await asyncio.create_task(film.apply_review(id_))
    else:
        await asyncio.create_task(film.decline_review(id_))
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    callback_data = await asyncio.create_task(callback_encode('moderate|',
                                                              f'{user_id}|{film_name}|{director}'
                                                              f'|{iteration + 1}',
                                                              TEMP_ID_PATH))
    keyboard.add(types.InlineKeyboardButton(text='Продолжить',
                                            callback_data=callback_data))
    await call.message.answer(text=f'Успешно!', reply_markup=keyboard)


@dp.message_handler(commands=["Цитаты"])
async def give_quote(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text="Любая цитата", callback_data="quotes"),
                 types.InlineKeyboardButton(text="Цитата о кино", callback_data="quotesCinema"),
                 types.InlineKeyboardButton(text="Стихи", callback_data="quotesPoem"),
                 types.InlineKeyboardButton(text="Русская культура", callback_data="quotesRussian"))
    if message.from_user.id in list(ADMINS.keys()):
        keyboard.add(types.InlineKeyboardButton(text="Добавить новую цитату", callback_data="select_type_quote"))
    await message.answer("Выберите какую цитату вы хотите:", reply_markup=keyboard)


@dp.callback_query_handler(text='select_type_quote')
async def select_type_quote(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text="Любая цитата", callback_data="add:quotes.txt"),
                 types.InlineKeyboardButton(text="Цитата о кино", callback_data="add:quotesCinema.txt"),
                 types.InlineKeyboardButton(text="Русская культура", callback_data="add:quotesRussian.txt"))
    await call.message.edit_text("Выберите категорию для добавления цитаты:", reply_markup=keyboard)


@dp.callback_query_handler(
    text=['add:quotes.txt', 'add:quotesCinema.txt', 'add:quotesPoem.txt', 'add:quotesRussian.txt'])
async def input_quote(call: types.CallbackQuery):
    await Form.quote.set()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Отменить ввод", callback_data="cancel_input"))
    await call.message.edit_text(f"Введите цитату:", reply_markup=keyboard)
    global temp_message_quote
    temp_message_quote = call


class Form(StatesGroup):
    quote = State()
    author = State()


@dp.message_handler(state=Form.quote)
async def input_author(message: types.Message, state: FSMContext):
    await state.finish()

    global temp_message_quote
    await temp_message_quote.message.edit_text(f"Содержание цитаты:\n{message.text}")  # <-- Here we get the name
    temp_message_quote.message.text = message.text

    await message.delete()

    await Form.author.set()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Отменить ввод", callback_data="cancel_input"))

    global temp_delete_message
    temp_delete_message = await message.answer(f"Введите автора цитаты:", reply_markup=keyboard)


@dp.message_handler(state=Form.author)
async def accept_quote_and_author(message: types.Message, state: FSMContext):
    await state.finish()

    global temp_delete_message
    await temp_delete_message.delete()

    global temp_message_quote
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text="Сохранить", callback_data=f"save_new_quote"),
        types.InlineKeyboardButton(text="Отмена", callback_data="cancel_save_quote"))
    await temp_message_quote.message.edit_text(
        f"Окончательный вид цитаты:\n{temp_message_quote.message.text}©{message.text}\nСохранить данную цитату?",
        reply_markup=keyboard)
    temp_message_quote.message.text = f'{temp_message_quote.message.text} ({message.text})'

    await message.delete()


@dp.callback_query_handler(text='save_new_quote')
async def save_new_quote(call: types.CallbackQuery, state: FSMContext):
    global temp_message_quote
    await append_to_file(f'\n{temp_message_quote.message.text}', temp_message_quote.data.split(':')[1], 'quotes')
    await temp_message_quote.message.edit_text('Цитата успешно сохранена!')
    temp_message_quote = ''


@dp.callback_query_handler(text='cancel_save_quote')
async def cancel_save_quote(call: types.CallbackQuery, state: FSMContext):
    global temp_message_quote
    await temp_message_quote.message.edit_text(f'{temp_message_quote.message.text}\nЦитата не сохранена!')
    temp_message_quote = ''


@dp.callback_query_handler(text=["quotes", 'quotesCinema', 'quotesRussian', 'quotesPoem'])
async def send_quotes(call: types.CallbackQuery):
    type_of_quote = call.data
    if type_of_quote == 'quotesPoem':
        authors_and_quotes = await open_file(name=f'{type_of_quote}.txt', directory_in_resources='quotes', sep='<new>')
        quotes = await format_quotes_from_list(authors_and_quotes)
    else:
        authors_and_quotes = await open_file(name=f'{type_of_quote}.txt', directory_in_resources='quotes', sep='\n')
        quotes = await format_quotes_from_list(authors_and_quotes)
    random_count = random.randint(0, len(quotes) - 1)
    await call.message.answer(quotes[random_count])


@dp.callback_query_handler(text='cancel_input', state=[Form.quote, Form.author])
async def send_quotes(call: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()

    try:
        global temp_delete_message
        await temp_delete_message.delete()
    except NameError as e:
        print(e)

    global temp_message_quote
    await temp_message_quote.message.edit_text('Добавление цитаты отменено.')
    temp_message_quote = ''


@dp.message_handler(commands=['Словарь'])
async def give_category(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Ввести фразу", callback_data="word_input"))
    await bot.send_message(message.from_user.id,
                           'Этот словарь📖 может кратко раскрыть значения терминов из философии. Просто нажми кнопку ниже👇 и введи слово или предложение, например спроси что такое схоластика❓',
                           reply_markup=keyboard)


class Form_Dict(StatesGroup):
    word = State()


@dp.callback_query_handler(text='word_input')
async def word_input(call: types.CallbackQuery):
    await Form_Dict.word.set()

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Отменить ввод", callback_data="cancel_input_word"))
    global temp_delete_message
    temp_delete_message = await call.message.edit_text(f"Введите слово или предложение:", reply_markup=keyboard)


def read_dictionary_csv(temp_list_path):
    frame_temp = pd.read_csv(temp_list_path, header=None)
    temp = frame_temp.values.tolist()
    list_temp = []
    for i in range(len(temp)):
        list_temp.append(temp[i][0])
    return list_temp


def normalize_input(input_words):
    tokens = word_tokenize(input_words, language="russian")
    lemma_tokens = []
    for word in tokens:
        p = morph.parse(word)[0]
        if p.tag.POS in ['NOUN', 'COMP', 'VERB', 'INTJ', 'INFN', 'PRTF', 'PRTS', 'NUMR', 'ADVB', 'PREP', 'CONJ', 'PRED',
                         'PRCL', 'ADJF', 'ADJS', 'GRND', 'NPRO']:
            lemma_tokens.append(p.normal_form)
    return lemma_tokens


async def search_in_dict(input_words, message):
    normal_words = normalize_input(input_words)
    dictionary = read_dictionary_csv('resources/dictionary/dictionary1.csv')
    meanings = read_dictionary_csv('resources/dictionary/meanings1.csv')
    presentation = read_dictionary_csv('resources/dictionary/presentation1.csv')
    is_in_dict = False
    for word in normal_words:
        if word in dictionary:
            is_in_dict = True
            await message.answer(
                f'Что я нашёл😌📚\n{presentation[dictionary.index(word)].strip()} - {meanings[dictionary.index(word)].strip()}')
    if not is_in_dict:
        await message.answer(
            'К сожалению, по этому запросу я ничего не смог найти😔, но вы можете попробовать найти другие слова или предложения📕')


@dp.message_handler(state=Form_Dict)
async def give_word_from_dict(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer(f"Вы ввели:\n{message.text}")
    await search_in_dict(message.text, message)
    await temp_delete_message.delete()
    await message.delete()


@dp.callback_query_handler(text='cancel_input_word', state=[Form_Dict.word])
async def send_quotes(call: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()

    try:
        global temp_delete_message
        await temp_delete_message.edit_text('Ввод слова или предложения отменен.')
    except NameError as e:
        print(e)


@dp.message_handler(commands=["Курс_философии"])
async def give_course(message: types.Message):
    await give_course_pages(message, DEFAULT_PAGES_PARAMS, 'os.listdir:' + PHILOSOPHY_COURSE_PATH)


async def give_course_pages(call, page_params, attribute_and_path):
    keyboard = types.InlineKeyboardMarkup()
    attribute = attribute_and_path.split(':')[0]
    path = attribute_and_path.split(':')[1]
    # для работы не с os.listdir вставить ниже другой функционал чтения list(который надо разбить на странички)
    if attribute == 'os.listdir':
        selected_themes = os.listdir(path)[page_params[0]:page_params[1]]
    # c == course philo, l == literature
    elif attribute in ['c', 'l']:
        if attribute == 'c':
            package = 'philosophy_course'
        elif attribute == 'l':
            package = 'literature'
        theme = await open_file(path, package, '<new>')
        selected_themes = []
        urls = []
        for i in theme:
            temp = i.split('\n')
            selected_themes.append(temp[0])
            if attribute == 'l':
                urls.append(temp[1])
        selected_themes = selected_themes[page_params[0]:page_params[1]]
        if attribute == 'l':
            urls = urls[page_params[0]:page_params[1]]
        print('selected', selected_themes)
    else:
        print('incorrect attribute')
        return

    if len(selected_themes) < 1:
        await call.answer(text='Больше страниц нет!', show_alert=True)
        return

    for theme_path in selected_themes:
        if attribute == 'os.listdir':
            print(theme_path)
            keyboard.add(types.InlineKeyboardButton(text=os.path.splitext(theme_path)[0], callback_data=theme_path))
        if attribute == 'c':
            print('c', theme_path)
            keyboard.add(types.InlineKeyboardButton(text=theme_path, callback_data=theme_path))
    if attribute == 'l':
        for i in range(len(urls)):
            keyboard.add(types.InlineKeyboardButton(text=selected_themes[i], url=urls[i]))

    page = int(page_params[0] / DEFAULT_PAGES_PARAMS[1])

    keyboard.add(
        types.InlineKeyboardButton(text='Назад',
                                   callback_data=await callback_encode('LCQ:', f'p:{page}:{attribute}:{path}',
                                                                       TEMP_ID_PATH)),
        types.InlineKeyboardButton(text='Вперед',
                                   callback_data=await callback_encode('LCQ:', f'n:{page}:{attribute}:{path}',
                                                                       TEMP_ID_PATH)))
    print(f'p:{page}:{attribute}:{path}')
    print('размер', utf8len(f'p:{page}:{attribute}:{path}'))

    if type(call) != types.CallbackQuery:
        # в данном случае call это переданный message
        await call.answer(text="Выберите тему:", reply_markup=keyboard)
    else:
        try:
            heading = os.path.splitext(path)[0]
            if attribute == 'os.listdir':
                heading = "Выберите тему"
            await call.message.edit_text(text=heading + ':', reply_markup=keyboard)
        except aiogram.utils.exceptions.ButtonDataInvalid as e:
            print(e)


def utf8len(s):
    return len(s.encode('utf-8'))


def change_page_params(page):
    return [DEFAULT_PAGES_PARAMS[1] * page, DEFAULT_PAGES_PARAMS[1] * page + DEFAULT_PAGES_PARAMS[1]]


async def course_previous_next(call):
    print(call.data)
    print(await callback_decode(call.data, TEMP_ID_PATH))

    call_data_dec = await callback_decode(call.data, TEMP_ID_PATH)
    pressed_button = call_data_dec.split(':')[0]
    page = int(call_data_dec.split(':')[1])
    # ниже переписать нормально
    path_directory = call_data_dec.split(':')[2] + ':' + call_data_dec.split(':')[3]
    if pressed_button == 'n':
        page += 1
        await give_course_pages(call, change_page_params(page), path_directory)
        return

    if pressed_button == 'p':
        if page > 0:
            page -= 1
            await give_course_pages(call, change_page_params(page), path_directory)
        else:
            await call.answer(text='Больше страниц нет!', show_alert=True)
        return


def get_header(theme: str):
    header = theme.split('\n')[0]
    return header


@dp.message_handler(commands="Литература")
async def give_literature(message: types.Message):
    await give_course_pages(message, DEFAULT_PAGES_PARAMS, 'os.listdir:' + LITERATURE_COURSE_PATH)


@dp.message_handler(commands="Общая_информация")
async def give_info(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="🎬Киноклуб \"Философия кино\"", callback_data="cinema_club"))
    keyboard.add(types.InlineKeyboardButton(text="🧑‍💻👩‍💻Разработчики бота", callback_data="developers"))
    keyboard.add(types.InlineKeyboardButton(text="Список литературы📚", callback_data="list_of_literature"))
    await message.answer("Общая_информация:", reply_markup=keyboard)


@dp.callback_query_handler(text="cinema_club")
async def cinema_club(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text="Вступить в 🎬Киноклуб", url="https://t.me/studactiv_znatie_samgtu/242"))
    await call.message.answer(
        "При поддержке Студактива \"Знание\" СамГТУ, был открыт Киноклуб \"Философия кино\", который ведет активную жизнь под руководством д.ф.н. В.Б.Малышева.",
        reply_markup=keyboard)


@dp.callback_query_handler(text="developers")
async def developers(call: types.CallbackQuery):
    await call.message.answer(
        "Данный бот был разработан студентами СамГТУ 2-ИАИТ-109😎\nСпециально для Студактива \"Знание\", Киноклуба \"Философия кино\"\nУчастники и разработчики:\n👉Бартенев А.В\n👉Авдошин М.А\n👉Малышев М.А.\n👉Мурыгин Д.А.\n👉Строкин И.А\n👉Пасюга А.А.\n👉Ермолин К.П.\n👉Рябова Д.А\n👉Плюхин В.К.")


@dp.callback_query_handler(text="list_of_literature")
async def list_of_literature(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Античная философия",
                                            url='https://spravochnick.ru/filosofiya/istoriya_zapadnoy_filosofii/antichnaya_filosofiya/periody_razvitiya_antichnoy_filosofii/#osnovnye-periody-razvitiya-antichnoy-filosofii'))
    keyboard.add(types.InlineKeyboardButton(text="Экзистенцианализм", url='https://lifehacker.ru/ekzistencializm/'))
    keyboard.add(types.InlineKeyboardButton(text="Постмодернизм", url='https://bigenc.ru/philosophy/text/3162376'))

    await call.message.answer('Список литературы📚:', reply_markup=keyboard)


@dp.callback_query_handler()
async def catch_all_callbacks(call: types.CallbackQuery):
    if call.data.split(':')[0] == 'LCQ':
        # print('catch', call.data)
        await course_previous_next(call)
        return

    if call.data in os.listdir(PHILOSOPHY_COURSE_PATH):
        await give_philo_topics(call)
        return

    if call.data in os.listdir(LITERATURE_COURSE_PATH):
        await give_lit_topics(call)
        return

    await give_text_and_picture(call)


async def give_philo_topics(call):
    print('def philo topic', call.data)
    theme_file = call.data
    attribute = 'c'
    # ниже переписать недочеты
    await give_course_pages(call, DEFAULT_PAGES_PARAMS, f'{attribute}:{theme_file}')


async def give_lit_topics(call):
    print('def lit topic', call.data)
    theme_file = call.data
    attribute = 'l'
    # ниже переписать недочеты
    await give_course_pages(call, DEFAULT_PAGES_PARAMS, f'{attribute}:{theme_file}')


async def give_text_and_picture(call):
    print('give text and picture')
    for theme_name in os.listdir(PHILOSOPHY_COURSE_PATH):
        theme = await open_file(theme_name, 'philosophy_course', '<new>')
        for topic in theme:
            if call.data == get_header(topic):
                try:
                    path = f'resources/pictures/{call.data.strip()}.png'
                    photo = open(path, 'rb')
                    await call.message.answer_photo(photo, caption=topic)
                except:
                    try:
                        print("Слишком большой caption")
                        path = f'resources/pictures/{call.data.strip()}.png'
                        photo = open(path, 'rb')
                        await call.message.answer_photo(photo)
                        await call.message.answer(topic)
                    except:
                        print("Не нашёл картинку")
                        await call.message.answer(topic)

def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(manual, commands=['Инструкция'])
    dp.register_message_handler(give_category, commands=['Цитаты', 'Курс_философии', 'Литература', 'Общая_информация',
                                                         'Кино', 'Словарь'])
