from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
import psycopg2
from config import *

# Create connection func

def create_connection(host, user, password, db_name, port):
    connection = psycopg2.connect(
            host = host,
            user = user,
            password = password,
            database = db_name,
            port = port
            )

    return connection

# MAIN CATEGORIES

async def get_main_categories():
    
    try:
    
        connection = create_connection(host, user, password, db_name, port)

        with connection.cursor() as cursor:

            connection.autocommit = True

            cursor.execute(
                """
                SELECT * FROM main_categories;
                """ 
            )

            categories_list = []

            for category_tuple in cursor.fetchall():

                category = {
                    'id': category_tuple[0],
                    'name': category_tuple[2]
                }
                
                categories_list.append(category)

            return categories_list

    except Exception as _ex:
        print('Error occured: ', _ex)

    finally:
        connection.close()

    # SUBCATEGORIES

async def get_subcategories(main_category_id: str):
     
    try:
    
        connection = create_connection(host, user, password, db_name, port)

        with connection.cursor() as cursor:

            connection.autocommit = True

            cursor.execute(
            f"""
            SELECT *
            FROM subcategories
            WHERE main_category_id = {int(main_category_id)}
            """
            )

            categories_list = []

            for category_tuple in cursor.fetchall():

                category = {
                    'id': category_tuple[0],
                    'name': category_tuple[1],
                    'main_cat_id': category_tuple[2],
                    'sections': category_tuple[3]
                }
                
                categories_list.append(category)

            return categories_list

    except Exception as _ex:
        print('Error occured: ', _ex)

    finally:
        connection.close()

async def get_sections(subcategory_id: str, *args):
    try:
    
        connection = create_connection(host, user, password, db_name, port)

        with connection.cursor() as cursor:
            cursor.execute(
            f"""
            SELECT *
            FROM sections
            WHERE subcategory_id = {subcategory_id}
            """
            )
        
            sections_list = []

            for section_tuple in cursor.fetchall():
                section = {
                    'section_id': section_tuple[0],
                    'section_name': section_tuple[1],
                }
                sections_list.append(section)
            
            return sections_list



    except Exception as _ex:
        print('Error occured: ', _ex)

    finally:
        connection.close()
    
async def get_items(section_id: str, *args):
    try:
    
        connection = create_connection(host, user, password, db_name, port)

        with connection.cursor() as cursor:
            cursor.execute(
            f"""
            SELECT *
            FROM products
            WHERE section_id = {section_id}
            """
            )
        
            product_list = []

            for product_tuple in cursor.fetchall():
                product = {
                    'product_id': product_tuple[0],
                    'product_photo': product_tuple[2],
                    'product_title': product_tuple[3],
                    'product_description': product_tuple[4],
                    'product_price': product_tuple[5],
                }
                product_list.append(product)
            
            return product_list

    except Exception as _ex:
        print('Error occured: ', _ex)

    # finally:
        connection.close()