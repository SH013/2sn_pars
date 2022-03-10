import psycopg2
from config import host, user, password, db_name


connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name    
)
connection.autocommit = True

try:
    with connection.cursor() as cursor:
        cursor.execute(
                    """CREATE TABLE Products(
                        Product_id SERIAL ,
                        Product_name_column VARCHAR(200))
                    ;"""
                )
        print("[INFO] Table create Products")

    with connection.cursor() as cursor:
        cursor.execute(
                    """CREATE TABLE Prices(
                        id SERIAL Primary key,
                        posting_date DATE NOT NULL DEFAULT CURRENT_DATE,
                        Prices INTEGER,
                        Product VARCHAR(200))
                    ;"""
                )
        print("[INFO] Table create Price")   

except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
