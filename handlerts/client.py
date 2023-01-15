from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import keyboards_client
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import random
from typing import List


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
                    'Древняя Индия и Китая': 'Drevnyaya_India_i_Kitay.txt',
                    'Гуманизм, Молот Ведьм, Эразм': 'Gumanizm_Molot_Vedm_Erazm.txt',
                    'Русская философия': 'Russkaya_filosofia.txt',
                    'Позитивизм': 'Pozitsivizm.txt'}

literature_and_files = {'Общество и общественные отношения': 'obchestvo_i_obsch_otnoshenia.txt',
                        'Мироустройство': 'miroustroystvo.txt',
                        'Cogito ergo sum': 'cogito ergo sum.txt',
                        'Самоопределение и самопознание': 'samoopredelenie_i_samopoznanie.txt'}


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
                    path = f'resources/pictures/{call.data}.png'
                    photo = open(path, 'rb')
                    await call.message.answer_photo(photo, caption=topic)
                except:
                    try:
                        print("Слишком большой caption")
                        path = f'resources/pictures/{call.data}.png'
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
    dp.register_message_handler(give_category, commands=['Цитаты', 'Курс_философии', 'Литература', 'Общая_информация'])
