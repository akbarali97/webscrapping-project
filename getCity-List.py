from selenium import webdriver
from bs4 import BeautifulSoup
driver = webdriver.Chrome("/home/akbar/PROJECTS/webscrapping/chromedriver")


# initialization
citylist = []
zomato_citylist = []
zomato_kerala_citylist = []
swiggy_citylist = []
swiggy_kerala_citylist = []

def intersection(lst1, lst2):
	temp = set(lst2) 
	lst3 = [value for value in lst1 if value in temp] 
	return lst3 

# getting list of cities  in kerala from wiki
driver.get('https://en.wikipedia.org/wiki/List_of_cities_and_towns_in_Kerala')
content = driver.page_source
soup = BeautifulSoup(content,features="html5lib")
a = soup.find("table")
count = 0
for i in a.findAll("a"):
    if (count%2) == 0:
            citylist.append(i.text+"\n")
    count += 1

f = open("citylist.txt","w")
f.writelines(citylist)
f.close()


# getting list of cities that zomato delivers
driver.get('https://www.zomato.com/delivery-cities')
content = driver.page_source
soup = BeautifulSoup(content,features="html5lib")
for i in soup.findAll("a", href=True, attrs={"class":"cblack"}):
    x = str(i.text).strip()
    zomato_citylist.append(x+"\n")

with open("zomatocitylist.txt", "w+")  as f:
    f.writelines(zomato_citylist)

# getting list of cities that swiggy delivers
driver.get('https://www.swiggy.com/thrissur')
content = driver.page_source
soup = BeautifulSoup(content,features="html5lib")
for i in soup.findAll("a",attrs={"class":"b-Hy9"}):
    x = str(i.text).strip().capitalize()
    # print(x)
    swiggy_citylist.append(x+"\n")

with open("swiggycitylist.txt", "w+")  as f:
    f.writelines(swiggy_citylist)


# getting list of cities that zomato delivers in kerala

zomato_kerala_citylist = intersection(citylist, zomato_citylist)
with open("zomatocitylist-kerala.txt", "w+")  as f:
    f.writelines(zomato_kerala_citylist)

# getting list of cities that swiggy delivers in kerala

swiggy_kerala_citylist = intersection(citylist, swiggy_citylist)
with open("swiggycitylist-kerala.txt", "w+")  as f:
    f.writelines(swiggy_kerala_citylist)
