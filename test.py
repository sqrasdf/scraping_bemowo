from bs4 import BeautifulSoup
import requests
import pyperclip

link_list = [
    "https://www.olx.pl/nieruchomosci/mieszkania/q-mieszkanie-bemowo/?search%5Bfilter_float_price%3Afrom%5D=1000&search%5Bfilter_float_price%3Ato%5D=3000&search%5Border%5D=created_at%3Adesc",
]

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
        offer_link = offer.find("a").get("href")
        offer_link = "https://www.olx.pl" + offer_link
        offer_id = offer.get("id")
        if offer_id not in offers_past:
            print(offer_id, offer_link)


        offers_now.append(offer_id)
        
offers_now = list(set(offers_now))
offers_now.sort()

print("offers_now:", len(offers_now))
print("offers_now set:", len(set(offers_now)))

file = open("file.txt", "w")
for offer in offers_now:
    file.write(offer + "\n")
file.close()

copy_str = "\n".join(offers_now)
pyperclip.copy(copy_str)