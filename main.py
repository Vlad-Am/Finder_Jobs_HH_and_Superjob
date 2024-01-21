from create_tables import TableCreator
from db_manager import DBManager
from hh_engine import FillDB


def main():
    # Подставляем предварительно подготовленные компании для поиска вакансий по ним
    # Список компаний:
    employers = ['skyeng', 'skillbox', 'лаборатория касперского', 'lesta games', 'Вконтакте', 'LG Electronics Inc.',
                 'SberTech', 'YARD', 'Доктор Веб']
    table_creator = TableCreator
    name_table_employers = input("Введите имя таблицы с работодателями:\n")
    table_creator.create_company_table(name_table_employers)

    name_table_vacancies = input("Введите имя таблицы с вакансиями:\n")
    table_creator.create_vacancies_table(name_table_vacancies)

    fill_db = FillDB(employers)
    fill_db.fill_db_employers(name_table_employers)
    try:
        fill_db.fill_db_vacancies(name_table_vacancies)
    except TypeError:
        print("Данные не получены")
    db_manger = DBManager()
    data = db_manger.get_companies_and_vacancies_count(name_table_employers, name_table_vacancies)
    print("Информация по всем вакансий у каждой компании")
    for d in data:
        print(d)
    all_info = db_manger.get_all_vacancies(name_table_employers, name_table_vacancies)
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
    vacancies = db_manger.get_vacancies_with_keyword(name_table_vacancies, "flask")
    for vac in vacancies:
        print(vac)


if __name__ == '__main__':
    main()
