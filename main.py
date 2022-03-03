from bs4 import BeautifulSoup
import requests

# print('What do you search for?')
# key_word = input('>')
# print(f'Serching for  "{key_word}"')
concerts = []

html_text = requests.get('https://www.irk.ru/afisha/tours/').text
soup = BeautifulSoup(html_text, 'lxml')
events = soup.find_all('li', class_ = 'grid-list__item')
for event in events:
    if event.article:
        event_type = event.find('div', class_ = 'afisha-article__elements').span.text.replace('  ', '')
        if 'концерт' in event_type:
            event_name = event.find('h4', class_ = 'afisha-article__title').a.text.replace('  ', '')
            if event_name not in concerts:
                concerts.append(event_name)

for concert in concerts:
    print(concert)