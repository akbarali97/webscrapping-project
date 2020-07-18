from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time
driver = webdriver.Chrome("/home/akbar/PROJECTS/webscrapping/chromedriver")

links = []
with open('Kunnamkulam.csv', newline='') as csvfile:
    read = csv.reader(csvfile)
    for row in read:
        links.append(row[2])
    links.remove("Link")
    # print(links)

for url in links[0:1]:
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content,features="html5lib")
    hotel_name = str(soup.find("h1", attrs={"class":"sc-7kepeu-0"}).text)
    print(hotel_name)
    with open(f'{hotel_name}.csv', 'w+', newline='') as csvfile:
        fieldnames = ['Dish_Name', 'dish_type','category','dish_price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for a in soup.findAll('section', attrs={"class":"sc-jWojfa WRoJu"}):
            category = a.find('h4',attrs={"class":"sc-1hp8d8a-0"})
            for aa in a.findAll("div", attrs={"class":"sc-1s0saks-15"}):
                dish_type = aa.find("div", attrs={"class":"sc-1tx3445-1 iSPzhY sc-1s0saks-3 bGiihD"})
                dish_type = str(dish_type['type'])
                print(dish_type)
                dish_name = str(aa.find("h4", attrs={"class":"sc-1s0saks-13"}).text)
                print(dish_name)
                dish_price = str(aa.find("span", attrs={"class":"sc-17hyc2s-1"}).text)
                print(dish_price)
                writer.writerow({'Dish_Name':dish_name,"dish_type":dish_type,"category":category,"dish_price":dish_price})
