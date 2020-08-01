# from selenium import webdriver
from bs4 import BeautifulSoup
import sqlite3
import time
import requests
import random
from headers import headers
# driver = webdriver.Chrome("../chromedriver")


header = {'User-Agent':random.choice(headers)}

# inserting data into database.
def intoDB(final_list,k):
    try:
        with sqlite3.connect('./zomato/zomato_db.sqlite3') as con:
            con.executemany("""INSERT INTO 
            hotel_links(city_id,city_name,locality,hotel_name,hotel_link) 
            values (?,?,?,?,?)""", final_list)
            con.execute(f"UPDATE avail_cities_kerala SET isScaned = 'True' WHERE id = {k}")
    except sqlite3.IntegrityError:
        print("integrity Error")
        con.rollback()
    finally:
        con.close()

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# retriving city list from db
con = sqlite3.connect("swiggy_db.sqlite3")
c = con.cursor()
c.execute("SELECT * FROM avail_cities_kerala")
City = dictfetchall(c)
con.close()


for i in City[9:10]:
    if i['isScaned'] == 'True' : continue
    j = str(i["city"]).lower()
    k = i["id"]
    pgs = []
    l = []
    url = f"https://www.swiggy.com/{j}?page=1"
    rspns = requests.get(url,headers=header)
    content = rspns.content 
    soup = BeautifulSoup(content,features="html5lib")
    # with open(f"{j}.html","w+") as f: f.write(str( soup.prettify() ) )
    if len(soup.findAll("a", href=True, attrs={"class":"_15mJL"})) != 0:
        for a in soup.findAll("a", href=True, attrs={"class":"_15mJL"}):
            x = str(a["href"])
            if x.find('www.swiggy.com') == -1:
                x = 'https://www.swiggy.com' + x
                l.append(x)
        
    if len(l) == 0:
        for i in soup.findAll("a", href=True,attrs={"class":"_1FZ7A"}): pgs.append(i['href'])
        for i in soup.findAll("a", href=True, attrs={"class":"_1j_Yo"}):
            link = i.find('div',attrs={"class":"nA6kb"})
            print(str(link.text).strip() + ' => ' + str(link['href']))
        
    else:
        for i in l:
            rspns = requests.get(i,headers=header)
            content = rspns.content 
            soup = BeautifulSoup(content,features="html5lib")



    

