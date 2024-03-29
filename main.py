from selenium import webdriver
from bs4 import BeautifulSoup
import sqlite3
import time
import sys
driver = webdriver.Chrome("/home/akbar/PROJECTS/webscrapping/chromedriver")

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# retriving city list from db
con = sqlite3.connect("zomato/zomato_db.sqlite3")
c = con.cursor()
c.execute("SELECT * FROM avail_cities_kerala")
City = dictfetchall(c)
con.close()

for i in City:
    if i['isScaned'] == 'True' : continue
    j = i["city"]
    k = i["id"]
    driver.get(f'https://www.zomato.com/{j}/restaurants?')
    content = driver.page_source
    soup = BeautifulSoup(content,features="html5lib")
    qq = []
    for a in soup.find('div', attrs={'class':'pagination-number'}):
        for q in a.findAll('b'):
            qq.append(str(q.text))
    pgs = int(qq[1],10)
    final_list = []
    for ii in range(1,pgs+1):
        time.sleep(3)
        driver.get(f'https://www.zomato.com/{j}/restaurants?page={ii}')
        content = driver.page_source
        soup = BeautifulSoup(content,features="html5lib")
        for a in soup.findAll("div", attrs={"class":"col-s-12"}):
            x = str(a.find("a",href=True, attrs={"class":"result-title"}).text).strip()
            y = str(a.find("a",href=True, attrs={"class":"result-title"})['href']).strip()
            z = str(a.find("a",href=True, attrs={"class":"search_result_subzone"}).text).strip()
            tem_tuple = (k,j,z,x,y)
            final_list.append(tem_tuple)

    # inserting data into database.
    try:
        with sqlite3.connect('./zomato/zomato_db.sqlite3') as con:
            con.executemany("""INSERT INTO 
            hotel_links(city_id,city_name,locality,hotel_name,hotel_link) 
            values (?,?,?,?,?)""", final_list)
            con.execute(f"UPDATE avail_cities_kerala SET isScaned = 'True' WHERE id = {k}")
    except sqlite3.IntegrityError:
        print("integrity Error")
        con.close()
        sys.exit() 
    finally:
        con.close()

