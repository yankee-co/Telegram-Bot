from bs4 import element
import requests
import psycopg2
import bs4
from config import *
import sys

home = 'https://detal-trafic.com.ua'
page_all = '?page=all'

headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "Content-Type": "text/html",
}

try:
    connection = psycopg2.connect(
        host = host,
        user = user,
        password = password,
        database = db_name,
        port = port
    )

    with connection.cursor() as cursor:

        connection.autocommit = True

        soup1 = bs4.BeautifulSoup(requests.get(home, headers=headers).text, 'html.parser')

        cursor.execute(
            """
            TRUNCATE TABLE main_categories CASCADE;
            TRUNCATE TABLE subcategories CASCADE;
            TRUNCATE TABLE sections CASCADE;
            TRUNCATE TABLE products CASCADE;
            """
            )

        # MAIN CATEGORIES FROM MAIN PAGE

        main_categories_li_list = soup1.find('div', id='main-categories').find('ul').find_all('li')

        for li in main_categories_li_list:
            main_category_url = home + li.a['href'] + page_all
            main_category_name = li.a.text.replace('\t', '').replace('\n', '')

            cursor.execute(
                """
                INSERT INTO main_categories(main_category_url, main_category_name)
                VALUES ('{}', '{}');
                """.format(
                    main_category_url,
                    main_category_name
                    )
                )

            #PRINT
            print('\n\n\nMAIN CATEGORY NAME', main_category_name)

            soup2 = bs4.BeautifulSoup(requests.get(main_category_url, headers=headers).text, 'html.parser')
            divs = soup2.find_all('div', {"class":'cct-wrap'})

            # GET MAIN CATEGORY ID 
            cursor.execute(
                """
                SELECT main_category_id
                FROM main_categories
                WHERE main_category_name = '{}'
                """.format(
                    main_category_name
                    )
                )

            main_category_id = cursor.fetchone()[0]

            # SUBCATEGORIES

            for div in divs:

                subcategory_url = home + div.h3.a['href'] + page_all
                subcategory_name = div.a.text

                #PRINT
                print('\n\nSUBCATEGORY NAME', subcategory_name)

                cursor.execute(
                    """
                    INSERT INTO subcategories (subcategory_name, main_category_id, sections)
                    VALUES ('{}','{}','{}');
                    """.format(
                        subcategory_name,
                        main_category_id,
                        False
                    )
                )

                cursor.execute(
                    """
                    SELECT subcategory_id
                    FROM subcategories
                    WHERE subcategory_name = '{}' AND main_category_id = '{}'
                    """.format(
                        subcategory_name,
                        main_category_id
                    )
                        )

                subcategory_id = cursor.fetchone()[0]

                # PRODUCTS

                product = {}

                try:
                    section_list = div.ul.findAll('li')[0:-1]
                
                    for section in section_list:
                        section_url = home + section.a['href'] + page_all
                        section_name = section.a.text

                        # PRINT
                        print('[SECTION NAME]', section_name)

                        cursor.execute(
                            """
                            INSERT INTO sections (section_url, section_name, subcategory_id)
                            VALUES ('{}','{}','{}')
                            """.format(
                                section_url, section_name, subcategory_id
                            )
                        )

                        # Set subcategory sections = True or False

                        cursor.execute(
                            """
                            UPDATE subcategories
                            SET sections = True
                            WHERE subcategory_id = '{}' AND subcategory_name = '{}';
                            """.format(
                                subcategory_id, subcategory_name
                            )
                        )
                        
                        soup3 = bs4.BeautifulSoup(requests.get(section_url, headers=headers).text, 'html.parser')

                        lis = soup3.findAll('li', {'class':'product'})
                        counter = 0
                        for li in lis:
                            try:
                                product_photo = li.find('div', {'class':'image'}).a.img['src'] = li.find('div', {'class':'image'}).a.img['src']
                                #IN STOCK OR NOT
                                if li.find('div', {'class':'p-not-available'}):  continue
                            except:
                                product_photo = None

                            try:
                                product_title = li.find('div', {'class':'product_info'}).h3.a.text.strip()
                                print("[PRODUCT TITLE] ", product_title)
                            except:
                                continue
                                
                            try:
                                product_url = home + li.div.div.a['href'] + page_all
                            except:
                                product_url = None

                            try:
                                product_url = home + li.div.div.a['href'] + page_all
                            except:
                                product_url = None

                            try:
                                product_info = li.find('div', {'class':'product_info'}).div
                                product_description = ''

                                for p in product_info.find_all('p'):
                                    product_description += p.text.strip() + ' \n '
                                
                            except:
                                product_description = None
        
                            try:
                                product_price = li.find('tr', {'class':'variant'}).td.span.text
                            except:
                                product_price = None
                            

                            cursor.execute(
                                """
                                SELECT section_id
                                FROM sections
                                WHERE subcategory_id = '{}' AND section_name = '{}'
                                """.format(subcategory_id, section_name)
                            )

                            section_id = cursor.fetchone()[0]

                            cursor.execute(
                                """
                                INSERT INTO products (product_url, product_photo, product_title, product_description, product_price, section_id)
                                VALUES ('{}','{}','{}','{}','{}','{}')""".format(
                                    product_url, product_photo, product_title, product_description, product_price, section_id
                                )
                            )

                except AttributeError:
                    pass

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)

finally:
    if connection:
        connection.close()
        print("[INFO] PostgreSQL connection closed")
