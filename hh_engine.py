import json
import psycopg2.errors
import requests
from db_manager import DBManager


class HeadHunterAPI:
    """Класс для доступа к api hh.ru"""
    employer_dict = {}
    employers_data = []
    vacancies_emp = []

    def __init__(self, employer: str):
        """Инициализация происходит через выбор работодателя"""
        self.employer = employer

    def get_employer(self) -> dict:
        """Метод для отправки запроса на hh и получения информации по работодателю"""

        url = "https://api.hh.ru/employers"
        params = {"text": self.employer, "area": 113, "per_page": 25}
        response = requests.get(url, params=params)
        info = response.json()
        print(info)
        if info is None:
            return "Данны не найдены"
        elif "errors" in info:
            return info["errors"][0]["value"]
        elif "items" not in info:
            return "Нет указанных работодателей"
        else:
            self.employer_dict = {'id': info["items"][0]["id"], 'name': info["items"][0]["name"],
                                  'alternate_url': info["items"][0]["alternate_url"]}
            self.employers_data.append(self.employer_dict)
            return self.employer_dict

    def __get_page_vacancies(self, employer_id: int, page: int) -> json:
        """Метод для получения всех вакансий работодателя по его id"""
        self.employer_id = employer_id
        params = {'employer_id': self.employer_id, 'area': 113, 'per_page': 100, 'page': page}
        response = requests.get("https://api.hh.ru/vacancies", params)
        data = response.content.decode()
        response.close()
        return data

    def get_vacancies(self, employer_id: int) -> list[dict]:
        """Метод для обработки полученной информации по вакансиям"""
        vacancies_emp_dicts = []
        # диапазон поиска страниц можно расширить или сузить
        # как написать функцию по узнаванию количества страниц по запросу я нашел
        # сюда смысла ее подтягивать не нашел
        for page in range(10):
            vacancies_data = json.loads(self.__get_page_vacancies(employer_id, page))

            if "errors" in vacancies_data:
                return vacancies_data["errors"][0]["value"]
            for vacancy_data in vacancies_data["items"]:
                if vacancy_data["salary"] is None:
                    vacancy_data["salary"] = {}
                    vacancy_data["salary"]["from"] = None
                    vacancy_data["salary"]["to"] = None

                vacancy_dict = {"id": vacancy_data["id"], "vacancy_name": vacancy_data["name"],
                                "url": vacancy_data["alternate_url"], "salary_from": vacancy_data["salary"]["from"],
                                "salary_to": vacancy_data["salary"]["to"],
                                "requirement": vacancy_data["snippet"]["requirement"],
                                "employer_id": vacancy_data["employer"]["id"]}
                if vacancy_dict["salary_to"] is None:
                    vacancy_dict["salary_to"] = vacancy_dict["salary_from"]
                vacancies_emp_dicts.append(vacancy_dict)
        return vacancies_emp_dicts


# HeadHunterAPI("Вконтакте").get_employer()
# HeadHunterAPI("Вконтакте").get_vacancies(15478)


class FillDB(HeadHunterAPI):
    """Класс для заполнения БД"""
    __employers_name = []

    def __init__(self, employers_list: list[str]):
        """Инициализация происходит через список работодателей"""
        self.employers_list = employers_list
        for employer in employers_list:
            super().__init__(employer)
            self.__employers_name.append(self.employer)

    @classmethod
    def __get_employers_all(cls):
        """Метод для получения информации из класса родителя по работодателям"""
        for emp in cls.__employers_name:
            employers_info = HeadHunterAPI(emp)
            employers_info.get_employer()
        return super().employers_data

    @classmethod
    def __get_vacancies_all(cls):
        """Метод для получения информации из класса родителя по вакансиям"""
        vacancies_all = []
        for emp in cls.employers_data:
            employer = HeadHunterAPI(emp["name"])
            vacancies_emp = employer.get_vacancies(emp["id"])
            for vacancy in vacancies_emp:
                vacancies_all.append(vacancy)
        return vacancies_all

    def fill_db_vacancies(self, table_name):
        """Метод для заполнения таблицы вакансий"""
        conn = DBManager.create_connection()
        try:
            for vac in self.__get_vacancies_all():

                try:
                    with conn:
                        with conn.cursor() as cursor:
                            cursor.execute(
                                f"""INSERT INTO {table_name} VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                                (vac["id"], vac["vacancy_name"], vac["url"], vac["salary_from"], vac["salary_to"],
                                 vac["requirement"], vac["employer_id"]))
                except psycopg2.errors.UniqueViolation:
                    continue
        except psycopg2.errors.UndefinedTable:
            print(f"Таблица {table_name} не найдена")
        finally:
            if conn:
                conn.close()
                print("Соединение с PostgreSQL закрыто")

    def fill_db_employers(self, table_name):
        """Метод для заполнения таблицы работодателей"""
        conn = DBManager.create_connection()
        employers = self.__get_employers_all()
        try:
            for emp in employers:
                try:
                    with conn:
                        with conn.cursor() as cursor:
                            cursor.execute(
                                f"""INSERT INTO {table_name} VALUES (%s, %s, %s)""",
                                (emp["id"], emp["name"], emp["alternate_url"]))
                except psycopg2.errors.UniqueViolation:
                    continue
        except psycopg2.errors.UndefinedTable:
            print(f"Таблица {table_name} не найдена")
        finally:
            if conn:
                conn.close()
                print("Соединение с PostgreSQL закрыто")
