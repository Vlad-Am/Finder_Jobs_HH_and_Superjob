import json

import requests


class HeadHunterAPI:
    """Класс для доступа к api hh.ru"""

    def __init__(self, vacancies):
        self.vacancies = vacancies
        self.vacancies_all = []
        self.vac = []
        self.vacancies_dicts = []
        self.info = self.get_request()
        print("Подключаюсь к HH.ru")

    def get_request(self):
        """Метод для отправки запроса на hh, записывает json"""

        for num in range(50):
            url = "https://api.hh.ru/vacancies"
            params = {"text": self.vacancies, "area": 113, "per_page": 25, "page": num}
            response = requests.get(url, params=params)
            info = response.json()
            if info is None:
                return "Данны не найдены"
            elif "errors" in info:
                return info["errors"][0]["value"]
            elif "items" not in info:
                return "Нет вакансий"
            else:
                for vacancy in range(len(info["items"])):
                    if (info["items"][vacancy]["salary"] is not None
                            and info["items"][vacancy]["salary"]["currency"] == 'RUR'):
                        self.vac.append([info["items"][vacancy]["employer"]["name"],
                                         info["items"][vacancy]["name"],
                                         info["items"][vacancy]["apply_alternate_url"],
                                         info["items"][vacancy]["snippet"]["requirement"],
                                         info["items"][vacancy]["salary"]["from"],
                                         info["items"][vacancy]["salary"]["to"]])
        for vacancy in self.vac:
            vacancies_dict = {"employer": vacancy[0], "name": vacancy[1], "url": vacancy[2], "requirement": vacancy[3],
                              "salary_from": vacancy[4], "salary_to": vacancy[5]}
            if vacancies_dict["salary_from"] is None:
                vacancies_dict["salary_from"] = 0
            elif vacancies_dict["salary_to"] is None:
                vacancies_dict["salary_to"] = vacancies_dict["salary_from"]
            self.vacancies_dicts.append(vacancies_dict)

        with open(f"{self.vacancies}_hh_ru.json", "w", encoding="UTF-8") as file:
            json.dump(self.vacancies_dicts, file, indent=4, ensure_ascii=False)
        print(f"Отбор осуществлялся из {len(self.vac)} вакансий(проверка обращения к сервису)")
        return self.vacancies_dicts

hh = HeadHunterAPI("python developer")

