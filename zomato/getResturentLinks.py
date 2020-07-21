from selenium import webdriver
from bs4 import BeautifulSoup
# import scrapy
import os
import time
import csv
import sqlite3
driver = webdriver.Chrome("/home/akbar/PROJECTS/webscrapping/chromedriver")

# def getCityList():
#     city = []
#     with open('zomatocitylist-kerala.csv','r') as f:
#         read = csv.reader(f)
#         for row in read:
#             [row] = row
#             city.append(row)
#     return city

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


con = sqlite3.connect("zomato_db.sqlite3")
c = con.cursor()
c.execute("SELECT * FROM avail_cities_kerala")
City = dictfetchall(c)
con.close()

for i in City:
    j = i["city"]
    k = i["id"]
    url = f"https://www.zomato.com/{j}/restaurants"
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content,features="html5lib")

    qq = []
    for a in soup.find('div', attrs={'class':'pagination-number'}):
    for q in a.findAll('b'):
        qq.append(str(q.text))
    pgs = int(qq[1],10)
    # hotel_name = str(soup.find("h1", attrs={"class":"sc-7kepeu-0"}).text)

