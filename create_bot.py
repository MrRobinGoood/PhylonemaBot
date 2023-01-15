from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

from aiogram.utils import executor

# token=os.getenv('TOKEN')
fake_token = '5822945704:AAHpJ8CZSR6V8DBKaaLT7aGPzRGABzcM0Dk'
bot = Bot(fake_token)
    #Bot('5780044264:AAE2YbGLalI5yCGKvwivObCt7mq4OLahu0s')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

