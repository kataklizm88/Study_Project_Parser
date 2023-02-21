from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from Lesson_3.task import parse_hh, parse_rabota_ru


def get_parse_hh():
    return parse_hh(page_limit=1)


def get_parse_rabota_ru():
    return parse_rabota_ru(page_limit=1)


def connect_to_db_collection():
    client = MongoClient('mongodb://localhost:27017')
    db = client['test_homework']
    vacancion_collection = db.vacancies
    return vacancion_collection


def add_data_from_hh_to_db(data):
    vacancion_collection = connect_to_db_collection()
    for item in data:
        try:
            if len(list(vacancion_collection.find({'ссылка': item['ссылка']}))) == 0:
                vacancion_collection.insert_one(item)
            else:
                print(f'Значение вакансии {item["название вакансии"]} уже существует')
        except DuplicateKeyError:
            print(f'Значение с таким id {item["_id"]} уже существует')


"""
Сайт работа.ру постоянно генерирует новую ссылку на одну и ту вакансию,
поэтому для поиска уже занесенных в БД вакансий мы будет извлекать из урла
номер вакансии, т.к он не меняется в отличие от всей ссылки
"""


def get_number_from_link(link: str):
    result = []
    for i in link.split('/'):
        try:
            result.append(int(i))
        except ValueError:
            pass
    return result[0]


def add_data_from_rabota_ru_to_db(data):
    vacancion_collection = connect_to_db_collection()
    for item in data:
        item['номер ссылки'] = get_number_from_link(item['ссылка'])
        try:
            if len(list(vacancion_collection.find({'номер ссылки': item['номер ссылки']}))) == 0:
                vacancion_collection.insert_one(item)
            else:
                print(f'Значение вакансии {item["название вакансии"]} уже существует')
        except DuplicateKeyError:
            print(f'Значение с таким id {item["_id"]} уже существует')


def find_vacancy():
    while True:
        salary = input('Введите желаемую зарплату ')
        try:
            salary = int(salary)
            break
        except ValueError:
            print('Надо ввести число')
    vacancion_collection = connect_to_db_collection()
    find_vacancies = vacancion_collection.find({'$or': [{'зарплата.зарплата': {'$gt': salary}},
                                                          {'зарплата.минимальная зарплата': {'$gt': salary}},
                                                          {'зарплата.максимальная зарплата': {'$gt': salary}}]})
    res = [i for i in list(find_vacancies)]
    print(f' Список вакансий с подходящей зарплатой: {res}')


def main():
    hh = get_parse_hh()
    rabota_ru = get_parse_rabota_ru()
    add_data_from_hh_to_db(hh)
    add_data_from_rabota_ru_to_db(rabota_ru)
    find_vacancy()


if __name__ == '__main__':
    main()




