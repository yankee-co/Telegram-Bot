import os

from aiogram import Bot, Dispatcher

TOKEN = os.environ["BOT_TOKEN"]
REQUEST_LINK = f"https://api.telegram.org/bot{TOKEN}/"
CHAT_ID = None

bot = Bot(TOKEN)
dp = Dispatcher(bot)