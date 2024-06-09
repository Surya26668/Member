from pytz import timezone
from logging import ERROR
from telebot import logger
from telebot.asyncio_filters import *
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage

owner = 1038305176
whitelist = {}
datetime_format = f"%H:%M:%S %d-%m-%Y"
wib = timezone('Asia/Jakarta')
bot_token = '6946010945:AAHKgdRw27gy8guQsLiS7V00g6v8BaIcTPY'
bot = AsyncTeleBot(bot_token, parse_mode='HTML', state_storage=StateMemoryStorage())

bot.add_custom_filter(StateFilter(bot))
bot.add_custom_filter(IsDigitFilter())

logger.setLevel(ERROR)