from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/Зачем_ты_нужен?')
b2 = KeyboardButton('/Цитата_о_кино')
b3 = KeyboardButton('/Любая_цитата')


keyboards_client = ReplyKeyboardMarkup(resize_keyboard=True)

keyboards_client.add(b1).add(b2).add(b3)