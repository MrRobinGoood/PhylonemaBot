from aiogram import types, Dispatcher
import random
from create_bot import dp, bot
from keyboards import keyboards_client
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# 1-й вариант
urlkb = InlineKeyboardMarkup(row_width=1)
urlButton = InlineKeyboardButton(text='Древний Китай',
                                 url='https://docs.google.com/document/d/1fL2rhhblCS6OqZdSYf_omd2ER4NGqpOxSC34YrixMhc/edit')
urlButton2 = InlineKeyboardButton(text='Новый Китай',
                                  url='https://docs.google.com/document/d/1fL2rhhblCS6OqZdSYf_omd2ER4NGqpOxSC34YrixMhc/edit')
urlkb.add(urlButton, urlButton2)

file = open("resources/quotes.txt", mode="r", encoding="utf8")
res = file.read().split('\n')
file.close()
quotes = res[::2]
authors = res[1::2]

file2 = open("resources/quotesCinema.txt", mode="r", encoding="utf8")
res2 = file2.read().split('\n')
for i in range(len(res2)):
    res2[i] = res2[i].replace(' (', "©")
    res2[i] = res2[i].replace(")", "")
file2.close()

file3 = open("resources/Epokha_Marxizma_i_vytekayuschikh_iz_nego_techeniy.txt", mode="r", encoding="utf8")
theme1 = file3.read().split('<new>')
for i in range(len(theme1)):
    theme1[i] = theme1[i].strip()
file3.close()

file4 = open("resources/Drevnyaya_India_i_Kitay.txt", mode="r", encoding="utf8")
theme2 = file4.read().split('<new>')
for i in range(len(theme2)):
    theme2[i] = theme2[i].strip()
file4.close()

file5 = open("resources/Gumanizm_Molot_Vedm_Erazm.txt", mode="r", encoding="utf8")
theme3 = file5.read().split('<new>')
for i in range(len(theme3)):
    theme3[i] = theme3[i].strip()
file5.close()

file6 = open("resources/Russkaya_filosofia.txt", mode="r", encoding="utf8")
theme4 = file6.read().split('<new>')
for i in range(len(theme4)):
    theme4[i] = theme4[i].strip()
file6.close()

file7 = open("resources/Pozitsivizm.txt", mode="r", encoding="utf8")
theme5 = file7.read().split('<new>')
for i in range(len(theme5)):
    theme5[i] = theme5[i].strip()
file7.close()




@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id,
                               'Привет, я бот Филонема👋. Моё имя образовано от двух слов - философия и синема(кино).',
                               reply_markup=keyboards_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nt.me/PhilonemaBot')


@dp.message_handler(commands='ссылки')
async def url_command(message: types.Message):
    await message.answer('Полезные ссылки:', reply_markup=urlkb)


@dp.message_handler(commands="Цитаты")
async def give_quotes(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Любая цитата", callback_data="quotes")).add(
        types.InlineKeyboardButton(text="Цитата о кино", callback_data="cinema_quotes"))
    await message.answer("Выберите какую цитату вы хотите:", reply_markup=keyboard)


@dp.callback_query_handler(text="quotes")
async def send_quotes(call: types.CallbackQuery):
    random_count = random.randint(0, len(quotes))
    await call.message.answer(quotes[random_count] + "©" + authors[random_count])


@dp.callback_query_handler(text="cinema_quotes")
async def send_cinema_quotes(call: types.CallbackQuery):
    random_count = random.randint(0, len(res2))
    await call.message.answer(res2[random_count])


@dp.message_handler(commands="Курс_философии")
async def give_quotes(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Эпоха Марксизма и вытекающих из него течений", callback_data="topic1"))
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

# path = 'resources/' + call.data.lower().strip() + '.jpg'
# photo = open(path, 'rb')
# await call.message.answer_photo(photo, caption=theme1[i])
@dp.callback_query_handler()
async def lasten(call: types.CallbackQuery):
    for i in range(len(theme1)):
        if call.data == get_headers(theme1)[i]:
            await call.message.answer(theme1[i])
    for i in range(len(theme2)):
        if call.data == get_headers(theme2)[i]:
            await call.message.answer(theme2[i])
    for i in range(len(theme3)):
        if call.data == get_headers(theme3)[i]:
            await call.message.answer(theme3[i])
    for i in range(len(theme4)):
        if call.data == get_headers(theme4)[i]:
            await call.message.answer(theme4[i])
    for i in range(len(theme5)):
        if call.data == get_headers(theme5)[i]:
            await call.message.answer(theme5[i])

@dp.message_handler(commands=['Зачем_ты_нужен?'])
async def why_need(message: types.Message):
    await bot.send_message(message.from_user.id, 'Пока что я и сам точно не знаю, это философский вопрос🤔')


def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(why_need, commands=['Зачем_ты_нужен?'])
    dp.register_message_handler(give_quotes, commands=['Цитаты'])
    dp.register_message_handler(give_quotes, commands=['Курс_философии'])
