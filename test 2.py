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
    salary_from_to = []

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
        vacancie_pages = response.json()
        for salary in vacancie_pages["items"]:
            if salary["salary"]["from"]:
                payment_from = salary["salary"]["from"] * 1.2
                salary_from_to.append(payment_from)
            else:
                payment_to = salary["salary"]["to"] * 0.8
                salary_from_to.append(payment_to)

        # if page > pages_data['pages']:
        if page > 5:  # долго собирает при полной паганации
            break
        vacancies_found = response.json()["found"]
    return salary_from_to, vacancies_found


salary_and_found_hh = get_salary_info_from_hh(language)


def get_average_salary_and_processed(salary_and_found_hh):
    average_salary = int(sum(salary_and_found_hh[0]) / len(salary_and_found_hh[0]))
    vacancies_processed = len(salary_and_found_hh[0])
    return average_salary, vacancies_processed


average_salary_and_processed = get_average_salary_and_processed(salary_and_found_hh)



table_hh = []
sample_form = [language, salary_and_found_hh[1], average_salary_and_processed[1], average_salary_and_processed[0]]
table_hh.append(sample_form)
title_site_hh = "HH Vacancies"


def print_data_tabs(table, title_site):
    columns = ["Язык программирования ", "Вакансий найдено", "Вакансий отработано", "Средняя ЗП"]
    data_tabs_hh = [columns]

    for string in table:
        data_tabs_hh.append(string)
    title = title_site
    table_instance = AsciiTable(data_tabs_hh, title)
    table_instance.justify_columns[1] = 'center'
    print(table_instance.table)


print_data_tabs(table_hh, title_site_hh)  #MVP







# def get_sj_autorisation(secret_key, headers):
#     url_for_autorisation = "https://www.superjob.ru/authorize/"
#     sj_response = requests.post(url_for_autorisation, headers=headers)
#     sj_response.raise_for_status()
#
#
# def get_salary_info_from_sj(language, headers):
#     url_for_vacancy = "https://api.superjob.ru/2.0/vacancies/"
#     all_pages_with_salary = []
#
#     for page in count(0):
#         payload = {'keyword': f"{language}",
#                    "town": 4,
#                    'page': page,
#                    "no_agreement": 1
#                    }
#         sj_vacancy_response = requests.get(url_for_vacancy, headers=headers, params=payload)
#         sj_vacancy_response.raise_for_status()
#         sj_vacancy_response = sj_vacancy_response.json()
#         all_pages_with_salary.append(sj_vacancy_response)
#         # print(sj_vacancy_response)
#         # print(page)
#         if page >= 5:
#             # if page >= 500:# долго собирает при полной паганации
#             break
#     return all_pages_with_salary
#
#
# def get_vacancies_found_sj(language, headers):
#     url_for_vacancy = "https://api.superjob.ru/2.0/vacancies/"
#     for page in count(0):
#         payload = {'keyword': f"{language}",
#                    "town": 4,
#                    'page': page,
#                    "no_agreement": 1
#                    }
#         sj_vacancy_response = requests.get(url_for_vacancy, headers=headers, params=payload)
#         sj_vacancy_response.raise_for_status()
#         sj_vacancy_response = sj_vacancy_response.json()["total"]
#         if page >= 15:
#             # if page >= 500:# долго собирает при полной паганации
#             break
#     return sj_vacancy_response
#
#
# def get_all_salary_from_sj(salary_info_sj):
#     all_salary_from_sj = []
#
#     for vacancies in salary_info_sj:
#         for salary in vacancies['objects']:
#             try:
#                 if salary['payment_from']:
#                     payment = salary['payment_from'] * 1.2
#                     all_salary_from_sj.append(payment)
#             except TypeError:
#                 continue
#     return all_salary_from_sj
#
#
# def get_all_salary_to_sj(salary_info_sj):
#     all_salary_to_sj = []
#     for vacancies in salary_info_sj:
#         for salary in vacancies['objects']:
#             try:
#                 if salary['payment_to']:
#                     payment = salary['payment_to'] * 1.2
#                     all_salary_to_sj.append(payment)
#             except TypeError:
#                 continue
#     return all_salary_to_sj
#
#
# def main():
#     table_hh = []
#     table_sj = []
#     title_site_hh = "HH Vacancies"
#     title_site_sj = "SJ Vacancies"
#
#     load_dotenv()
#     secret_key = os.getenv("SJ_TOKEN")
#     headers = {
#         "X-Api-App-Id": secret_key
#     }
#     columns = ["Язык программирования ", "Вакансий найдено", "Вакансий отработано", "Средняя ЗП"]
#     programming_languages = ["Python", "Java", "Javascript", "Ruby", "PHP", "C++", "CSS", "C#"]
#     for language in programming_languages:
#         salary_info = get_salary_info_from_hh(language)
#         salary_from_hh = (get_all_salary_from_hh(salary_info))
#         salary_to_hh = get_all_salary_to_hh(salary_info)
#         average_salary = get_average_salary(salary_from_hh, salary_to_hh)
#         vacancies_processed = get_vacancies_processed(salary_from_hh, salary_to_hh)
#         vacancies_found = get_vacancies_numbers_hh(language)
#         sample_form = [language, vacancies_found, vacancies_processed, average_salary]
#         table_hh.append(sample_form)
#
#         get_sj_autorisation(secret_key, headers)
#         salary_info_sj = get_salary_info_from_sj(language, headers)
#         salary_from_sj = get_all_salary_from_sj(salary_info_sj)
#         salary_to_sj = get_all_salary_to_sj(salary_info_sj)
#         average_salary_sj = get_average_salary(salary_from_sj, salary_to_sj)
#         vacancies_processed_sj = get_vacancies_processed(salary_from_sj, salary_to_sj)
#         vacancies_found_sj = get_vacancies_found_sj(language, headers)
#         sample_form_sj = [language, vacancies_found_sj, vacancies_processed_sj, average_salary_sj]
#         table_sj.append(sample_form_sj)
#
#     print_data_tabs(table_hh, columns, title_site_hh)
#     print_data_tabs(table_sj, columns, title_site_sj)
#
# # if __name__ == "__main__":
# # main()
