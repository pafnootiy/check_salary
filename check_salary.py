from pprint import pprint
from itertools import count
from itertools import chain
import os

from dotenv import load_dotenv
from terminaltables import AsciiTable
import requests


def predict_rub_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    if salary_from:
        return salary_from * 1.2
    if salary_to:
        return salary_to * 0.8


def get_salary_info_from_hh(language, pages=1):
    url = "https://api.hh.ru/vacancies/"
    vacancies_processed = 0
    total_salary = 0

    for page in count(0):
        payload = {
            "text": language,
            "area": "1",
            "currency": "RUR",
            "only_with_salary": True,
            'page': page
        }
        response = requests.get(url, params=payload)
        response.raise_for_status()
        response_hh = response.json()

        for item in response_hh["items"]:
            if item.get('currency') != 'RUB':
                continue
            salary = predict_rub_salary(item["salary"]["from"], item["salary"]["to"])
            if salary:
                vacancies_processed += 1
                total_salary += salary
        if page >= pages:
            break
        vacancies_found = response_hh["found"]
        avarage_salary = total_salary / vacancies_processed if vacancies_processed else 0

    return {
        "vacancies_found": vacancies_found,
        "vacancies_processed": vacancies_processed,
        "avarage_salary": avarage_salary
    }


def create_data_tabs(hh_info, header):
    table = [["Язык программирования", "Вакансий найдено", "Вакансий отработано", "Средняя зп"]]

    for item in hh_info:
        table.append(
            [item["language"], item["info"]["vacancies_found"], item["info"]["vacancies_processed"],
             item["info"]["avarage_salary"]]
        )

    table_instance = AsciiTable(table, header)
    table_instance.justify_columns[1] = 'center'
    return (table_instance.table)


def get_sj_autorisation(secret_key, headers):
    url_for_autorisation = "https://www.superjob.ru/authorize/"
    sj_response = requests.post(url_for_autorisation, headers=headers)
    sj_response.raise_for_status()


def get_salary_info_from_sj(language, headers, pages=1):
    url_for_vacancy = "https://api.superjob.ru/2.0/vacancies/"

    vacancies_processed = 0
    total_salary = 0

    for page in count(0):
        payload = {'keyword': language,
                   "town": 4,
                   'page': None,
                   "no_agreement": 1
                   }
        response = requests.get(url_for_vacancy, headers=headers, params=payload)
        response.raise_for_status()
        response_sj = response.json()

        for item in response_sj["objects"]:
            salary = predict_rub_salary(item["payment_from"], item["payment_to"])
            if salary:
                vacancies_processed += 1
                total_salary += salary
        if page >= pages:
            break
        vacancies_found = response_sj["total"]
        avarage_salary = total_salary / vacancies_processed if vacancies_processed else 0

    return {
        "vacancies_found": vacancies_found,
        "vacancies_processed": vacancies_processed,
        "avarage_salary": avarage_salary
    }


def main():
    load_dotenv()
    secret_key = os.getenv("SJ_TOKEN")
    headers = {
        "X-Api-App-Id": secret_key
    }
    programming_languages = ["Python", "Java", "Javascript", "Ruby", "PHP", "C++", "CSS", "C#"]
    hh_salaries= []
    get_sj_autorisation(secret_key, headers)

    for language in programming_languages:
        vacancies_info_hh = get_salary_info_from_hh(language, pages=1)
        hh_salaries.append({'language': language, "info": vacancies_info_hh})

    for language in programming_languages:
        vacancies_info_sj = get_salary_info_from_sj(language, headers, pages=1)
        hh_salaries.append({'language': language, "info": vacancies_info_sj})

    title_site_hh = "HH Vacancies"
    title_site_sj = "SJ Vacancies"
    print(create_data_tabs(hh_salaries, title_site_hh))
    print(create_data_tabs(hh_salaries, title_site_sj))


if __name__ == '__main__':
    main()
