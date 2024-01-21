import psycopg2

from create_tables import TableCreator
from db_manager import DBManager
from hh_engine import FillDB


def main():
    # Подставляем предварительно подготовленные компании для поиска вакансий по ним
    # Список компаний можно редактировать вручную, но для этого надо удалить старую таблицу с работодателями:
    employers = ['skyeng', 'маркет деливери', 'лаборатория касперского', 'lesta games', 'Вконтакте',
                 'LG Electronics Inc.', 'Sberbank', 'SberTech', 'YARD', 'Доктор Веб']
    # создаем экземпляр класса создающий таблицы
    table_creator = TableCreator()
    table_creator.create_company_table("employers")
    print("Таблицы с работодателями создана")

    name_table_vacancies = input("Введите имя таблицы с вакансиями:\n")
    table_creator.create_vacancies_table(name_table_vacancies)

    fill_db = FillDB(employers)
    fill_db.fill_db_employers("employers")
    try:
        fill_db.fill_db_vacancies(name_table_vacancies)
    except psycopg2.Error as e:
        print(e)
    db_manger = DBManager()
    data = db_manger.get_companies_and_vacancies_count("employers", name_table_vacancies)
    print("Информация по всем вакансий у каждой компании")
    for d in data:
        print(d)
    all_info = db_manger.get_all_vacancies("employers", name_table_vacancies)
    print("Информация по всем вакансиям компании")
    for info in all_info:
        print(info)
    salary = db_manger.get_avg_salary(name_table_vacancies)
    print("Средняя зарплата по всем вакансиям")
    print(salary)
    top_salary = db_manger.get_vacancies_with_higher_salary(name_table_vacancies)
    print("Список вакансий с зарплатой выше средней по всем вакансиям")
    for top in top_salary:
        print(top)
    print("Список вакансий с ключевым навыком 'python'")
    vacancies = db_manger.get_vacancies_with_keyword(name_table_vacancies, "python")
    for vac in vacancies:
        print(vac)


if __name__ == '__main__':
    main()
