from pprint import pprint
from itertools import count
from itertools import chain
import os

from dotenv import load_dotenv
from terminaltables import AsciiTable
import requests

def get_salary_info_from_hh(language):
    url = "https://api.hh.ru/vacancies/"

    salary_from_to = []
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
        hh_json = response.json()

        for salary in hh_json["items"]:
            salary_from_to.append(salary["salary"])
        if page >= 20:
            break
        vacancies_found = hh_json["found"]
    return salary_from_to, vacancies_found


def get_salaries_from_to(salary_hh):
    salary_from_to = []
    for salary in salary_hh[0]:
        if salary["from"]:
            payment_from = salary["from"] * 1.2
            salary_from_to.append(payment_from)
        else:
            payment_to = salary["to"] * 0.8
            salary_from_to.append(payment_to)
    return salary_from_to




def get_average_salary_and_processed(salary):
    average_salary = int(sum(salary) / len(salary))
    vacancies_processed = len(salary)
    return average_salary, vacancies_processed


def get_sj_autorisation(secret_key, headers):
    url_for_autorisation = "https://www.superjob.ru/authorize/"
    sj_response = requests.post(url_for_autorisation, headers=headers)
    sj_response.raise_for_status()


def get_salary_info_from_sj(language, headers):
    url_for_vacancy = "https://api.superjob.ru/2.0/vacancies/"
    salary_from_to_sj = []

    for page in count(0):
        payload = {'keyword': language,
                   "town": 4,
                   'page': page,
                   "no_agreement": 1
                   }
        response = requests.get(url_for_vacancy, headers=headers, params=payload)
        response.raise_for_status()
        sj_json = response.json()
        if sj_json['total']:
            sj_total = sj_json['total']

        for salary in sj_json["objects"]:
            salary_from_to_sj.append(salary)

        if page >= 65:
            break
    return salary_from_to_sj, sj_total


def get_salary_from_to_sj(salary_sj):
    salary_from_to = []
    for salary in salary_sj[0]:
        if salary["payment_from"]:
            payment_from = salary["payment_from"] * 1.2
            salary_from_to.append(payment_from)
        else:
            payment_to = salary["payment_to"] * 0.8
            salary_from_to.append(payment_to)
    return salary_from_to


def create_dictionary(language, salary, vacancies_processed, average_salary):
    table = []
    sample_form = {
        language: {"vacancies_found": salary, "vacancies_processed": vacancies_processed,
                   "average_salary": average_salary}}

    for lang, stats in sample_form.items():
        table.append([language, stats["vacancies_found"], stats["vacancies_processed"], stats["average_salary"]])

    return table


def print_data_tabs(table, title_site):
    columns = ["Язык программирования ", "Вакансий найдено", "Вакансий отработано", "Средняя ЗП"]
    data_tabs = [columns]

    for string in table:
        data_tabs.append(string)
    title = title_site
    table_instance = AsciiTable(data_tabs, title)
    table_instance.justify_columns[1] = 'center'
    print(table_instance.table)


def main():
    programming_languages = ["Python", "Java"]
    table_hh = []
    table_sj = []

    for language in programming_languages:
        salary_hh = get_salary_info_from_hh(language)
        salary_from_to_hh = get_salaries_from_to(salary_hh)
        average_salary_and_processed = get_average_salary_and_processed(salary_from_to_hh)
        table_col_hh = create_dictionary(language, salary_hh[1], average_salary_and_processed[1],
                                         average_salary_and_processed[0])
        table_hh.append(table_col_hh[0])

        load_dotenv()
        secret_key = os.getenv("SJ_TOKEN")
        headers = {
            "X-Api-App-Id": secret_key
        }
        get_sj_autorisation(secret_key, headers)
        salary_sj = get_salary_info_from_sj(language, headers)
        sj_salary_from_to = get_salary_from_to_sj(salary_sj)
        average_salary_and_processed_sj = get_average_salary_and_processed(sj_salary_from_to)
        table_col_sj = create_dictionary(language, salary_sj[1], average_salary_and_processed_sj[1],
                                         average_salary_and_processed_sj[0])

        table_sj.append(table_col_sj[0])
    title_site_hh = "HH Vacancies"
    print_data_tabs(table_hh, title_site_hh)
    title_site_sj = "SJ Vacancies"
    print_data_tabs(table_sj, title_site_sj)


if __name__ == '__main__':
    main()
