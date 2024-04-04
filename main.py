import requests
from bs4 import BeautifulSoup
import re
import json
from pprint import pprint

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}

response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
vacancy_links = soup.find_all('a', attrs={'href': re.compile('https://spb.hh.ru/vacancy/')})

vacancies_list = []

for link in vacancy_links:
    vacancy_link = link.get('href') 
    response = requests.get(vacancy_link, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    if soup.find('div', attrs={'class': 'vacancy-description'}):
        vacancy_description = soup.find('div', attrs={'data-qa': 'vacancy-description'}).text

        if 'Django' and 'Flask' in vacancy_description:
            vacancy = {}

            vacancy['company_name'] = soup.find('a', attrs={'data-qa': 'vacancy-company-name'}).text.strip()
            if soup.find('div', attrs={'data-qa': 'vacancy-salary'}):
                vacancy['salary'] = soup.find('div', attrs={'data-qa': 'vacancy-salary'}).text.strip()
            else:
                vacancy['salary'] = 'не указана'
            if soup.find('span', attrs={'data-qa': 'vacancy-view-raw-address'}):
                vacancy['city'] = soup.find('span', attrs={'data-qa': 'vacancy-view-raw-address'}).text.split(',')[0]
            else:
                vacancy['city'] = 'не указан'
            vacancy['vacancy_link'] = vacancy_link

            vacancies_list.append(vacancy)
    else:
        print('Нет описания вакансии')

json_list = json.dumps(vacancies_list)
vacancies = json.loads(json_list)
pprint(vacancies)
