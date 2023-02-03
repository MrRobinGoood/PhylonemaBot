from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

b0 = KeyboardButton('/Кино')
b1 = KeyboardButton('/Инструкция')
b2 = KeyboardButton('/Цитаты')
b3 = KeyboardButton('/Курс_философии')
b4 = KeyboardButton('/Литература')
b5 = KeyboardButton('/Общая_информация')
b6 = KeyboardButton('/Словарь')

keyboards_client = ReplyKeyboardMarkup(resize_keyboard=True)
keyboards_client.add(b1).add(b2, b0, b4).add(b3,b6).add(b5)

