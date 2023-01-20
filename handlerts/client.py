
import asyncio
import random
from typing import List
import re


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


# Значения: [С какого файла(строки) начинать, Сколько файлов(inline кнопок) выводить]
DEFAULT_PAGES_PARAMS = [0, 5]
PHILOSOPHY_COURSE_PATH = 'resources/philosophy_course'
LITERATURE_COURSE_PATH = 'resources/literature'

ADMINS = {828256665: 'Бартенев Андрей', 1144869308: 'Авдошин Максим', 1048347854: 'Василиса'}
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
    print(message.from_user.id)
    directors = set(CinemaCard.cinema_cards_base['Режиссер'])
    if message.from_user.id in list(ADMINS.keys()):
        keyboard.add(types.InlineKeyboardButton(text='Добавить карточку фильма', callback_data='add_card'))
    for i in directors:
        keyboard.add(types.InlineKeyboardButton(text=i, callback_data=f'{i}|{message.from_user.id}'))
    _ = "В этом разделе можно найти информацию о фильмах, рассмотренных или планируемых к рассмотрению нашим киноклубом"
    __ = 'Выберите режиссера, фильмы которого вас интересуют'
    await message.answer(text=f'{_}.\n{__}:', reply_markup=keyboard)

global temp_film_info
global temp_delete_message
global temp_review_info
fields = ('название', 'режиссера', 'реперные точки', 'ссылку')


@dp.callback_query_handler(text='add_card')
async def input_name(call: types.CallbackQuery):
    await Form_films.card.set()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Отменить ввод", callback_data="cancel_input"))
    global temp_film_info
    temp_film_info = []
    await call.message.edit_text(f"Введите название фильма:", reply_markup=keyboard)


class Form_films(StatesGroup):
    card = State()
    director = State()
    timecodes = State()
    link = State()

    quote = State()
    author = State()



@dp.message_handler(state=Form_films.card)
async def input_author(message: types.Message, state: FSMContext):
    await state.finish()
    global temp_film_info
    temp_film_info.append(message.text)
    await message.delete()
    await Form_films.director.set()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Отменить ввод", callback_data="cancel_input"))
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
    keyboard.add(types.InlineKeyboardButton(text="Отменить ввод", callback_data="cancel_input"))
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
    keyboard.add(types.InlineKeyboardButton(text="Отменить ввод", callback_data="cancel_input"))
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


@dp.callback_query_handler(lambda call: True if re.fullmatch(r'[^|]*\|[^|]*', call.data) else False)
async def give_films(call: types.CallbackQuery):
    director, user_id = call.data.split('|')
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    films = set(CinemaCard.cinema_cards_base['Название'].loc[CinemaCard.cinema_cards_base['Режиссер'] == director])
    for i in films:
        keyboard.add(types.InlineKeyboardButton(text=i, callback_data=f'{i}|{call.data}'))
    await call.message.answer(text=f'Выберите фильм режиссера {director}', reply_markup=keyboard)


@dp.callback_query_handler(lambda call: True if re.fullmatch(r'[^|]*\|[^|]*\|[^|]*', call.data) else False)
async def give_film_card(call: types.CallbackQuery):
    film_name, director, user_id = call.data.split('|')
    user_id = int(user_id)
    film = await asyncio.create_task(CinemaCard.get_card_from_csv(film_name, director))
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    if user_id in list(ADMINS.keys()):
        keyboard.add(types.InlineKeyboardButton(text='Модерировать рецензии',
                                                callback_data=f'moderate|{film_name}|{director}|{user_id}'))
    keyboard.add(types.InlineKeyboardButton(text='Оценить фильм', callback_data=f'rate|{film_name}|{director}'),
                 types.InlineKeyboardButton(text='Оставить рецензию',
                                            callback_data=f'leave review|{user_id}|{film_name}|{director}'),
                 types.InlineKeyboardButton(text='Показать рецензии',
                                            callback_data=f'show reviews|{film_name}|{director}|{user_id}'))
    text = f'{film.name}\n{film.director}\n{film.timecodes}\nСсылка на просмотр фильма: {film.link}'
    rating = f'Оценки:\n'
    for i in film.rating.keys():
        rating = f'{rating}{i}: {film.rating[i]}\n'
    await call.message.answer(text=f'{text}\n{rating}', reply_markup=keyboard)


class FormReview(StatesGroup):
    text = State()
    author = State()


@dp.callback_query_handler(lambda call: True if re.fullmatch(r'leave review\|[^|]*\|[^|]*\|[^|]*', call.data) else False)
async def input_quote(call: types.CallbackQuery):
    await FormReview.text.set()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Отменить ввод", callback_data="cancel_input"))
    await call.message.edit_text(f"Введите рецензию:", reply_markup=keyboard)
    global temp_review_info
    temp_review_info = call.data.split('|')[1:]


@dp.message_handler(state=FormReview.text)
async def input_text(message: types.Message, state: FSMContext):
    await state.finish()
    global temp_review_info
    temp_review_info.append(message.text)
    await message.delete()
    await FormReview.author.set()
    global temp_delete_message
    await temp_delete_message.delete()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text="Сохранить", callback_data=f"save_new_review"),
        types.InlineKeyboardButton(text="Отмена", callback_data="cancel_save_review"))
    await temp_message_quote.message.edit_text(
        f"Окончательный вид рецензии:\n{message.text}\nСохранить данную рецензию?",
        reply_markup=keyboard)
    await message.delete()


@dp.callback_query_handler(text='save_new_review')
async def save_new_review(call: types.CallbackQuery, state: FSMContext):
    global temp_review_info
    film = await CinemaCard.get_card_from_csv(temp_review_info[1], temp_review_info[2])
    film.add_review_to_csv(temp_review_info[0], temp_review_info[4], CinemaCard.path_to_unseen_reviews)
    await call.message.edit_text('Рецензия успешно сохранена!')
    temp_review_info = []


@dp.callback_query_handler(text='cancel_save_review')
async def cancel_save_review(call: types.CallbackQuery, state: FSMContext):
    global temp_review_info
    await call.message.edit_text('Рецензия не сохранена!')
    temp_review_info = []


@dp.callback_query_handler(lambda call: True if re.fullmatch(r'show reviews\|[^|]*\|[^|]*\|[^|]*', call.data) else False)
async def show_reviews(call: types.CallbackQuery):
    *_, film_name, director, user_id = call.data.split('|')
    film = await asyncio.create_task(CinemaCard.get_card_from_csv(film_name, director))
    try:
        id_, text = film.get_next_applied_review()
    except StopIteration:
        end_keyboard = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text='Назад',
                                                        callback_data=f'{film_name}|{director}|{user_id}'))
        await call.message.answer(text=f'Больше рецензий нет.', reply_markup=end_keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(text='Показать следующую',
                                                callback_data=f'show reviews|{film_name}|{director}'),
                     types.InlineKeyboardButton(text='Назад',
                                                callback_data=f'{film_name}|{director}'))
        await call.message.answer(text=f'Рецензия пользователя{id_}:\n{text}', reply_markup=keyboard)


@dp.callback_query_handler(lambda call: True if re.fullmatch(r'rate\|[^|]*\|[^|]*', call.data) else False)
async def rate_beginning(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Продолжить', callback_data=f'{call.data}|'))
    text = 'Вам будут предложены 8 категорий, по каждой из которых можно поставить оценку от 1 до 10'
    await call.message.answer(text=text, reply_markup=keyboard)


@dp.callback_query_handler(lambda call: True if re.fullmatch(r'rate\|[^|]*\|[^|]*\|[^|]*', call.data) else False)
async def rate_processing(call: types.CallbackQuery):
    categories = ('Философская глубина',
                  'Острота постановки проблемы',
                  'Наличие категориального аппарата',
                  'Эстетическое удовольствие',
                  'Насколько берет за душу',
                  'Раскрытие мировоззрения автора',
                  'Художественная глубина',
                  'Общее впечатление')
    _, film_name, director, rates = call.data.split('|')
    length = len(rates)
    if length == 8:
        text = 'Ваши оценки:\n'
        for i in categories:
            text = f'{text}{i}: {rates[categories.index(i)]}\n'
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(text='Продолжить', callback_data=f'{call.data}|apply'),
                     types.InlineKeyboardButton(text='Выставить заново',
                                                callback_data=f'rate|{film_name}|{director}|'))
        await call.message.answer(text=text, reply_markup=keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        for i in range(10):
            keyboard.add(types.InlineKeyboardButton(text=f'{i+1}', callback_data=f'{call.data}{i}'))
        await call.message.answer(text=f'{categories[length]}', reply_markup=keyboard)


@dp.callback_query_handler(lambda call: True if re.fullmatch(r'rate\|[^|]*\|[^|]*\|[^|]*\|apply', call.data) else False)
async def rate_apply(call: types.CallbackQuery):
    _, film_name, director, rates, __ = call.data.split('|')
    int_rates = [int(x)+1 for x in rates]
    film = await asyncio.create_task(CinemaCard.get_card_from_csv(film_name, director))
    film.add_rating(int_rates)
    await call.message.answer(text='Оценка успешно добавлена!')


@dp.callback_query_handler(lambda call: True if re.fullmatch(r'moderate\|[^|]*\|[^|]*\|[^|]*', call.data) else False)
async def moderate_reviews(call: types.CallbackQuery):
    *_, film_name, director, user_id = call.data.split('|')
    film = await asyncio.create_task(CinemaCard.get_card_from_csv(film_name, director))
    try:
        id_, text = film.get_next_unseen_review()
    except StopIteration:
        end_keyboard = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text='Назад',
                                                        callback_data=f'{film_name}|{director}|{user_id}'))
        await call.message.answer(text=f'Нерассмотренных рецензий нет.', reply_markup=end_keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(text='Одобрить рецензию и показать следующую',
                                                callback_data=f'apply|{film_name}|{director}|{user_id}|{id_}'),
                     types.InlineKeyboardButton(text='Отклонить рецензию и показать следующую',
                                                callback_data=f'decline|{film_name}|{director}|{user_id}|{id_}'),
                     types.InlineKeyboardButton(text='Назад',
                                                callback_data=f'{film_name}|{director}|{user_id}'))
        await call.message.answer(text=f'Рецензия пользователя {id_}:\n{text}', reply_markup=keyboard)


@dp.callback_query_handler(lambda call: True if re.fullmatch(r'apply\|[^|]*\|[^|]*\|[^|]*\|[^|]*|decline\|[^|]*\|['
                                                             r'^|]*\|[^|]*\|[^|]*', call.data) else False)
async def apply_or_decline_review(call: types.CallbackQuery):
    _, film_name, director, user_id, id_ = call.data.split('|')
    film = await asyncio.create_task(CinemaCard.get_card_from_csv(film_name, director))
    if _ == 'apply':
        film.apply_review(id_)
    else:
        film.decline_review(id_)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text='Продолжить',
                                            callback_data=f'moderate|{film_name}|{director}|{user_id}'))
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


# class Form(StatesGroup):
#     quote = State()
#     author = State()
#     save = State()


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

    print(temp_message_quote.data)
    await temp_message_quote.message.edit_text(
        f"Окончательный вид цитаты:\n{temp_message_quote.message.text}©{message.text}\nСохранить данную цитату?",
        reply_markup=keyboard)
    temp_message_quote.message.text = f'{temp_message_quote.message.text} ({message.text})'
    print(temp_message_quote.message.text)

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
            keyboard.add(types.InlineKeyboardButton(text=os.path.splitext(theme_path)[0], callback_data=theme_path))
        if attribute == 'c':
            keyboard.add(types.InlineKeyboardButton(text=theme_path, callback_data=theme_path))
    if attribute == 'l':
        for i in range(len(urls)):
            keyboard.add(types.InlineKeyboardButton(text=selected_themes[i], url=urls[i]))

    page = int(page_params[0] / DEFAULT_PAGES_PARAMS[1])

    keyboard.add(
        types.InlineKeyboardButton(text='Назад', callback_data=f'p:{page}:{attribute}:{path}'),
        types.InlineKeyboardButton(text='Вперед', callback_data=f'n:{page}:{attribute}:{path}'))
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
            await call.message.edit_text(text=heading+':', reply_markup=keyboard)
        except aiogram.utils.exceptions.ButtonDataInvalid as e:
            print(e)


def utf8len(s):
    return len(s.encode('utf-8'))


def change_page_params(page):
    return [DEFAULT_PAGES_PARAMS[1] * page, DEFAULT_PAGES_PARAMS[1] * page + DEFAULT_PAGES_PARAMS[1]]


async def course_previous_next(call):
    pressed_button = call.data.split(':')[0]
    page = int(call.data.split(':')[1])
    # ниже переписать нормально
    path_directory = call.data.split(':')[2] + ':' + call.data.split(':')[3]
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


@dp.callback_query_handler()
async def catch_all_callbacks(call: types.CallbackQuery):
    if call.data.split(':')[0] in ['p', 'n']:
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


@dp.message_handler(commands=['Зачем_ты_нужен?'])
async def why_need(message: types.Message):
    await bot.send_message(message.from_user.id, 'Пока что я и сам точно не знаю, это философский вопрос🤔')


def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(why_need, commands=['Зачем_ты_нужен?'])
    dp.register_message_handler(give_category, commands=['Цитаты', 'Курс_философии', 'Литература', 'Общая_информация',
                                                         'Кино'])
