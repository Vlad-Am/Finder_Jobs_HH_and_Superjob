
def main():
    # Подставлем предварительно подготовленные id компаний для поиска вакансий по ним
    # Список компаний:
    employers = []
    table_creator = TableCreator

    name_table_employers = input("Введите имя таблицы с работадателями:\n")
    table_creator.create_emp(name_table_employers)

    name_table_vacancies = input("Введите имя таблицы с вакансиями:\n")
    table_creator.create_vac(name_table_vacancies)

    fill_db = FillDB(employers)
    fill_db.fill_db_vacancies(name_table_employers)
    try:
        fill_db.fill_db_vacancies(name_table_vacancies)
    except TypeError:
        print("Данные не получены")
    db_manger = DBManager()




if __name__ == '__main__':
    main()
