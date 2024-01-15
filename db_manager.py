import os
import psycopg2
import requests
from dotenv import load_dotenv
from psycopg2.errors import DuplicateTable


class DBManager:
    def __init__(self):
        self.connection = self.create_connection()

    @staticmethod
    def create_connection(port=5432):
        load_dotenv()
        password = os.environ.get("PASSWORD_DB")
        connection = psycopg2.connect(
            host="localhost",
            dbname="HH_RU",
            user="postgres",
            password=password,
        )
        return connection

    def create_vacancies_table(self, table_name):

        try:
            self.connection.autocommit = True
            with self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute(
                        f"""CREATE TABLE {table_name}(
                            id serial PRIMARY KEY,
                            external_id integer NOT NULL,
                            url varchar(64) NOT NULL,
                            name_vacancy varchar(64) NOT NULL,
                            city varchar(64),
                            company_id integer NOT NULL REFERENCES {table_name}(id),
                            salary_from integer,
                            salary_to integer)""")
                print(f"Таблица {table_name} создана успешно")

        except psycopg2.errors.DuplicateTable:
            print(f"Такая таблица уже существует считываю данные")

        finally:
            if self.connection:
                self.connection.close()
                print("Соединение с PostgreSQL закрыто")

    def create_company_table(self, table_name):

        try:
            self.connection.autocommit = True
            with self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute(
                        f"""CREATE TABLE {table_name}(
                        id serial PRIMARY KEY,
                        external_id integer NOT NULL,
                        name_company varchar(64) NOT NULL,
                        city_company varchar(64))
                        """)
                print(f"Таблица {table_name} создана успешно")

        except psycopg2.errors.DuplicateTable:
            print(f"Такая таблица уже существует считываю данные")

        finally:
            if self.connection:
                self.connection.close()
                print("Соединение с PostgreSQL закрыто")

    def get_companies_and_vacancies_count(self, table_name_emp: str, table_name_vac: str):
        """Получает список всех вакансий у каждой компании """
        employers_vac_list = []
        try:
            with self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute(f"SELECT * FROM {table_name_emp}")
                    employers = cursor.fetchall()
                    for employer in employers:
                        cursor.execute(f"""SELECT employer_name, COUNT({table_name_vac}) AS vac_count
                        FROM {table_name_emp},
                        INNER JOIN {table_name_vac}, 
                        USING (employer_id),
                        GROUP BY employee_name,
                        ORDER BY vac_count DESC""")
                        vacancies = cursor.fetchall()
                        for vac in vacancies:
                            emp, vac_count = vac
                            employers_vac_list.append(f"Работадатель {emp}: число вакансий {vac_count}")
        finally:
            if self.connection:
                self.connection.close()
                print("Соединение с PostgreSQL закрыто")
        return employers_vac_list


test = DBManager
test.create_vacancies_table("vac1")
test.create_company_table("emp1")

