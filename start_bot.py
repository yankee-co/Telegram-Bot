from aiogram import Bot, Dispatcher

TOKEN = "1963004307:AAFUE6pU-Jw9pkoXsPNLViV82jRR8Hgxe0g"
REQUEST_LINK = f"https://api.telegram.org/bot{TOKEN}/"
CHAT_ID = None

bot = Bot(TOKEN)
dp = Dispatcher(bot)