from bs4 import BeautifulSoup as bs
from requests import get
import json

SITE = 'Headhunter.ru'
URL_HH = 'https://spb.hh.ru/search/vacancy?'
headers = {
    "User-Agent":
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        ' Chrome/108.0.0.0 YaBrowser/23.1.1.1138 Yowser/2.5 Safari/537.36'
}
params_hh = {
    'text': 'python',
    'area': 2,
    'salary': 20000,
    'ored_clusters': 'true',
    'enable_snippets': 'true',
    'items_on_page': 20
}
"""
Функция salary_format обрабатывает поле "зарплата" в зависимости от его значения
"""


def salary_format(salary=None):
    result = {}
    res = []
    for i in salary.split():
        try:
            res.append(int(i))
        except ValueError:
            pass
    if len(res) == 0:
        result = salary
    elif len(res) == 1:
        result['зарплата'] = res[0]
    elif len(res) == 2:
        result['минимальная зарплата'] = res[0]
        result['максимальная зарплата'] = res[1]
    return result


"""
Функция parse_hh парсит все страницы сайта Headhunter.ru, которые находит по ключевому слову "python"
и записывает результаты в json-файл
Параметр page_limit устанавливает кол-во страниц, по которым пройдет парсер для сбора данных,
по умолчанию равен 2
"""


def parse_hh(page_limit=2):
    result_list = []
    page = 0
    while page_limit > page:
        params_hh['page'] = page
        response = get(url=URL_HH, headers=headers, params=params_hh)
        soup = bs(response.text.replace('\xa0', '').replace('\u202f', ''), 'html.parser')
        vacancy_name = soup.find_all('a', {'class': 'serp-item__title'})
        salary = soup.find_all('h3', {'class': 'bloko-header-section-3'})
        company_name = soup.find_all('a', {'class': 'bloko-link bloko-link_kind-tertiary'})
        if len(vacancy_name) > 0:
            for i in range(len(vacancy_name) - 1):
                res = {}
                res['название вакансии'] = vacancy_name[i].text
                res['ссылка'] = vacancy_name[i]['href']
                res['название компании'] = company_name[i].text
                res['зарплата'] = salary_format(salary[i].next_sibling.next_sibling.text) \
                    if salary[i].next_sibling.next_sibling.text else 'зарплата не указана'
                res['взято с сайта'] = SITE
                result_list.append(res)
            page += 1
        else:
            break
    return result_list


SITE_RABOTA_RU = 'spb.rabota.ru'
URL_S = 'https://spb.rabota.ru'
params_rabota = {'query': 'python', 'sort': 'relevance'}
"""
Функция parse_hh парсит все страницы сайта Headhunter.ru, которые находит по ключевому слову "python"
и записывает результаты в json-файл
Параметр page_limit устанавливает кол-во страниц, по которым пройдет парсер для сбора данных,
по умолчанию равен 2
"""


def parse_rabota_ru(page_limit=2):
    result_list = []
    page = 0
    while page_limit > page:
        params_rabota['page'] = page
        response = get(url=f'{URL_S}/vacancy/?',
                       headers=headers,
                       params=params_rabota)
        soup = bs(response.text, 'html.parser')
        vacancy_name = soup.find_all('h3',
                                     {'class': 'vacancy-preview-card__title'})
        vacancy_name = [i.text.replace('\n', '').replace('  ', '') for i in vacancy_name]
        vacancy_link = soup.find_all('a', {'class': 'vacancy-preview-card__title_border'})
        vacancy_link = [URL_S + i['href'] for i in vacancy_link]
        salary = soup.find_all('a', {'itemprop': 'title'})
        company_name = soup.find_all('a', {'itemprop': 'name'})
        company_name = [i.text.replace('\n', '').replace('  ', '') for i in company_name]
        if len(vacancy_name) > 0:
            for i in range(len(vacancy_name) - 1):
                res = {}
                res['название вакансии'] = vacancy_name[i]
                res['ссылка'] = vacancy_link[i]
                res['название компании'] = company_name[i]
                res['зарплата'] = salary_format(salary[i].text.replace('\xa0', ''))
                res['взято с сайта'] = SITE_RABOTA_RU
                result_list.append(res)
            page += 1
        else:
            break
    return result_list


def main(*args):
    final_result = []
    for i in args:
        final_result += i()
    # final_result = args[0]()
    with open('result_new.json', 'w', encoding='utf-8') as file:
        json.dump(final_result, file, ensure_ascii=False, indent=6)


if __name__ == '__main__':
    main(parse_hh, parse_rabota_ru)
