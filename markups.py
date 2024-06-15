from aiogram.bot import bot
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.update import Update
from aiogram.utils import callback_data
from aiogram.utils.callback_data import CallbackData

from db_commands import get_main_categories, get_subcategories, get_sections, get_items
from start_bot import bot

menu_cd = CallbackData('show_menu', 'level', 'main_category', 'subcategory', 'section' ,'item', 'limit')
buy_item = CallbackData('buy', 'item_id')

# CALLBACK DATA CONSTRUCTOR

def make_callback_data(level, main_category='0', subcategory='0', section = '0', item='0', limit='0'):
    return menu_cd.new(
        level = level,
        main_category = main_category,
        subcategory = subcategory,
        section = section,
        item = item,
        limit = limit
    )

# START KEYBOARD



async def start_kb(*args, **kwargs):

    CURRENT_LEVEL = 0

    start_markup = InlineKeyboardMarkup(row_width=1).insert(
        InlineKeyboardButton(text='Ознакомиться с каталогом', callback_data=make_callback_data(level = CURRENT_LEVEL + 1))
    )

    return start_markup


# MAIN CATEGORIES KEYBOARD

async def main_categories_kb(callback, *args):
    
    CURRENT_LEVEL = 1

    categories = await get_main_categories()

    markup = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)

    for category in categories:
        
        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1,
            main_category=category['id']
        )
        
        markup.add(
            InlineKeyboardButton(
                text = category['name'],
                callback_data = callback_data
                )
            )

    markup.row(
        InlineKeyboardButton(
            text = '▸ Назад ◂',
            callback_data = make_callback_data(level=CURRENT_LEVEL-1)
            )
        )

    return markup

# SUBCATEGORIES KEYBOARD

async def subcategories_kb(callback, main_category_id: str, *args):
    
    CURRENT_LEVEL = 2
    
    subcategories = await get_subcategories(main_category_id = main_category_id)
    markup = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)

    for subcategory in subcategories:
        
        callback_data = make_callback_data(
            level = CURRENT_LEVEL + 1,
            main_category = main_category_id,
            subcategory = subcategory['id']
        )
        
        markup.add(
            InlineKeyboardButton(
                text = subcategory['name'],
                callback_data = callback_data
                )
            )

    markup.row(
        InlineKeyboardButton(
            text = '▸ Назад ◂',
            callback_data = make_callback_data(level=CURRENT_LEVEL-1, main_category=main_category_id)
            )
        )

    return markup

# SECTIONS KEYBOARD

async def sections_kb(callback, subcategory_id: str, main_category_id: str, *args):

    CURRENT_LEVEL = 3

    sections = await get_sections(subcategory_id = subcategory_id)

    markup = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)

    for section in sections:
        
        callback_data = make_callback_data(
            level = CURRENT_LEVEL + 1,
            subcategory = subcategory_id,
            section = section['section_id']
        )
        
        markup.add(
            InlineKeyboardButton(
                text = section['section_name'],
                callback_data = callback_data
                )
            )
        
    markup.row(
        InlineKeyboardButton(
            text = '▸ Назад ◂',
            callback_data = make_callback_data(level=CURRENT_LEVEL-1, main_category=main_category_id)
            )
        )

    return markup

# PRODUCTS KEYBOARD

async def items_kb(callback, section_id: str, subcategory_id: str, *args):
    CURRENT_LEVEL = 4
    chat_id = callback['from']['id']
    products = await get_items(section_id = section_id)

    markup = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    limit = len(products)
    for product in products:

        chat_id = callback['from']['id']
        await bot.send_photo(
            chat_id=chat_id,
            photo=product['product_photo'],
            caption="{}\n\n{}\n\n{}".format(
                product['product_title'],
                product['product_description'],
                product['product_price'],
                ),
            reply_markup=InlineKeyboardMarkup(resize_keyboard=True, row_width=1).row(
                InlineKeyboardButton(
                    text = 'Купить',
                    callback_data = buy_item.new(
                        item_id = product['product_id']
                    )
                )
            )
        )

        # await bot.send_message(chat_id=chat_id, text=f'{Update.message.message_id}')
        
    markup.row(
        InlineKeyboardButton(
            text = '▸ Назад ◂',
            callback_data = make_callback_data(level=CURRENT_LEVEL-1, subcategory=subcategory_id, limit = limit)
            )
        )
    return markup

keyboards = {
    '0': start_kb,
    '1': main_categories_kb,
    '2': subcategories_kb,
    '3': sections_kb,
    '4': items_kb,
    }
