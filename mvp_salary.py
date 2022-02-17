import requests
from pprint import pprint
from itertools import count
from terminaltables import AsciiTable
import os
from dotenv import load_dotenv

url = "https://api.hh.ru/vacancies/"
programming_languages = ["Python", "Java", "Javascript", "Ruby", "PHP", "C++", "CSS", "C#"]


def get_all_response_hh(programming_languages):
    all_pages_with_vacancies = []
    for lang in programming_languages:
        try:
            for page in count(0):
                payload = {
                    "text": f"{lang}",
                    "area": "1",
                    "currency": "RUR",  # Почему не работает этот параметр ?
                    "only_with_salary": True,
                    'page': page
                }
                response = requests.get(url, params=payload)
                response.raise_for_status()
                pages_data = response.json()
                all_pages_with_vacancies.append(pages_data)
                # if page > pages_data['pages']:  # почему то возникает ошибка
                if page > 1:
                    break
        except requests.exceptions.HTTPError:
            print("error")
            continue
    return all_pages_with_vacancies


vacancy_response_all_hh = get_all_response_hh(programming_languages)


def get_all_average_salary_hh(vacancy_response_all_hh, programming_languages):
    avarage_salary_hh = []
    vacancies_processed_hh = []
    for language in programming_languages:
        all_salary = []
        for vacancy in vacancy_response_all_hh:
            for average_salary in vacancy["items"]:
                if f"{language}" in average_salary["name"]:
                    try:
                        if average_salary["salary"]["currency"] == "RUR":
                            salary_from = average_salary["salary"]["from"] * 1.2
                            all_salary.append(salary_from)
                        else:
                            salary_to = average_salary["salary"]["to"] * 0.8
                            all_salary.append(salary_to)
                    except TypeError:
                        salary_none = "none"

        avarage_salary_hh.append(int(sum(all_salary) / len(all_salary)))
        vacancies_processed_hh.append(len(all_salary))
    return avarage_salary_hh, vacancies_processed_hh


proccesed_and_average_hh = get_all_average_salary_hh(vacancy_response_all_hh, programming_languages)


def get_all_found_numbers_hh(vacancy_response_all_hh):
    vacancies_found_hh = []
    for i in vacancy_response_all_hh:
        vacancies_found_hh.append(i["found"])
    return vacancies_found_hh


vacancies_numbers_hh = get_all_found_numbers_hh(vacancy_response_all_hh)


def get_all_statistic_hh(programming_languages, proccesed_and_average_hh, vacancies_numbers_hh):
    vacancies_statistics_hh = {}
    for lang, processed, found, average in zip(programming_languages, proccesed_and_average_hh[1], vacancies_numbers_hh,
                                               proccesed_and_average_hh[0]):
        vacancies_statistics_hh[lang] = {"vacancies_found": found, "vacancies_processed": processed,
                                         "avarage_salary": average}
    return vacancies_statistics_hh

all_vacancy_statistic_hh = get_all_statistic_hh(programming_languages, proccesed_and_average_hh, vacancies_numbers_hh)



url_for_autorisation = "https://www.superjob.ru/authorize/"
secret_key = "v3.r.125475457.00923bb2ffcd9caaf26ea06f68d2af4e0f8a883a.9f62c587335b1e2697df5d7f06d971df31eec6e7"

load_dotenv()
secret_key = os.getenv("SJ_TOKEN")
headers = {
    "X-Api-App-Id": secret_key  # позже убрать в енв
}


def get_sj_autorisation(url_for_autorisation, secret_key, headers):
    sj_response = requests.post(url_for_autorisation, headers=headers)
    sj_response.raise_for_status()


sj_autorisation = get_sj_autorisation(url_for_autorisation, secret_key, headers)


def get_response_from_sj(programming_languages, sj_autorisation, headers):
    all_response_js = []
    url_vacancy_sj = "https://api.superjob.ru/2.0/vacancies/"
    for language in programming_languages:
        for page in count(0):
            payload = {'keyword': f"{language}",
                       "town": 4,
                       'page': page
                       }
            sj_vacancy_response = requests.get(url_vacancy_sj, headers=headers, params=payload)
            sj_vacancy_response.raise_for_status()
            sj_vacancy_response = sj_vacancy_response.json()
            all_response_js.append(sj_vacancy_response)
            if page >= 2:
                break

    return (all_response_js)


vacancy_response_all_sj = get_response_from_sj(programming_languages, sj_autorisation, headers)


def get_all_average_salary_sj(vacancy_response_all_sj, programming_languages):
    vacancies_processed_js = []
    avarage_salary_js = []
    salary_js = []
    for languages in programming_languages:
        for i in vacancy_response_all_sj:
            for avarage_salary in i["objects"]:
                if f"{languages}" in avarage_salary["profession"]:
                    if avarage_salary['payment_from'] != 0 or avarage_salary["payment_to"] != 0 and avarage_salary[
                        "currency"] == "rub":
                        try:
                            if avarage_salary["currency"] == "RUR":
                                salary_from_js = avarage_salary['payment_from'] * 1.2
                                salary_js.append(salary_from_js)
                            else:
                                salary_to_js = avarage_salary["payment_to"] * 0.8
                                salary_js.append(salary_to_js)
                        except TypeError:
                            salary_none = "none"
                    else:
                        continue

        avarage_salary_js.append(int(sum(salary_js) / len(salary_js)))
        vacancies_processed_js.append(len(salary_js))

    return avarage_salary_js, vacancies_processed_js


proccesed_and_average_sj = get_all_average_salary_sj(vacancy_response_all_sj, programming_languages)


def get_all_found_numbers_sj(vacancy_response_all_sj, programming_languages):
    number_vacancy_sj = []
    url_for_vacancy = "https://api.superjob.ru/2.0/vacancies/"

    for language in programming_languages:
        payload = {'keyword': f"{language}",
                   "town": 4
                   }
        vacancy_response_all_sj = requests.get(url_for_vacancy, headers=headers, params=payload)
        vacancy_response_all_sj.raise_for_status()
        vacancy_response_all_sj = vacancy_response_all_sj.json()
        number_vacancy_sj.append(vacancy_response_all_sj["total"])

    return number_vacancy_sj


vacancy_numbers_sj = get_all_found_numbers_sj(vacancy_response_all_sj, programming_languages)




def get_all_statistic_sj(programming_languages, proccesed_and_average_sj, vacancy_numbers_sj):
    vacancies_statistics_sj = {}
    for lang_sj, processed_sj, found_sj, average_sj in zip(programming_languages, proccesed_and_average_sj[1],
                                                           vacancy_numbers_sj,
                                                           proccesed_and_average_sj[0]):
        vacancies_statistics_sj[lang_sj] = {"vacancies_found": found_sj, "vacancies_processed": processed_sj,
                                            "avarage_salary": average_sj}
    return vacancies_statistics_sj



all_vacancy_statistic_sj = get_all_statistic_sj(programming_languages, proccesed_and_average_sj, vacancy_numbers_sj)


def get_vacancies_tab_hh(all_vacancy_statistic_hh):
    unzipped_all_vacancy_statistic_hh = zip(*all_vacancy_statistic_hh.items())
    all_vacancy_statistic_hh = list(
        zip(*unzipped_all_vacancy_statistic_hh))
    statisitic_tabs_hh = []
    for tab in all_vacancy_statistic_hh:
        statisitic_tabs_hh.append(tab[0])
        for string in tab[1].values():
            statisitic_tabs_hh.append(string)

    final_strings_hh = list(zip(*[iter(statisitic_tabs_hh)] * 4))

    columns = ["Язык программирования ", "Вакансий найдено", "Вакансий отработано", "Средняя ЗП"]

    data_tabs_hh = []
    data_tabs_hh.append(columns)
    for tab in final_strings_hh:
        data_tabs_hh.append(tab)

    title = 'HH Vacancies'
    table_instance = AsciiTable(data_tabs_hh, title)
    table_instance.justify_columns[1] = 'center'
    print(table_instance.table)


get_vacancies_tab_hh(all_vacancy_statistic_hh)


def get_vacancies_tab_sj(all_vacancy_statistic_sj):
    unzipped_all_vacancy_statistic_sj = zip(*all_vacancy_statistic_sj.items())
    all_vacancy_statistic_sj = list(zip(*unzipped_all_vacancy_statistic_sj))
    statisitic_tabs_sj = []
    for tab in all_vacancy_statistic_sj:
        statisitic_tabs_sj.append(tab[0])
        for string in tab[1].values():
            statisitic_tabs_sj.append(string)

    final_strings_hh = list(zip(*[iter(statisitic_tabs_sj)] * 4))

    columns = ["Язык программирования ", "Вакансий найдено", "Вакансий отработано", "Средняя ЗП"]

    data_tabs_sj = []
    data_tabs_sj.append(columns)
    for tab in final_strings_hh:
        data_tabs_sj.append(tab)

    title = 'SJ Vacancies'
    table_instance = AsciiTable(data_tabs_sj, title)
    table_instance.justify_columns[1] = 'center'
    print(table_instance.table)


get_vacancies_tab_sj(all_vacancy_statistic_hh)

def main():
    url = "https://api.hh.ru/vacancies/"
    programming_languages = ["Python", "Java", "Javascript", "Ruby", "PHP", "C++", "CSS", "C#"]


    # load_dotenv()
    # api_key = os.getenv("NASA_TOKEN")
    # flight_number = 107
    # path_for_images_photos = "photos_from_space/images"
    # path_for_apod_photos = "photos_from_space/apod_pics"
    # path_for_epic_photos = 'photos_from_space/epic_pics'
    # fetch_spacex_last_launch(flight_number, path_for_images_photos)
    # download_apod_photos(api_key, path_for_apod_photos)
    # download_epic_photos(api_key, path_for_epic_photos)


if __name__ == "__main__":
    main()