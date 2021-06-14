import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.db_api.postgresql import Users, Files, Sponsors

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

loop = asyncio.get_event_loop()

db_users = loop.run_until_complete(Users.create())
db_files = loop.run_until_complete(Files.create())
db_sponsors = loop.run_until_complete(Sponsors.create())
