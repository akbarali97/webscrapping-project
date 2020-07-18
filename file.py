from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

f = open("citylist.txt", "r")
lines = f.readlines()
citylist = []
for line in lines:
   citylist.append(line.strip())
f.close()

r_names = []
r_links = []
r_counts = []
driver = webdriver.Chrome("/home/akbar/PROJECTS/webscrapping/chromedriver")
driver.get(f'https://www.zomato.com/{citylist[30]}/restaurants?')
content = driver.page_source
soup = BeautifulSoup(content,features="html5lib")

qq = []
for a in soup.find('div', attrs={'class':'pagination-number'}):
    for q in a.findAll('b'):
        qq.append(str(q.text))
pgs = int(qq[1],10)

for i in range(1,pgs+1):
    driver.get(f'https://www.zomato.com/{citylist[30]}/restaurants?page={i}')
    content = driver.page_source
    soup = BeautifulSoup(content,features="html5lib")
    count = 1
    for a in soup.findAll('a',href=True, attrs={'class':'result-title'}):
        x = str(a.text).strip()
        y = str(a['href']).strip()
        r_names.append(x)
        r_links.append(y)
        


df = pd.DataFrame({'No.':r_counts,'Restaurant Name':r_names,"Link":r_links})
df.to_csv(f'{citylist[30]}.csv', index=False, encoding='utf-8')