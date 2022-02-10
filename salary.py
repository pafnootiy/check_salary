import requests
from pprint import pprint

url = "https://api.hh.ru/vacancies/"


def get_pl_response():
    pl = ["Python", "Java", "Javascript", "Ruby", "PHP", "C++", "CSS", "C#"]
    all_lg_resonse = []
    for i in pl:
        # print(i)
        payload = {
            "text": f"{i}",
            "area": "1",
            "currency": "RUR",  # Почему не работает этот параметр ?
            # "salary": 100000,
            # "period": 30,
            "only_with_salary": True
        }
        # print(payload)
        response = requests.get(url, params=payload)
        response.raise_for_status()
        response = response.json()
        all_lg_resonse.append(response)

    return all_lg_resonse


vacancy_response = get_pl_response()  # mvp


# pprint(vacancy_response)


def get_avarage_salary(vacancy_response):
    pl = ["Python", "Java", "Javascript", "Ruby", "PHP", "C++", "CSS", "C#"]
    salary = []
    avarage_salary = []
    vacancies_processed = []
    vacancies_found = []
    for name_pl in pl:
        salary = []
        for i in vacancy_response:
            for k in i["items"]:
                if f"{name_pl}" in k["name"]:
                    try:
                        if k["salary"]["currency"] == "RUR":
                            salary_from = k["salary"]["from"] * 1.2
                            salary.append(salary_from)
                        else:
                            salary_to = k["salary"]["to"] * 0.8
                            salary.append(salary_to)
                    except TypeError:
                        salary_none = "none"
                        # print("nono")
        avarage_salary.append(int(sum(salary) / len(salary)))
        # print(int(sum(avarage_salary) / len(avarage_salary)))

        vacancies_processed.append(len(salary))

    for i in vacancy_response:
        vacancies_found.append(i["found"])
    print(pl)
    print(vacancies_processed)
    print(vacancies_found)
    print(avarage_salary)



get_avarage_salary(vacancy_response)  # MVP
