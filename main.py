import requests

from bs4 import BeautifulSoup


print("What key word are you looking for?")
key_word = input(">")
print(f'Searching for  "{key_word}" ...')


html_text = requests.get("https://www.irk.ru/afisha/tours/").text
soup = BeautifulSoup(html_text, "lxml")
events = soup.find_all("li", class_="grid-list__item")
for event in events:
    if event.article:
        event_type = event.find(
            "div", class_="afisha-article__elements").span.text
        if "концерт" in event_type:
            event_link = event.article.header.a["href"]
            event_text = requests.get(f"https://www.irk.ru{event_link}").text
            if key_word in event_text:
                print(event.find("h4", class_="afisha-article__title").a.text.strip())
                print((f"https://www.irk.ru{event_link}"))
