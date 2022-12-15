from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

b1 = KeyboardButton('/Зачем_ты_нужен?')
b2 = KeyboardButton('/Цитаты')
b3 = KeyboardButton('/Курс_философии')

keyboards_client = ReplyKeyboardMarkup(resize_keyboard=True)
keyboards_client.add(b1).add(b2).add(b3)

