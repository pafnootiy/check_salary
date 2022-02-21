import requests
from pprint import pprint
from itertools import count
from itertools import chain
from terminaltables import AsciiTable
import os
from dotenv import load_dotenv
import collections

language = "Python"


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
        if page > 1:  # долго собирает при полной паганации
            break

    return all_pages_with_salary


# salary_info = get_salary_info_from_hh(language)


def get_all_salary_from_hh(salary_info):
    all_salary_from_hh = []
    for salary in salary_info:
        try:
            payment = salary["from"] * 1.2
            all_salary_from_hh.append(payment)
        except TypeError:
            continue
    return all_salary_from_hh


# salary_from_hh = (get_all_salary_from_hh(salary_info))


def get_all_salary_to_hh(salary_info):
    all_salary_to_hh = []
    for salary in salary_info:
        try:
            payment = salary["to"] * 0.8
            all_salary_to_hh.append(payment)
        except TypeError:
            continue
    return all_salary_to_hh


# salary_to_hh = get_all_salary_to_hh(salary_info)


def get_average_salary(salary_from, salary_to):

    all_salary = list(chain(salary_from, salary_to))
    average_salary= int(sum(all_salary) / len(all_salary))
    # print(average_salary)
    return average_salary


# average_salary = get_average_salary(salary_from_hh, salary_to_hh)


def get_vacancies_processed(salary_from, salary_to):
    # vacancies_processed = []
    vacancies_processed = len(list(chain(salary_from, salary_to)))
    # vacancies_processed.append(len(merge_salary))
    # print(vacancies_processed)
    return vacancies_processed


# vacancies_processed = get_vacancies_processed(salary_from_hh, salary_to_hh)


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
    # print(count_vacancies)

    return vacancies_found


# count_vacancies = get_vacancies_numbers_hh(language)

# statistics_dict = {language: {"vacancies_found": count_vacancies, "vacancies_processed": vacancies_processed,
#                               "avarage_salary": average_salary}}

# form_for_table = [language, count_vacancies, vacancies_processed, average_salary]

# print(statistics_dict)
columns = ["Язык программирования ", "Вакансий найдено", "Вакансий отработано", "Средняя ЗП"]

def print_data_tabs(form_for_table,columns):

    # data_tabs_hh = [columns, form_for_table]
    data_tabs_hh = []
    data_tabs_hh.append(columns)
    data_tabs_hh.append(form_for_table)

    title = 'HH Vacancies'
    table_instance = AsciiTable(data_tabs_hh, title)
    table_instance.justify_columns[1] = 'center'
    # inner_heading_row_border = True
    print(table_instance.table)
# get_data_tabs(form_for_table,columns)

def main():
    # language = "Python"
    programming_languages = ["Python", "Java", "Javascript", "Ruby", "PHP", "C++", "CSS", "C#"]

    # print(language)
    for language in programming_languages:


        salary_info = get_salary_info_from_hh(language)
        salary_from_hh = (get_all_salary_from_hh(salary_info))
        salary_to_hh = get_all_salary_to_hh(salary_info)
        average_salary = get_average_salary(salary_from_hh, salary_to_hh)
        vacancies_processed = get_vacancies_processed(salary_from_hh, salary_to_hh)


        vacancies_found = get_vacancies_numbers_hh(language)


        statistics_dict = {language: {"vacancies_found": vacancies_found, "vacancies_processed": vacancies_processed,
                                      "avarage_salary": average_salary}}

        form_for_table = [language, vacancies_found, vacancies_processed, average_salary]




    print_data_tabs(form_for_table, columns)

if __name__ == "__main__":
    main()