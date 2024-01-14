import os
import psycopg2
from dotenv import load_dotenv


class DBManager:
    load_dotenv()
    password = os.environ.get("PASSWORD_DB")
    port = os.environ.get("POSTGRES_PORT")
    connection = psycopg2.connect(
        host="localhost",
        dbname="HH_RU",
        user="postgres",
        password=password,
        port=port
    )

    @staticmethod
    def connect():

        try:
            DBManager.connection.autocommit = True
            with DBManager.connection.cursor() as cursor:
                cursor.execute(
                    """CREATE TABLE employers(
                    id serial PRIMARY KEY,
                    external_id integer NOT NULL,
                    name_company varchar(64) NOT NULL,
                    city_company varchar(64)
                    )""")
            print("Таблица создана успешно")

        except Exception as ex:
            print("Ошибка создания БД", ex)

        finally:
            if DBManager.connection:
                DBManager.connection.close()
                print("Соединение с PostgreSQL закрыто")


DBManager.connect()

# cur = conn.cursor()
# cur.execute("CREATE DATABASE IF NOT EXISTS employers")
# conn.close()
