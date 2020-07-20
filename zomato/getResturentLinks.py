from selenium import webdriver
from bs4 import BeautifulSoup
import os
import time
import csv
driver = webdriver.Chrome("/home/akbar/PROJECTS/webscrapping/chromedriver")

city = []
with open('zomatocitylist-kerala.csv','r') as f:
    read = csv.reader(f)
    for row in read:
        [r] = row
        city.append(r)
print(city)

