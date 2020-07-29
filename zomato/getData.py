from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import random
import sqlite3
import time
import sys
import json
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
hotelObject = client.khra.hotels

# headers = [
#     "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/ Safari/530.5",
#     "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13",
#     "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0",
#     "Mozilla/5.0 (Linux; U; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13"
# ]


# # retriving city list from db --sqlite3
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

con = sqlite3.connect("zomato_db.sqlite3")
c = con.cursor()
c.execute("SELECT * FROM hotel_links")
hotels = dictfetchall(c)
con.close()

# visit every link in db and collect data
driver = webdriver.Chrome("../chromedriver")
for i in hotels[0:1]:
    if i['isScaned'] == 'True' : continue
    url = str(i['hotel_link'])
    driver.get(url)
    title = str(driver.title).split(None)[0]
    if title in ['404', '500']: sys.exit('sraping error')
    # content = driver.execute_script("return document.documentElement.outerHTML;")
    content = driver.page_source()
    soup = BeautifulSoup(content,features="html5lib")
    # jn = json.dumps(soup)
    # with open(f"{i['hotel_name']}.json","w+") as f: f.write(jn)
    with open(f"{i['hotel_name']}1.html","w+") as f: f.write(str(soup.prettify()))
    hotel_name = str(soup.find("h1", attrs={"class":"sc-7kepeu-0"}).text)
    hotel_direction = soup.find("h1", attrs={"class":"sc-dvpmds"})
    hotel_direction = str(hotel_direction["href"])
    # print(hotel_name)
    menu_items = [
        {
        "item_name": item_name,
        "item_price": item_price,
        "item_category": item_category,
        "item_type": item_type,
        "item_image": item_image,
        "item_rating": item_rating
        }
    ]
    dict_object = {
        "hotel_name": hotel_name,
        "direction":hotel_direction,
        "image":
    }
    zx = hotelObject.insert_one(dict_object)
    driver.close()


