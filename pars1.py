import requests
from bs4 import BeautifulSoup
import json
import psycopg2
from config import user, host, password, db_name
import datetime


connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name   
    )
connection.autocommit = True



def get_pages():
    max_pages = []
    html = requests.get('https://2scoop.ru/catalog/proteiny/?SIZEN_1=42').text
    soup = BeautifulSoup(html, 'html5lib')
    pages = [i.text
            for i in soup("li")
            if i.text.isdigit()]
    return (int(max(pages)))


def names():
    all_products_list = []
    all_price_list = []
    for page in range(1,get_pages() - 1):
        html = requests.get(f'https://2scoop.ru/catalog/proteiny/?PAGEN_1={page}').text
        soup = BeautifulSoup(html, 'html5lib')
        product = soup ("h3", {'class' : 'product-item-title'})
        price = soup('span', {'class' : 'product-item-price-current'})
      
        for v in product:
            pr = ((v.text).replace('\t','')).replace('\n','')
            all_products_list.append(pr)
        
        for q in price:
            rp = ((q.text).replace('\t','')).replace('\n','').replace("'", "").replace("руб.", '').replace(" ", '')
            all_price_list.append(rp)

        product_and_price = dict( zip(all_products_list, all_price_list))
        b = len(product_and_price)
    len_product_and_price = len(product_and_price)
    
    with open("products_and_prices.json", "w") as file:
        json.dump(product_and_price, file, indent=1, ensure_ascii=False)


    with open("products_and_prices.json") as f:
        templates = json.load(f)
    
    count = 0
    for product_name, price in templates.items():   
        with connection.cursor() as cursor:
            if cursor.execute("""SELECT * FROM products WHERE Product_name_column =  (%s) ;""" , (  f'{product_name}', )):
                print("[INFO] Table not inserted successfully")
                connection.commit()
            else:
                cursor.execute(
                        """INSERT INTO Products ( Product_name_column) VALUES
                        ( %s) ;""", (  f'{product_name}', )
                    )
                connection.commit()
                print("[INFO] Table inserted successfully")

        with connection.cursor() as cursor:
                        cursor.execute(
                        """INSERT INTO Prices (prices, product) VALUES
                        ( %s, %s);""", (f'{price}',  f'{product_name}',)
                        )
                        connection.commit()
                        print("[INFO] Table inserted successfully")

        with connection.cursor() as cursor:
                        cursor.execute(
                        """COPY (SELECT * FROM Products JOIN Prices ON Product_name_column = Product where product_id = 1)
                         TO '/home/shah/Загрузки/2s_parser/p_p.csv' WITH (FORMAT CSV, HEADER);"""
                        )
                        connection.commit()
                        print("[INFO] Table COPY ")
if __name__ == "__main__":
    names()

 