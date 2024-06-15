from typing import Union
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
import requests, datetime
import logging
from aiogram.types import CallbackQuery, message
from aiogram import executor, types
from aiogram.utils import callback_data, executor

from start_bot import bot, dp
from markups import items_kb, keyboards, menu_cd, buy_item, start_kb

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message = None, *args, **kwargs):

    """
    This handler will be called when user sends `/start` or `/help` command
    """
    global CHAT_ID
    CHAT_ID = message.from_user.id
    if message:
        markup = await keyboards['0']()
        await bot.send_message(
            chat_id = CHAT_ID,
            text = f"""
Здравствуйте, {message.from_user.first_name}, это каталог магазина DETAL TRAFIC. 

Время работы: 
Пн - Пт - с 9:00 до 18:00, 
Сб - с 9:00 до 12:00, 
Вс - выходной.

Телефоны: 
(067) 308-75-45, 
(099) 304-73-13, 
(073) 440-23-34 
            """,
            reply_markup = markup
            )

async def start_kb(callback: types.CallbackQuery, *args, **kwargs):
    markup = await keyboards['0']()
    await callback.message.edit_reply_markup(markup)

async def list_main_categories(callback: types.CallbackQuery, *args, **kwargs):
    markup = await keyboards['1'](callback)
    await callback.message.edit_reply_markup(markup)

async def list_subcategories(callback: types.CallbackQuery, main_category_id: str, *args, **kwargs):
    markup = await keyboards['2'](callback, main_category_id = main_category_id)
    await callback.message.edit_reply_markup(markup)

async def list_sections(callback: types.CallbackQuery, subcategory_id: str, main_category_id: str, *args, **kwargs):
    markup = await keyboards['3'](callback, subcategory_id = subcategory_id, main_category_id = main_category_id)
    await callback.message.edit_reply_markup(markup)

async def list_items(callback: types.CallbackQuery, section_id: str, subcategory_id: str, *args, **kwargs):
    markup = await items_kb(callback, section_id, subcategory_id)
    await callback.message.edit_reply_markup(markup)

@dp.callback_query_handler(menu_cd.filter())
async def navigate(callback: types.CallbackQuery, callback_data: dict):

    level = callback_data.get('level')
    main_category = callback_data.get('main_category')
    subcategory = callback_data.get('subcategory')
    sections = callback_data.get('section')
    items = callback_data.get('item')

    levels = {
        '0': start_kb,
        '1': list_main_categories,
        '2': list_subcategories,
        '3': list_sections,
        '4': list_items,
    }



    level_func = levels[level]

    await level_func(
        callback = callback,
        main_category_id = main_category,
        subcategory_id = subcategory,
        section_id = sections,
        items_id = items,

    )

@dp.callback_query_handler(buy_item.filter())
async def buy(callback: types.CallbackQuery, callback_data: dict):

    item_id = callback_data.get('item_id')

    await callback.message.reply(f'buy {item_id}')

@dp.message_handler()
async def delete_products(message):
    await message.reply(text='a')

if __name__ == "__main__":
    executor.start_polling(dp)


