import requests
from bs4 import BeautifulSoup
from telegram.ext import *

from constants import API_KEY

# Prompting a key word
print("Hi! \nI'm going to scrape an event section of irk.ru looking for your key word.")
print("What are you looking for?")
key_word = input(" Key word > ")
print(f'Searching for event articles mentioning "{key_word}" . . . ')


# Scrape an event section of irk.ru looking for all concert articles mentioning the key word
html_text = requests.get("https://www.irk.ru/afisha/tours/").text
soup = BeautifulSoup(html_text, "lxml")
events = soup.find_all("li", class_="grid-list__item")
found_info = []
for event in events:
    if event.article:
        event_type = event.find("div", class_="afisha-article__elements").span.text
        if "концерт" in event_type:
            event_link = event.article.header.a["href"]
            event_text = requests.get(f"https://www.irk.ru{event_link}").text
            if key_word in event_text:
                found_info.append(
                    event.find("h4", class_="afisha-article__title").a.text.strip()
                    + f":\nhttps://www.irk.ru{event_link}"
                )


# Set up a Telegram bot
updater = Updater(API_KEY, use_context=True)


# Inform me about all the found concerts via the bot
if found_info:
    updater.bot.send_message(chat_id="-1001775792397", text=f"Анонсы мероприятий, упоминаюшие {key_word}: \n")
    for event in found_info:
        updater.bot.send_message(chat_id="-1001775792397", text=event)
else:
    updater.bot.send_message(chat_id="-1001775792397", text=f"Статьи, упоминаюшие {key_word} не найдены.")
