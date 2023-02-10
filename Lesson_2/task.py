import requests
from lxml import html

"""
Запарсить Dzen.ru не получилось, сайт просто не отдает ни одного элемента
Поэтому для парсенга выбраны порталы РБК и Лента
"""

url_lenta = 'https://lenta.ru'
url_rbk = 'https://www.rbc.ru/short_news'
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                         ' (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.1.1138 Yowser/2.5'
                         ' Safari/537.36'}


def parse_lenta():
    response = requests.get(url=url_lenta, headers=headers)
    dom = html.fromstring(response.text)
    result = {}
    news = dom.xpath("//div[@class='topnews__column']/a")
    for item in news:
        link = url_lenta + item.xpath(".//@href")[0]
        news_name = item.xpath(".//div/span/text()")[0]
        news_time = item.xpath(".//div/div/time/text()")[0]
        result[f'Название новости: {news_name}'] = {'Ссылка': link, 'Время публикации': news_time}
    return f'Главные новости Lenta.ru : {result} \n'


def parse_rbk():
    response = requests.get(url=url_rbk, headers=headers)
    dom = html.fromstring(response.text)
    result = {}
    news = dom.xpath("//div[@class='item__wrap l-col-center']")
    for item in news:
        link = item.xpath(".//a/@href")[1]
        news_time = item.xpath(".//div/span/text()")[0]
        news_name = item.xpath(".//a/span/span/text()")[0]
        news_category = item.xpath(".//div/a/text()")[0]
        news_name = [i for i in str(news_name).split(' ') if i != ''][1:]
        news_name = ' '.join(news_name)
        result[f'Название новости: {news_name}'] = {'Ссылка': link,
                                                    'Время публикации': news_time, 'Рубрика': news_category}
    return f'Главные новости РБК : {result} \n'


def main(*args):
    with open('parsing_news.txt', 'w', encoding='utf-8') as file:
        for i in args:
            file.write(i())


if __name__ == '__main__':
    main(parse_lenta, parse_rbk)
