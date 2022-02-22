import requests
from pprint import pprint
from itertools import count
from itertools import chain
from terminaltables import AsciiTable
import os
from dotenv import load_dotenv
import collections


def get_salary_info_from_hh(language):
    url = "https://api.hh.ru/vacancies/"
    all_pages_with_salary = []

    for page in count(0):
        payload = {
            "text": f"{language}",
            "area": "1",
            "currency": "RUR",
            "only_with_salary": True,
            'page': page
        }
        response = requests.get(url, params=payload)
        response.raise_for_status()
        pages_data = response.json()["items"]
        for salary in pages_data:
            all_pages_with_salary.append(salary["salary"])
        # if page > pages_data['pages']:
        if page > 10:  # долго собирает при полной паганации
            break

    return all_pages_with_salary


def get_all_salary_from_hh(salary_info):
    all_salary_from_hh = []
    for salary in salary_info:
        try:
            payment = salary["from"] * 1.2
            all_salary_from_hh.append(payment)
        except TypeError:
            continue
    return all_salary_from_hh


def get_all_salary_to_hh(salary_info):
    all_salary_to_hh = []
    for salary in salary_info:
        try:
            payment = salary["to"] * 0.8
            all_salary_to_hh.append(payment)
        except TypeError:
            continue
    return all_salary_to_hh


def get_average_salary(salary_from, salary_to):
    all_salary = list(chain(salary_from, salary_to))
    average_salary = int(sum(all_salary) / len(all_salary))
    return average_salary


def get_vacancies_processed(salary_from, salary_to):
    return len(list(chain(salary_from, salary_to)))


def get_vacancies_numbers_hh(language):
    url = "https://api.hh.ru/vacancies/"
    payload = {
        "text": f"{language}",
        "area": "1",
        "currency": "RUR",
        "only_with_salary": True,
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    vacancies_found = response.json()["found"]
    return vacancies_found


def print_data_tabs(table, columns, title_site):
    data_tabs_hh = [columns]

    for string in table:
        data_tabs_hh.append(string)
    title = title_site
    table_instance = AsciiTable(data_tabs_hh, title)
    table_instance.justify_columns[1] = 'center'
    print(table_instance.table)


def get_sj_autorisation(secret_key, headers):
    url_for_autorisation = "https://www.superjob.ru/authorize/"
    sj_response = requests.post(url_for_autorisation, headers=headers)
    sj_response.raise_for_status()


def get_salary_info_from_sj(language, headers):
    url_for_vacancy = "https://api.superjob.ru/2.0/vacancies/"
    all_pages_with_salary = []

    for page in count(0):
        payload = {'keyword': f"{language}",
                   "town": 4,
                   'page': page,
                   "no_agreement": 1
                   }
        sj_vacancy_response = requests.get(url_for_vacancy, headers=headers, params=payload)
        sj_vacancy_response.raise_for_status()
        sj_vacancy_response = sj_vacancy_response.json()
        all_pages_with_salary.append(sj_vacancy_response)
        # print(sj_vacancy_response)
        # print(page)
        if page >= 5:
            # if page >= 500:# долго собирает при полной паганации
            break
    return all_pages_with_salary


def get_vacancies_found_sj(language, headers):
    url_for_vacancy = "https://api.superjob.ru/2.0/vacancies/"
    for page in count(0):
        payload = {'keyword': f"{language}",
                   "town": 4,
                   'page': page,
                   "no_agreement": 1
                   }
        sj_vacancy_response = requests.get(url_for_vacancy, headers=headers, params=payload)
        sj_vacancy_response.raise_for_status()
        sj_vacancy_response = sj_vacancy_response.json()["total"]
        if page >= 15:
            # if page >= 500:# долго собирает при полной паганации
            break
    return sj_vacancy_response


def get_all_salary_from_sj(salary_info_sj):
    all_salary_from_sj = []

    for vacancies in salary_info_sj:
        for salary in vacancies['objects']:
            try:
                if salary['payment_from']:
                    payment = salary['payment_from'] * 1.2
                    all_salary_from_sj.append(payment)
            except TypeError:
                continue
    return all_salary_from_sj


def get_all_salary_to_sj(salary_info_sj):
    all_salary_to_sj = []
    for vacancies in salary_info_sj:
        for salary in vacancies['objects']:
            try:
                if salary['payment_to']:
                    payment = salary['payment_to'] * 1.2
                    all_salary_to_sj.append(payment)
            except TypeError:
                continue
    return all_salary_to_sj


def main():
    table_hh = []
    table_sj = []
    title_site_hh = "HH Vacancies"
    title_site_sj = "SJ Vacancies"

    load_dotenv()
    secret_key = os.getenv("SJ_TOKEN")
    headers = {
        "X-Api-App-Id": secret_key
    }
    columns = ["Язык программирования ", "Вакансий найдено", "Вакансий отработано", "Средняя ЗП"]
    programming_languages = ["Python", "Java", "Javascript", "Ruby", "PHP", "C++", "CSS", "C#"]
    for language in programming_languages:
        salary_info = get_salary_info_from_hh(language)
        salary_from_hh = (get_all_salary_from_hh(salary_info))
        salary_to_hh = get_all_salary_to_hh(salary_info)
        average_salary = get_average_salary(salary_from_hh, salary_to_hh)
        vacancies_processed = get_vacancies_processed(salary_from_hh, salary_to_hh)
        vacancies_found = get_vacancies_numbers_hh(language)
        sample_form = [language, vacancies_found, vacancies_processed, average_salary]
        table_hh.append(sample_form)

        get_sj_autorisation(secret_key, headers)
        salary_info_sj = get_salary_info_from_sj(language, headers)
        salary_from_sj = get_all_salary_from_sj(salary_info_sj)
        salary_to_sj = get_all_salary_to_sj(salary_info_sj)
        average_salary_sj = get_average_salary(salary_from_sj, salary_to_sj)
        vacancies_processed_sj = get_vacancies_processed(salary_from_sj, salary_to_sj)
        vacancies_found_sj = get_vacancies_found_sj(language, headers)
        sample_form_sj = [language, vacancies_found_sj, vacancies_processed_sj, average_salary_sj]
        table_sj.append(sample_form_sj)

    print_data_tabs(table_hh, columns, title_site_hh)
    print_data_tabs(table_sj, columns, title_site_sj)


if __name__ == "__main__":
    main()
