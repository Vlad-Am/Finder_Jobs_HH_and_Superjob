import psycopg2.errors

from db_manager import DBManager


class TableCreator:
    """ Класс для создания таблиц в PostgresQL """

    @staticmethod
    def create_vacancies_table(table_vacancies_name):
        con = DBManager.create_connection()
        try:
            with con:
                with con.cursor() as cursor:
                    cursor.execute(f'''CREATE TABLE {table_vacancies_name}
                                      (id serial PRIMARY KEY,
                                      name_vacancy varchar(100) NOT NULL,
                                      url_vacancy varchar(200) NOT NULL,
                                      salary_from integer,
                                      salary_to integer,
                                      employer_id integer
                                      REFERENCES employers(employer_id))''')
                print(f"Таблица {table_vacancies_name} создана успешно")

        except psycopg2.errors.DuplicateTable:
            print(f"Такая таблица уже существует считываю данные")

        finally:
            if con:
                con.close()
                print("Соединение с PostgreSQL закрыто")

    @staticmethod
    def create_company_table(table_company_name):
        con = DBManager.create_connection()
        try:
            with con:
                with con.cursor() as cursor:
                    cursor.execute(
                        f'''CREATE TABLE {table_company_name}(
                           employer_id SERIAL PRIMARY KEY,
                           name_company varchar(100) NOT NULL,
                           url varchar(200))
                           ''')
                print(f"Таблица {table_company_name} создана успешно")

        except psycopg2.errors.DuplicateTable:
            print(f"Такая таблица уже существует считываю данные")

        finally:
            if con:
                con.close()
                print("Соединение с PostgreSQL закрыто")
