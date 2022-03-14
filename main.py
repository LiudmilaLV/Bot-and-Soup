import json
import os

import requests
from bs4 import BeautifulSoup
from telegram.ext import *


def main():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(current_dir, "settings.json")) as f:
        settings = json.loads(f.read())

    key_word = settings["key_word"]

    # Scrape an event section of irk.ru looking for all concert articles mentioning the key word
    html_text = requests.get("https://www.irk.ru/afisha/tours/").text
    soup = BeautifulSoup(html_text, "lxml")
    events = soup.find_all("li", class_="grid-list__item")
    found_info = []
    for event in events:
        if not event.article:
            continue

        event_type = event.find("div", class_="afisha-article__elements").span.text
        if "концерт" not in event_type:
            continue

        event_link = event.article.header.a["href"]
        event_text = requests.get(f"https://www.irk.ru{event_link}").text
        if key_word in event_text:
            found_info.append(
                event.find("h4", class_="afisha-article__title").a.text.strip() + f":\nhttps://www.irk.ru{event_link}"
            )

    # Set up a Telegram bot
    updater = Updater(settings["api_key"], use_context=True)

    # Inform me about all the found concerts via the bot
    if found_info:
        updater.bot.send_message(chat_id=settings["chat_id"], text=f"Анонсы мероприятий, упоминаюшие {key_word}: \n")
        for event in found_info:
            updater.bot.send_message(chat_id=settings["chat_id"], text=event)


if __name__ == "__main__":
    main()
