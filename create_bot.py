from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

from aiogram.utils import executor

# token=os.getenv('TOKEN')
bot = Bot('5347751121:AAGIRh30ozMqnwZEDqVUOqmbWeB5gfHBdZk')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

