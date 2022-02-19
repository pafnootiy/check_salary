import requests
from pprint import pprint
from itertools import count
from itertools import chain
from terminaltables import AsciiTable
import os
from dotenv import load_dotenv
import collections
# from collections import collections
# programming_languages = ["Python", "Java", "Javascript", "Ruby", "PHP", "C++", "CSS", "C#"]

language = ["программист"]


def get_all_vacancies_from_hh(language):
    url = "https://api.hh.ru/vacancies/"
    all_pages_with_vacancies = []

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
        pages_data = response.json()
        all_pages_with_vacancies.append(pages_data)
        # if page > pages_data['pages']:
        if page > 3:  # долго собирает при полной паганации
            break

    return all_pages_with_vacancies


# all_vacancies_from_hh = get_all_vacancies_from_hh(language)


# print(all_vacancies_from_hh)

def get_all_salary_from_hh(all_vacancies_from_hh):
    all_salary_from_hh = []
    for vacancy in all_vacancies_from_hh:
        # print(all_vacancies_from_hh)
        for salary in vacancy["items"]:
            try:
                payment = salary["salary"]["from"] * 1.2
                # print(salary_from_hh)
            except TypeError:
                salary_none = "none"

            all_salary_from_hh.append(payment)
    return all_salary_from_hh


# salary_from_hh = (get_all_salary_from_hh(all_vacancies_from_hh))


def get_all_salary_to_hh(all_vacancies_from_hh):
    all_salary_to_hh = []
    for vacancy in all_vacancies_from_hh:
        # print(all_vacancies_from_hh)
        for salary in vacancy["items"]:
            # print(salary["salary"]["to"])
            try:
                payment = salary["salary"]["to"] * 0.8
                # print(payment)
                # except TypeError:
                #     salary_none = "none"
                all_salary_to_hh.append(payment)
            except TypeError:
                salary_none = "none"

    # print(all_salary_to_hh)
    return all_salary_to_hh


# salary_to_hh = (get_all_salary_to_hh(all_vacancies_from_hh))


def get_average_salary(salary_from, salary_to):
    average_salary = []
    all_salary = list(chain(salary_from, salary_to))
    # print(all_salary)
    average_salary.append(int(sum(all_salary) / len(all_salary)))
    # print(average_salary)
    return average_salary


# avarage_salary = average_salary(salary_from_hh, salary_to_hh)


# print(avarage_salary)


def get_vacancies_processed(salary_from, salary_to):
    vacancies_processed = []
    # print(vacancies_processed)
    merge_salary = list(chain(salary_from, salary_to))
    # print(salary_from)

    vacancies_processed.append(len(merge_salary))
    # print(vacancies_processed)
    return vacancies_processed


# vacancies_processed = vacancies_processed(salary_from_hh, salary_to_hh)


# test = all_vacancies_from_hh[0]
# pprint(test["found"])

def get_vacancies_numbers_hh(all_vacancies_from_hh):
    vacancies_numbers = []
    found_number = all_vacancies_from_hh[0]
    vacancies_numbers.append(found_number["found"])
    return vacancies_numbers


# vacancies_numbers_hh = get_vacancies_numbers_hh(all_vacancies_from_hh)


#
# print(type(language))
# print(type(vacancies_processed))
# print(type(vacancies_numbers_hh))
# print(type(avarage_salary))

def get_all_statistic_hh(language, vacancies_processed, vacancies_numbers_hh, avarage_salary):
    vacancies_statistics_hh = {}
    for processed, found, average in zip(vacancies_processed, vacancies_numbers_hh,
                                         avarage_salary):
        vacancies_statistics_hh[language] = {"vacancies_found": found, "vacancies_processed": processed,
                                             "avarage_salary": average}
    # print(vacancies_statistics_hh)
    return vacancies_statistics_hh


# all_vacancy_statistic_hh = get_all_statistic_hh(language, vacancies_processed, vacancies_numbers_hh, avarage_salary)


#
# print(all_vacancy_statistic_hh)


def unzip_vacancies_dictionary(all_vacancy_statistic_hh):
    # print(all_vacancy_statistic_hh)
    unzipped_all_vacancy_statistic_hh = zip(*all_vacancy_statistic_hh.items())
    all_vacancy_statistic_hh = list(
        zip(*unzipped_all_vacancy_statistic_hh))
    # print(all_vacancy_statistic_hh)
    #
    statisitic_tabs_hh = []
    # print(statisitic_tabs_hh)
    for tab in all_vacancy_statistic_hh:
        statisitic_tabs_hh.append(tab[0])
        for string in tab[1].values():
            statisitic_tabs_hh.append(string)

    final_strings_hh = list(zip(*[iter(statisitic_tabs_hh)] * 4))
    # print(final_strings_hh)
    # print(statisitic_tabs_hh)
    return statisitic_tabs_hh
    # table= unzip_vacancies_dictionary(all_vacancy_statistic_hh)

# def get_date_tabs
columns = ["Язык программирования ", "Вакансий найдено", "Вакансий отработано", "Средняя ЗП"]

# print("test")

# test= [['Python', 1521, 168, 218949],['Javascript', 1936, 174, 183127],['PHP', 1078, 172, 180580]]

def get_data_tabs(unzip_dict,columns):
    # print(unzip_dict)
    # all_table =[]

    data_tabs_hh = [columns, unzip_dict]
    title = 'HH Vacancies'
    table_instance = AsciiTable(data_tabs_hh,title)
    table_instance.justify_columns[1] = 'center'
    # inner_heading_row_border = True
    # print(table_instance.table)



def main():
    programming_languages = ["Python", "Java", "Javascript", "Ruby", "PHP", "C++", "CSS", "C#"]
    for language in programming_languages:
        # print(language)

        all_vacancies_from_hh = get_all_vacancies_from_hh(language)
        salary_from_hh = get_all_salary_from_hh(all_vacancies_from_hh)
        salary_to_hh = get_all_salary_to_hh(all_vacancies_from_hh)

        avarage_salary = get_average_salary(salary_from_hh, salary_to_hh)
        vacancies_processed = get_vacancies_processed(salary_from_hh, salary_to_hh)
        vacancies_numbers_hh = get_vacancies_numbers_hh(all_vacancies_from_hh)
        all_vacancy_statistic_hh = get_all_statistic_hh(language, vacancies_processed, vacancies_numbers_hh,
                                                        avarage_salary)
        # tab in all_vacancy_statistic_hh
        unzip_dict = unzip_vacancies_dictionary(all_vacancy_statistic_hh)
        # print_table(table)
        # get_collect(language)
        get_data_tabs(unzip_dict, columns)
        # tuple1 = tuple(unzip_dict)
        print(unzip_dict)
        # test_tuple = []
        # for i in tuple1:
            # print("test",i)
        # test_tuple.append(tuple1)
        # print(test_tuple)
        # def print_table(table):
        # print(table)
        # get_data_tabs(table, columns)
        # get_vacancies_tab_hh(all_vacancy_statistic_hh)
        # print(unzip_dict)
        # print(type(unzip_dict))
        # print(table)
if __name__ == "__main__":
    main()
