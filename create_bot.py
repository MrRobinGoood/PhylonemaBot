from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

from aiogram.utils import executor

# token=os.getenv('TOKEN')
bot = Bot('')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

