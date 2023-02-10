import requests
import json


LINK = 'https://api.github.com'
USER = 'kataklizm88'


def main(link=LINK, user=USER):
    request = requests.get(f'{link}/users/{user}/repos')
    response = request.json()
    repos = [repo['full_name'].split('/')[1] for repo in response]
    with open('repositories.json', 'w') as file:
        json.dump(f' All repositories of user {user}:{repos}', file)


if __name__ == "__main__":
    main()