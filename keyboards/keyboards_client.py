from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

b0 = KeyboardButton('/Кино')
b1 = KeyboardButton('/Зачем_ты_нужен?')
b2 = KeyboardButton('/Цитаты')
b3 = KeyboardButton('/Курс_философии')
b4 = KeyboardButton('/Литература')
b5 = KeyboardButton('/Общая_информация')

keyboards_client = ReplyKeyboardMarkup(resize_keyboard=True)
keyboards_client.add(b0).add(b1).add(b2, b4).add(b3).add(b5)

