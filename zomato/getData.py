from selenium import webdriver
from bs4 import BeautifulSoup
import requests
# import random
import sqlite3
import time
import sys
# import json
import os
import base64
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
hotelObject = client.khra.hotels

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
# options.add_argument('--headless')

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

# # loading links from database to a list.
con = sqlite3.connect("zomato_db.sqlite3")
c = con.cursor()
c.execute("SELECT * FROM hotel_links")
hotels = dictfetchall(c)
con.close()

# # function to download image
def downimg(url,name,num):
    img = requests.get(url)
    filename = name + str(num)
    with open(f"{filename}.webp", "wb") as f: 
        f.write(img.content)
        f.close()
    return img.content

# visit every link in db and collect data
driver = webdriver.Chrome("../chromedriver", chrome_options=options)
for i in hotels[0:1]:
    # # itrating through each hotel in hotels list 
    if i['isScaned'] == 'True' : continue
    url = str(i['hotel_link'])
    driver.get(url)
    # lastHeight = driver.execute_script("return document.body.scrollHeight")

    title = str(driver.title).split(None)[0]
    if title in ['404', '500']: sys.exit('sraping error')
    content = driver.execute_script("return document.documentElement.outerHTML;")

    # # get hotel_name
    element = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[3]/section/section[1]/h1').get_attribute("outerHTML")
    soup = BeautifulSoup(element,features="html5lib")
    hotel_name = str(soup.text)
    print(hotel_name)
    # # get hotel_phonenumber
    element = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[4]/section/article/p').get_attribute("outerHTML")
    soup = BeautifulSoup(element,features="html5lib")
    hotel_phonenumber = str(soup.text)
    print(hotel_phonenumber)

    # # get hotel_cuisines
    element = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[4]/section/section/article[1]/section[1]/section[2]').get_attribute("outerHTML")
    soup = BeautifulSoup(element,features="html5lib")
    hotel_cuisines = []
    for i in soup.find_all('a'):
        hotel_cuisines.append(str(i.text))
    print(hotel_cuisines)

    # # get hotel_address
    element = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[4]/section/article/section/p').get_attribute("outerHTML")
    soup = BeautifulSoup(element,features="html5lib")
    hotel_address = str(soup.text)
    print(hotel_address)

    # # get hotel_locality
    element = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[3]/section/section[1]/section[1]/a').get_attribute("outerHTML")
    soup = BeautifulSoup(element,features="html5lib")
    hotel_locality = str(soup.text)
    print(hotel_locality)

    # # get hotel_direction
    element = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[3]/div[1]/section/a').get_attribute("outerHTML")
    soup = BeautifulSoup(element,features="html5lib")
    hotel_direction = str(soup.find('a')['href'])
    print(hotel_direction)

    # # get hotel_openhours
    element = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[3]/section/section[1]/section[2]/span[2]').get_attribute("outerHTML")
    soup = BeautifulSoup(element,features="html5lib")
    hotel_openhours = str(soup.text)
    print(hotel_openhours)

    # # get image img
    element = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[2]/div[1]/div/div/img').get_attribute("outerHTML")
    soup = BeautifulSoup(element,features="html5lib")
    imgurl = str(soup.find("img")["src"]).strip()
    img = base64.b64encode(requests.get(imgurl,headers={'user-agent': 'Mozilla/5.0 (Linux; U; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13'}).content)

    # # create a menu_items object
    # menu_items = [
    #     {
    #     "item_name": item_name,
    #     "item_price": item_price,
    #     "item_category": item_category,
    #     "item_type": item_type,
    #     "item_image": item_image,
    #     "item_rating": item_rating
    #     }
    # ]

    # # create a hotel_object for inserting into db
    hotel_object = {
        "hotel_name": hotel_name,
        "hotel_cuisines": hotel_cuisines,
        "hotel_phonenumber":hotel_phonenumber,
        "hotel_address":hotel_address,
        "hotel_locality":hotel_locality,
        "hotel_direction":hotel_direction,
        "hotel_openhours":hotel_openhours,
        "img":img
    }

    # # insert data into db
    zx = hotelObject.insert_one(hotel_object)


# finally close the driver and exit the program
driver.close()
sys.exit()