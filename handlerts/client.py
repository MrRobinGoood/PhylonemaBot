import asyncio
import random
from typing import List
import re

from aiogram import types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import dp, bot
from keyboards import keyboards_client
from Cinema.CinemaCard import CinemaCard


async def open_file(name: str, directory_in_resources: str, sep: str) -> List:
    try:
        with open(f'resources/{directory_in_resources}/{name}', encoding='utf8') as opened_file:
            result = [x.strip() for x in opened_file.read().split(sep)]
            return result
    except OSError as e:
        print(e)


async def format_quotes_from_list(quotes_list: List[str]) -> List[str]:
    quotes = [x.replace(' (', "©").replace(")", "") for x in quotes_list]
    result = [quote for quote in quotes]
    return result

themes_and_files = {'Эпоха Марксизма': 'Epokha_Marxizma_i_vytekayuschikh_iz_nego_techeniy.txt',
                    'Древняя Индия и Китай': 'Drevnyaya_India_i_Kitay.txt',
                    'Гуманизм, Молот Ведьм, Эразм': 'Gumanizm_Molot_Vedm_Erazm.txt',
                    'Русская философия': 'Russkaya_filosofia.txt',
                    'Позитивизм': 'Pozitsivizm.txt'}

literature_and_files = {'Общество и общественные отношения': 'obchestvo_i_obsch_otnoshenia.txt',
                        'Мироустройство': 'miroustroystvo.txt',
                        'Cogito ergo sum': 'cogito ergo sum.txt',
                        'Самоопределение и самопознание': 'samoopredelenie_i_samopoznanie.txt'}
admins = {1144869308: 'Авдошин Максим'}
global new_film

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
    if message.from_user.id in list(admins.keys()):
        keyboard.add(types.InlineKeyboardButton(text='Добавить карточку фильма', callback_data='add_card'))
    for i in directors:
        keyboard.add(types.InlineKeyboardButton(text=i, callback_data=f'{i}|{message.from_user.id}'))
    _ = "В этом разделе можно найти информацию о фильмах, рассмотренных или планируемых к рассмотрению нашим киноклубом"
    __ = 'Выберите режиссера, фильмы которого вас интересуют'
    await message.answer(text=f'{_}.\n{__}:', reply_markup=keyboard)

global temp_film_info
global temp_delete_message
fields = ('название', 'режиссера', 'реперные точки', 'ссылку')


@dp.callback_query_handler(text='add_card')
async def input_name(call: types.CallbackQuery):
    await Form.card.set()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Отменить ввод", callback_data="cancel_input"))
    global temp_film_info
    temp_film_info = []
    await call.message.edit_text(f"Введите название фильма:", reply_markup=keyboard)


class Form(StatesGroup):
    card = State()
    director = State()
    timecodes = State()
    link = State()
    save = State()


@dp.message_handler(state=Form.card)
async def input_author(message: types.Message, state: FSMContext):
    await state.finish()
    global temp_film_info
    temp_film_info.append(message.text)
    await message.delete()
    await Form.director.set()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Отменить ввод", callback_data="cancel_input"))
    global temp_delete_message
    temp_delete_message = await message.answer(f"Введите автора цитаты:", reply_markup=keyboard)


@dp.message_handler(state=Form.director)
async def input_timecodes(message: types.Message, state: FSMContext):
    await state.finish()
    global temp_film_info
    temp_film_info.append(message.text)
    await message.delete()
    await Form.timecodes.set()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Отменить ввод", callback_data="cancel_input"))
    global temp_delete_message
    temp_delete_message = await message.answer(f"Введите реперные точки:", reply_markup=keyboard)


@dp.message_handler(state=Form.timecodes)
async def input_link(message: types.Message, state: FSMContext):
    await state.finish()
    global temp_film_info
    temp_film_info.append(message.text)
    await message.delete()
    await Form.link.set()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Отменить ввод", callback_data="cancel_input"))
    global temp_delete_message
    temp_delete_message = await message.answer(f"Введите ссылку:", reply_markup=keyboard)


@dp.message_handler(state=Form.link)
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
    if user_id in list(admins.keys()):
        keyboard.add(types.InlineKeyboardButton(text='Модерировать рецензии',
                                                callback_data=f'moderate|{film_name}|{director}|{user_id}'))
    keyboard.add(types.InlineKeyboardButton(text='Оценить фильм', callback_data=f'rate|{film_name}|{director}'),
                 # types.InlineKeyboardButton(text='Оставить рецензию',
                  #                          callback_data=f'leave review|{film_name}|{director}|{user_id}'),
                 types.InlineKeyboardButton(text='Показать рецензии',
                                            callback_data=f'show reviews|{film_name}|{director}|{user_id}'))
    text = f'{film.name}\n{film.director}\n{film.timecodes}\nСсылка на просмотр фильма: {film.link}'
    rating = f'Оценки:\n'
    for i in film.rating.keys():
        rating = f'{rating}{i}: {film.rating[i]}\n'
    await call.message.answer(text=f'{text}\n{rating}', reply_markup=keyboard)


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
                 types.InlineKeyboardButton(text="Цитата о кино", callback_data="quotesCinema"))
    await message.answer("Выберите какую цитату вы хотите:", reply_markup=keyboard)


@dp.callback_query_handler(text=["quotes", 'quotesCinema'])
async def send_quotes(call: types.CallbackQuery):
    type_of_quote = call.data
    authors_and_quotes = await open_file(name=f'{type_of_quote}.txt', directory_in_resources='quotes', sep='\n')
    quotes = await format_quotes_from_list(authors_and_quotes)
    random_count = random.randint(0, len(quotes)-1)
    await call.message.answer(quotes[random_count])


@dp.message_handler(commands="Курс_философии")
async def give_course(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Эпоха Марксизма", callback_data="Эпоха Марксизма"))
    keyboard.add(types.InlineKeyboardButton(text="Древняя Индия и Китай", callback_data="Древняя Индия и Китай"))
    keyboard.add(types.InlineKeyboardButton(text="Гуманизм, Молот Ведьм, Эразм",
                                            callback_data="Гуманизм, Молот Ведьм, Эразм"))
    keyboard.add(types.InlineKeyboardButton(text="Русская философия", callback_data="Русская философия"))
    keyboard.add(types.InlineKeyboardButton(text="Позитивизм", callback_data="Позитивизм"))
    await message.answer("Выберите тему:", reply_markup=keyboard)


def get_header(theme: str):
    header = theme.split('\n')[0]
    return header


@dp.callback_query_handler(text=list(themes_and_files.keys()))
async def topic(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    theme_file = themes_and_files[call.data]
    theme = await open_file(theme_file, 'philosophy_course', '<new>')
    for i in theme:
        temp = i.split('\n')
        keyboard.add(types.InlineKeyboardButton(text=temp[0], callback_data=temp[0]))
    await call.message.answer(f"{call.data}:", reply_markup=keyboard)


@dp.message_handler(commands="Литература")
async def give_literature(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Общество и общественные отношения",
                                            callback_data="Общество и общественные отношения"))
    keyboard.add(types.InlineKeyboardButton(text="Мироустройство", callback_data="Мироустройство"))
    keyboard.add(types.InlineKeyboardButton(text="Cogito ergo sum", callback_data="Cogito ergo sum"))
    keyboard.add(types.InlineKeyboardButton(text="Самоопределение и самопознание",
                                            callback_data="Самоопределение и самопознание"))
    await message.answer("Выберите тему:", reply_markup=keyboard)


@dp.callback_query_handler(text=list(literature_and_files.keys()))
async def literature(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    theme_file = literature_and_files[call.data]
    literature = await open_file(theme_file, 'literature', '<new>')
    for i in literature:
        temp = i.split('\n')
        keyboard.add(types.InlineKeyboardButton(text=temp[0], url=temp[1]))
    await call.message.answer(f"{call.data}:", reply_markup=keyboard)


@dp.message_handler(commands="Общая_информация")
async def give_info(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="🎬Киноклуб\"Философия кино\"", callback_data="cinema_club"))
    keyboard.add(types.InlineKeyboardButton(text="🧑‍💻👩‍💻Разработчики бота", callback_data="developers"))
    await message.answer("Общая_информация:", reply_markup=keyboard)


@dp.callback_query_handler(text="cinema_club")
async def cinema_club(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Вступить в 🎬Киноклуб", url="https://t.me/studactiv_znatie_samgtu/242"))
    await call.message.answer("При поддержке Студактива \"Знание\" СамГТУ, был открыт Киноклуб \"Философия кино\", который ведет активную жизнь под руководством д.ф.н. В.Б.Малышева.", reply_markup=keyboard)


@dp.callback_query_handler(text="developers")
async def developers(call: types.CallbackQuery):
    await call.message.answer("Данный бот был разработан студентами СамГТУ 2-ИАИТ-109😎\nСпециально для Студактива \"Знание\", Киноклуба \"Философия кино\"\nУчастники и разработчики:\n👉Бартенев А.В\n👉Пасюга А.А.\n👉Ермолин К.П.\n👉Строкин И.А\n👉Малышев М.А.\n👉Мурыгин Д.А.\n👉Рябова Д.А\n👉Авдошин М.А")


# path = 'resources/' + call.data.strip() + '.png'
# photo = open(path, 'rb')
# await call.message.answer_photo(photo, caption=theme1[i])
@dp.callback_query_handler()
async def give_text_and_pictures(call: types.CallbackQuery):
    for theme_name in themes_and_files.keys():
        theme = await open_file(themes_and_files[theme_name], 'philosophy_course', '<new>')
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
