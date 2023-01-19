import os

from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import keyboards_client
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import random
from typing import List

# Значения: [С какого файла(строки) начинать, Сколько файлов(inline кнопок) выводить]
DEFAULT_PAGES_PARAMS = [0, 5]
PHILOSOPHY_COURSE_PATH = 'resources/philosophy_course'


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


# themes_and_files = {'Эпоха Марксизма': 'Эпоха Марксизма.txt',
#                     'Древняя Индия и Китай': 'Древняя Индия и Китай.txt',
#                     'Гуманизм, Молот Ведьм, Эразм': 'Гуманизм, Молот Ведьм, Эразм.txt',
#                     'Русская философия': 'Русская философия.txt',
#                     'Позитивизм': 'Позитивизм.txt'}

literature_and_files = {'Общество и общественные отношения': 'obchestvo_i_obsch_otnoshenia.txt',
                        'Мироустройство': 'miroustroystvo.txt',
                        'Cogito ergo sum': 'cogito ergo sum.txt',
                        'Самоопределение и самопознание': 'samoopredelenie_i_samopoznanie.txt'}


# @dp.message_handler()
# async def echo_send(message: types.Message):
#     if message.from_user.id == 828256665:
#         await bot.send_message(1048347854,message.text)
#     if message.from_user.id == 1048347854:
#         await bot.send_message(828256665,message.text)

@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id,
                               'Привет, я бот Филонема👋. Моё имя образовано от двух слов - философия и синема(кино).',
                               reply_markup=keyboards_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nt.me/PhilonemaBot')


@dp.message_handler(commands=["Цитаты", "Курс_философии", "Литература", 'Общая_информация'])
async def give_category(message: types.Message):
    if message.text == '/Цитаты':
        await give_quote(message)
    elif message.text == '/Курс_философии':
        await give_course(message)
    elif message.text == '/Литература':
        await give_literature(message)
    else:
        await give_info(message)


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
    random_count = random.randint(0, len(quotes) - 1)
    await call.message.answer(quotes[random_count])


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
    elif attribute == '<new>':
        print('path', path)
        print('1',os.path.split(path)[1])
        print('0',os.path.split(path)[0])
        theme = await open_file(os.path.split(path)[1], os.path.split(path)[0], attribute)
        selected_themes = []
        for i in theme:
            temp = i.split('\n')
            selected_themes.append(temp[0])
        selected_themes = selected_themes[page_params[0]:page_params[1]]
        print('selected', selected_themes)
    else:
        print('incorrect attribute')
        return

    if len(selected_themes) < 1:
        await call.answer(text='Больше страниц нет!', show_alert=True)
        return

    for theme_path in selected_themes:
        print('theme_path',theme_path)
        print('splitext',os.path.splitext(theme_path)[0])
        keyboard.add(types.InlineKeyboardButton(text=os.path.splitext(theme_path)[0], callback_data=theme_path))

    page = int(page_params[0] / DEFAULT_PAGES_PARAMS[1])
    print('длина',len(f'gcp:{page}:{attribute}:{path}'))
    print('длина', len(f'gcn:{page}:{attribute}:{path}'))
    keyboard.add(
        types.InlineKeyboardButton(text='Назад', callback_data=f'gcp:{page}:{attribute}:{path}'),
        types.InlineKeyboardButton(text='Вперед', callback_data=f'gcn:{page}:{attribute}:{path}'))
    if type(call) != types.CallbackQuery:
        # в данном случае call это переданный message
        await call.answer(text="Выберите тему:", reply_markup=keyboard)
    else:
        await call.message.edit_text(text="Выберите тему:", reply_markup=keyboard)


def change_page_params(page):
    return [DEFAULT_PAGES_PARAMS[1] * page, DEFAULT_PAGES_PARAMS[1] * page + DEFAULT_PAGES_PARAMS[1]]


async def course_previous_next(call):
    pressed_button = call.data.split(':')[0]
    page = int(call.data.split(':')[1])
    # ниже переписать нормально
    path_directory = call.data.split(':')[2] + ':' + call.data.split(':')[3]
    print('between', path_directory)
    if pressed_button == 'gcn':
        print('next')
        page += 1
        await give_course_pages(call, change_page_params(page), path_directory)
        return

    if pressed_button == 'gcp':
        print('prev')
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
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Общество и общественные отношения",
                                            callback_data="Общество и общественные отношения"))
    keyboard.add(types.InlineKeyboardButton(text="Мироустройство", callback_data="Мироустройство"))
    keyboard.add(types.InlineKeyboardButton(text="Cogito ergo sum", callback_data="Cogito ergo sum"))
    keyboard.add(types.InlineKeyboardButton(text="Самоопределение и самопознание",
                                            callback_data="Самоопределение и самопознание"))
    await message.answer(text="Выберите тему:", reply_markup=keyboard)


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
        "Данный бот был разработан студентами СамГТУ 2-ИАИТ-109😎\nСпециально для Студактива \"Знание\", Киноклуба \"Философия кино\"\nУчастники и разработчики:\n👉Бартенев А.В\n👉Пасюга А.А.\n👉Ермолин К.П.\n👉Строкин И.А\n👉Малышев М.А.\n👉Мурыгин Д.А.\n👉Рябова Д.А\n👉Авдошин М.А")


@dp.callback_query_handler()
async def catch_all_callbacks(call: types.CallbackQuery):
    if call.data.split(':')[0] in ['gcp', 'gcn']:
        print('catch', call.data)
        await course_previous_next(call)
        return

    if call.data in os.listdir(PHILOSOPHY_COURSE_PATH):
        await give_topics(call)
        return

    await give_text_and_picture(call)


async def give_topics(call):
    print('def topic', call.data)
    keyboard = types.InlineKeyboardMarkup()
    theme_file = call.data
    attribute = '<new>'
    package = 'philosophy_course'

    # theme = await open_file(theme_file, 'philosophy_course', '<new>')
    # ниже переписать недочеты
    await give_course_pages(call, DEFAULT_PAGES_PARAMS, f'{attribute}:{package}/{theme_file}')
    # for i in theme:
    #     temp = i.split('\n')
    #     # вот тут бывает ошибка, если файл пустой и нельзя вывести кнопки(ошибка что нельзя не давать текст инлайн кнопкам)
    #     keyboard.add(types.InlineKeyboardButton(text=temp[0], callback_data=temp[0]))
    # await call.message.answer(f"{os.path.splitext(call.data)[0]}:", reply_markup=keyboard)


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


# admins = {828256665:'Бартенев Андрей', 1144869308:'Авдошин Максим',1048347854:'Василиса'}
# @dp.message_handler()
# async def why_need(message: types.Message):
#     # функционал для админов
#     if message.from_user.id in list(admins.keys()):
#         await bot.send_message(message.from_user.id, 'Ты админ')
#         return
#     # функционал для юзеров
#     await bot.send_message(message.from_user.id, 'Ты холоп')


def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(why_need, commands=['Зачем_ты_нужен?'])
    dp.register_message_handler(give_category, commands=['Цитаты', 'Курс_философии', 'Литература', 'Общая_информация'])
