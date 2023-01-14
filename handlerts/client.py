from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import keyboards_client
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import random
from typing import List


async def open_file(name: str, directory_in_resourses: str, sep: str) -> List:
    try:
        with open(f'resourses/{directory_in_resourses}/{name}') as opened_file:
            result = [x.strip() for x in opened_file.read().split(sep)]
            return result
    except OSError as e:
        print(e)


async def format_quotes_from_list(quotes_list: List[str]) -> List[str]:
    quotes= quotes_list[::2]
    authors = [x.replace(' (', "©").replace(")", "") for x in quotes_list[1::2]]
    quotes = zip(quotes, authors)
    result = [f'{quote[0]} {quote[1]}' for quote in quotes]
    return result

file3 = open("resources/philosophy_course/Epokha_Marxizma_i_vytekayuschikh_iz_nego_techeniy.txt", mode="r",
             encoding="utf8")
theme1 = file3.read().split('<new>')
for i in range(len(theme1)):
    theme1[i] = theme1[i].strip()
file3.close()

file4 = open("resources/philosophy_course/Drevnyaya_India_i_Kitay.txt", mode="r", encoding="utf8")
theme2 = file4.read().split('<new>')
for i in range(len(theme2)):
    theme2[i] = theme2[i].strip()
file4.close()

file5 = open("resources/philosophy_course/Gumanizm_Molot_Vedm_Erazm.txt", mode="r", encoding="utf8")
theme3 = file5.read().split('<new>')
for i in range(len(theme3)):
    theme3[i] = theme3[i].strip()
file5.close()

file6 = open("resources/philosophy_course/Russkaya_filosofia.txt", mode="r", encoding="utf8")
theme4 = file6.read().split('<new>')
for i in range(len(theme4)):
    theme4[i] = theme4[i].strip()
file6.close()

file7 = open("resources/philosophy_course/Pozitsivizm.txt", mode="r", encoding="utf8")
theme5 = file7.read().split('<new>')
for i in range(len(theme5)):
    theme5[i] = theme5[i].strip()
file7.close()

file = open("resources/literature/obchestvo_i_obsch_otnoshenia.txt", mode="r", encoding="utf8")
lit1 = file.read().split('<new>')
for i in range(len(lit1)):
    lit1[i] = lit1[i].strip()
file.close()

file = open("resources/literature/miroustroystvo.txt", mode="r", encoding="utf8")
lit2 = file.read().split('<new>')
for i in range(len(lit2)):
    lit2[i] = lit2[i].strip()
file.close()

file = open("resources/literature/cogito ergo sum.txt", mode="r", encoding="utf8")
lit3 = file.read().split('<new>')
for i in range(len(lit3)):
    lit3[i] = lit3[i].strip()
file.close()
file = open("resources/literature/samoopredelenie_i_samopoznanie.txt", mode="r", encoding="utf8")
lit4 = file.read().split('<new>')
for i in range(len(lit4)):
    lit4[i] = lit4[i].strip()
file.close()


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id,
                               'Привет, я бот Филонема👋. Моё имя образовано от двух слов - философия и синема(кино).',
                               reply_markup=keyboards_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nt.me/PhilonemaBot')


@dp.message_handler(commands="Цитаты")
async def give_quotes(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Любая цитата", callback_data="quotes")).add(
        types.InlineKeyboardButton(text="Цитата о кино", callback_data="cinema_quotes"))
    await message.answer("Выберите какую цитату вы хотите:", reply_markup=keyboard)


@dp.callback_query_handler(text="quotes")
async def send_quotes(call: types.CallbackQuery):
    authors_and_quotes = await open_file(name='quotes', directory_in_resourses='quotes', sep='\n')
    quotes = await format_quotes_from_list(authors_and_quotes)
    random_count = random.randint(0, len(quotes))
    await call.message.answer(quotes[random_count])


#TODO: выяснить, как избавиться от одинаковости send_quotes и send_cinema_quotes
@dp.callback_query_handler(text="cinema_quotes")
async def send_cinema_quotes(call: types.CallbackQuery):
    authors_and_quotes = await open_file(name='quotesCinema', directory_in_resourses='quotes', sep='\n')
    quotes = await format_quotes_from_list(authors_and_quotes)
    random_count = random.randint(0, len(quotes))
    await call.message.answer(quotes[random_count])


@dp.message_handler(commands="Курс_философии")
async def give_quotes(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Эпоха Марксизма", callback_data="topic1"))
    keyboard.add(types.InlineKeyboardButton(text="Древняя Индия и Китай", callback_data="topic2"))
    keyboard.add(types.InlineKeyboardButton(text="Гуманизм, Молот Ведьм, Эразм", callback_data="topic3"))
    keyboard.add(types.InlineKeyboardButton(text="Русская философия", callback_data="topic4"))
    keyboard.add(types.InlineKeyboardButton(text="Позицивизм", callback_data="topic5"))
    await message.answer("Выберите тему:", reply_markup=keyboard)


def get_headers(theme):
    headers = []
    for i in range(len(theme)):
        temp = theme[i].split('\n')
        headers.append(temp[0])
    return headers


@dp.callback_query_handler(text="topic1")
async def topic1(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(theme1)):
        temp = theme1[i].split('\n')
        keyboard.add(types.InlineKeyboardButton(text=temp[0], callback_data=temp[0]))
    await call.message.answer("Эпоха Марксизма и вытекающих из него течений:", reply_markup=keyboard)


@dp.callback_query_handler(text="topic2")
async def topic2(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(theme2)):
        temp = theme2[i].split('\n')
        keyboard.add(types.InlineKeyboardButton(text=temp[0], callback_data=temp[0]))
    await call.message.answer("Древняя Индия и Китай:", reply_markup=keyboard)


@dp.callback_query_handler(text="topic3")
async def topic3(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(theme3)):
        temp = theme3[i].split('\n')
        keyboard.add(types.InlineKeyboardButton(text=temp[0], callback_data=temp[0]))
    await call.message.answer("Гуманизм, Молот Ведьм, Эразм:", reply_markup=keyboard)


@dp.callback_query_handler(text="topic4")
async def topic4(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(theme4)):
        temp = theme4[i].split('\n')
        keyboard.add(types.InlineKeyboardButton(text=temp[0], callback_data=temp[0]))
    await call.message.answer("Русская философия:", reply_markup=keyboard)


@dp.callback_query_handler(text="topic5")
async def topic5(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(theme5)):
        temp = theme5[i].split('\n')
        keyboard.add(types.InlineKeyboardButton(text=temp[0], callback_data=temp[0]))
    await call.message.answer("Позицивизм:", reply_markup=keyboard)


@dp.message_handler(commands="Литература")
async def give_quotes(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Общество и общественные отношения", callback_data="litrature1"))
    keyboard.add(types.InlineKeyboardButton(text="Мироустройство", callback_data="litrature2"))
    keyboard.add(types.InlineKeyboardButton(text="Cogito ergo sum", callback_data="litrature3"))
    keyboard.add(types.InlineKeyboardButton(text="Самоопределение и самопознание", callback_data="litrature4"))
    await message.answer("Выберите тему:", reply_markup=keyboard)


@dp.callback_query_handler(text="litrature1")
async def literature1(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(lit1)):
        temp = lit1[i].split('\n')
        keyboard.add(types.InlineKeyboardButton(text=temp[0], url=temp[1]))
    await call.message.answer("Общество и общественные отношения:", reply_markup=keyboard)


@dp.callback_query_handler(text="litrature2")
async def literature1(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(lit2)):
        temp = lit2[i].split('\n')
        keyboard.add(types.InlineKeyboardButton(text=temp[0], url=temp[1]))
    await call.message.answer("Мироустройство:", reply_markup=keyboard)


@dp.callback_query_handler(text="litrature3")
async def literature1(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(lit3)):
        temp = lit3[i].split('\n')
        keyboard.add(types.InlineKeyboardButton(text=temp[0], url=temp[1]))
    await call.message.answer("Cogito ergo sum:", reply_markup=keyboard)


@dp.callback_query_handler(text="litrature4")
async def literature1(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(lit4)):
        temp = lit4[i].split('\n')
        keyboard.add(types.InlineKeyboardButton(text=temp[0], url=temp[1]))
    await call.message.answer("Самоопределение и самопознание:", reply_markup=keyboard)


@dp.message_handler(commands="Общая_информация")
async def give_quotes(message: types.Message):
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
async def lasten(call: types.CallbackQuery):
    for i in range(len(theme1)):
        if call.data == get_headers(theme1)[i]:
            try:
                path = 'resources/pictures/' + call.data.strip() + '.png'
                photo = open(path, 'rb')
                await call.message.answer_photo(photo, caption=theme1[i])
            except:
                try:
                    print("Слишком большой caption")
                    path = 'resources/pictures/' + call.data.strip() + '.png'
                    photo = open(path, 'rb')
                    await call.message.answer_photo(photo)
                    await call.message.answer(theme1[i])
                except:
                    print("Не нашёл картинку")
                    await call.message.answer(theme1[i])

    for i in range(len(theme2)):
        if call.data == get_headers(theme2)[i]:
            try:
                path = 'resources/pictures/' + call.data.strip() + '.png'
                photo = open(path, 'rb')
                await call.message.answer_photo(photo, caption=theme2[i])
            except:
                try:
                    print("Слишком большой caption")
                    path = 'resources/pictures/' + call.data.strip() + '.png'
                    photo = open(path, 'rb')
                    await call.message.answer_photo(photo)
                    await call.message.answer(theme2[i])
                except:
                    print("Не нашёл картинку")
                    await call.message.answer(theme2[i])

    for i in range(len(theme3)):
        if call.data == get_headers(theme3)[i]:
            try:
                path = 'resources/pictures/' + call.data.strip() + '.png'
                photo = open(path, 'rb')
                await call.message.answer_photo(photo, caption=theme3[i])
            except:
                try:
                    print("Слишком большой caption")
                    path = 'resources/pictures/' + call.data.strip() + '.png'
                    photo = open(path, 'rb')
                    await call.message.answer_photo(photo)
                    await call.message.answer(theme3[i])
                except:
                    print("Не нашёл картинку")
                    await call.message.answer(theme3[i])

    for i in range(len(theme4)):
        if call.data == get_headers(theme4)[i]:
            try:
                path = 'resources/pictures/' + call.data.strip() + '.png'
                photo = open(path, 'rb')
                await call.message.answer_photo(photo, caption=theme4[i])
            except:
                try:
                    print("Слишком большой caption")
                    path = 'resources/pictures/' + call.data.strip() + '.png'
                    photo = open(path, 'rb')
                    await call.message.answer_photo(photo)
                    await call.message.answer(theme4[i])
                except:
                    print("Не нашёл картинку")
                    await call.message.answer(theme4[i])

    for i in range(len(theme5)):
        if call.data == get_headers(theme5)[i]:
            try:
                path = 'resources/pictures/' + call.data.strip() + '.png'
                photo = open(path, 'rb')
                await call.message.answer_photo(photo, caption=theme5[i])
            except:
                try:
                    # print("Слишком большой caption")
                    path = 'resources/pictures/' + call.data.strip() + '.png'
                    photo = open(path, 'rb')
                    await call.message.answer_photo(photo)
                    await call.message.answer(theme5[i])
                except:
                    # print("Не нашёл картинку")
                    await call.message.answer(theme5[i])


@dp.message_handler(commands=['Зачем_ты_нужен?'])
async def why_need(message: types.Message):
    await bot.send_message(message.from_user.id, 'Пока что я и сам точно не знаю, это философский вопрос🤔')


def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(why_need, commands=['Зачем_ты_нужен?'])
    dp.register_message_handler(give_quotes, commands=['Цитаты'])
    dp.register_message_handler(give_quotes, commands=['Курс_философии'])
    dp.register_message_handler(give_quotes, commands=['Литература'])
    dp.register_message_handler(give_quotes, commands=['Общая_информация'])
