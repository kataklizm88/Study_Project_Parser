import requests
from datetime import date


LINK = 'http://api.openweathermap.org/data/2.5/weather?id=524901'
key = '99f2512a7d14f5e7c452c5ae7274efdb'
params = {'q': 'Volhov',
          'appid': key,
          'lang': 'ru'
          }


def main(_params: dict):
    request = requests.get(url=LINK, params=_params)
    response = request.json()
    city_name = response['name']
    current_date = date.fromtimestamp(response['dt'])
    current_temperature = round(273.15 - (response['main']['temp']), 1)
    with open('response.txt', 'w', encoding='utf-8') as file:
        file.write(f'Температура в городе {city_name} на {current_date} составляет {current_temperature} градусов')


if __name__ == '__main__':
    main(params)