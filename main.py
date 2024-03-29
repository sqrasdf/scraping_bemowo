from bs4 import BeautifulSoup
import requests
from datetime import datetime
import telegram
import asyncio
import os 
from dotenv import load_dotenv

link_list = [
    "https://www.olx.pl/nieruchomosci/mieszkania/q-mieszkanie-bemowo/?search%5Bfilter_float_price%3Afrom%5D=1000&search%5Bfilter_float_price%3Ato%5D=3000&search%5Border%5D=created_at%3Adesc",
]

bad_words = [
    
]

# get hidden values
load_dotenv()
TOKEN = os.environ.get("TOKEN")
sqr_id = os.environ.get("sqr_id")
group_id = os.environ.get("group_id")

async def sendNotification(message):
    bot = telegram.Bot(token=TOKEN)
    task_message = asyncio.create_task(bot.send_message(chat_id=group_id, text=message))
    res_message = await task_message


# read previous data from txt file
file = open("file.txt", "r")
file_text = file.read()
offers_past = file_text.split("\n")
file.close()

# get current ids of offers
offers_now = []

for link in link_list:
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, "lxml")
    offers = soup.find("div", class_='css-oukcj3').find_all("div", class_="css-1sw7q4x")

    for offer in offers:
        offer_name = offer.find("h6", class_ = "css-16v5mdi er34gjf0").text


        # checking if title has no bad words
        if not any(bad_word in offer_name.lower() for bad_word in bad_words):    
            
            offer_link = offer.find("a").get("href")
            offer_link = "https://www.olx.pl" + offer_link
            offer_id = offer.get("id")

            # comparing current and past ids
            if offer_id not in offers_past:
                print("notifying about: " + offer_name + " " + offer_id)
                asyncio.run(sendNotification(offer_name + "\n" + offer_link))

            offers_now.append(offer_id)

offers_now = offers_now + offers_past
offers_now = list(set(offers_now))
offers_now.sort()
file = open("file.txt", "w")
for offer in offers_now:
    file.write(offer + "\n")
file.close()


# now = datetime.now()
# current_time = now.strftime("%H:%M:%S")
# asyncio.run(sendNotification("good file, time: " + current_time))