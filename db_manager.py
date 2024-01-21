import os
import psycopg2
from dotenv import load_dotenv


class DBManager:

    @staticmethod
    def create_connection():
        load_dotenv()
        password = os.environ.get("PASSWORD_DB")
        connection = psycopg2.connect(
            host="localhost",
            dbname="HH_RU",
            user="postgres",
            password=password
        )
        return connection

    @staticmethod
    def get_companies_and_vacancies_count(table_name_emp: str, table_name_vac: str):
        """Получает количество всех вакансий у каждой компании из начального списка """
        employers_vac_list = []
        con = DBManager.create_connection()
        try:
            with con:
                with con.cursor() as cursor:
                    cursor.execute(f"""SELECT name_company, COUNT({table_name_vac}) AS vac_count
                                        FROM {table_name_emp}
                                        INNER JOIN {table_name_vac}
                                        USING (employer_id)
                                        GROUP BY name_company
                                        ORDER BY vac_count DESC""")
                    vacancies = cursor.fetchall()
                    for vac in vacancies:
                        emp, vac_count = vac
                        employers_vac_list.append(f"Работодатель {emp}: число вакансий {vac_count}")
        finally:
            if con:
                con.close()
                print("Соединение с PostgreSQL закрыто")
        return employers_vac_list

    @staticmethod
    def get_all_vacancies(table_name_emp: str, table_name_vac: str) -> list[str]:
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        vacancies_data_list = []
        con = DBManager.create_connection()
        try:
            with con:
                with con.cursor() as cursor:
                    cursor.execute(f'''SELECT name_company, name_vacancy, url_vacancy, salary_from, salary_to
                                        FROM {table_name_emp}
                                        JOIN {table_name_vac}
                                        USING(employer_id)''')
                    all_info = cursor.fetchall()
                    for vac_info in all_info:
                        emp_name, vac_name, vac_url, vac_sal_from, vac_sal_to, = vac_info
                        form_sal_from, form_sal_to = DBManager.format_salary(vac_sal_from, vac_sal_to)
                        vacancies_data_list.append(
                            f"""Работодатель {emp_name}: вакансия {vac_name}: зарплата от {form_sal_from}
                                до {form_sal_to} ссылка на вакансию {vac_url}""")

        finally:
            if con:
                con.close()
                print("Соединение с PostgreSQL закрыто")
        return vacancies_data_list

    @staticmethod
    def get_avg_salary(table_name_vac: str) -> str:
        """ Получает среднюю зарплату по вакансиям."""
        con = DBManager.create_connection()
        try:
            with con:
                with con.cursor() as cursor:
                    cursor.execute(f"""SELECT AVG(salary_from) AS avg_sal_from FROM {table_name_vac}""")
                    avg_salary = cursor.fetchall()[0]
        finally:
            if con:
                con.close()
                print("Соединение с PostgreSQL закрыто")
        return f"Средняя зарплата: {avg_salary}"

    @staticmethod
    def get_vacancies_with_higher_salary(table_name_vac: str):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        salaries_top_list = []
        connection = DBManager.create_connection()
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(f"""SELECT name_vacancy, salary_from
                                        FROM {table_name_vac} 
                                        WHERE salary_from > (SELECT AVG(salary_from) FROM {table_name_vac})
                                        ORDER BY salary_from DESC""")
                    top_salaries = cursor.fetchall()
                    for salary in top_salaries:
                        name, sal_top = salary
                        salaries_top_list.append(
                            f"Вакансия {name}: зарплата выше средней по всем вакансиям: {sal_top}"
                        )
        finally:
            if connection:
                connection.close()
                print("Соединение с PostgreSQL закрыто")
        return salaries_top_list

    @staticmethod
    def get_vacancies_with_keyword(table_name_vac: str, keyword: str):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        """
        vacancies_list = []
        connection = DBManager.create_connection()
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(f'''SELECT name_vacancy, url_vacancy, salary_from, salary_to, requirement
                                        FROM {table_name_vac} 
                                        WHERE requirement LIKE '%{keyword}%'
                                        ORDER BY salary_from DESC''')
                    vac_keyword = cursor.fetchall()
                    for vacancy in vac_keyword:
                        name, url, sal_from, sal_to, requirement = vacancy
                        form_sal_from, form_sal_to = DBManager.format_salary(sal_from, sal_to)
                        vacancies_list.append(
                            f"Вакансия {name}: зарплата от {form_sal_from} до {form_sal_to}"
                            f": ссылка на вакансию {url}, требования: {requirement}")
        finally:
            if connection:
                connection.close()
                print("Соединение с PostgreSQL закрыто")
        return vacancies_list

    @staticmethod
    def format_salary(vac_sal_from, vac_sal_to):
        if vac_sal_from is None:
            vac_sal_from = "не указана"
        if vac_sal_to is None:
            vac_sal_to = "не указана"
        return vac_sal_from, vac_sal_to

# DBManager.create_vacancies_table('test_table')
