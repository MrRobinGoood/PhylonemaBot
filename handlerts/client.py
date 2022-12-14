import random

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor

from create_bot import dp, bot
from keyboards import keyboards_client

file = open("resources/quotes.txt",mode="r",encoding="utf8")
res = file.read().split('\n')
file.close()
quotes = res[::2]
authors = res[1::2]

file2 = open("resources/quotesCinema.txt",mode="r",encoding="utf8")
res2 = file2.read().split('\n')
for i in range(len(res2)):
    res2[i] = res2[i].replace(' (',"©")
    res2[i] =  res2[i].replace(")","")
file2.close()


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id,'Привет, я бот Филонема👋. Моё имя образовано от двух слов - философия и синема(кино).', reply_markup=keyboards_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nt.me/PhilonemaBot')


@dp.message_handler(commands=['Зачем_ты_нужен?'])
async def why_need(message: types.Message):
        await bot.send_message(message.from_user.id,'Пока что я и сам точно не знаю, это философский вопрос🤔')

@dp.message_handler(commands=['Любая_цитата'])
async def give_quotes(message: types.Message):
    random_count = random.randint(0, len(quotes))
    await bot.send_message(message.from_user.id,quotes[random_count] + "©" + authors[random_count])

@dp.message_handler(commands=['Цитата_о_кино'])
async def give_cinema_quotes(message: types.Message):
    random_count = random.randint(0, len(res2))
    await bot.send_message(message.from_user.id, res2[random_count])

@dp.message_handler(commands=['Любая_цитата'])
async def give_quotes(message: types.Message):
    random_count = random.randint(0, len(quotes))
    await bot.send_message(message.from_user.id,quotes[random_count] + "©" + authors[random_count])



def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(why_need, commands=['Зачем_ты_нужен?'])
    dp.register_message_handler(give_cinema_quotes, commands=['Цитата_о_кино'])
    dp.register_message_handler(give_quotes, commands=['Любая_цитата'])


