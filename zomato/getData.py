from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException , ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
import requests
import random
import sqlite3
import time
import sys
import json
import os
import base64
from lxml import etree
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
driver = webdriver.Chrome("../chromedriver", options=options)
driver.maximize_window()

# # itrating through each hotel in hotels list 
for i in hotels[1:2]:
    if i['isScaned'] == 'True' : continue
    # url = str(i['hotel_link'])
    url = 'https://www.zomato.com/trivandrum/zam-zam-ymr-ambalamukku'
    # driver.get(url)

    # Scrap page-header details
    # get hotel_name
    try:
        element = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[3]/section/section[1]/h1').get_attribute("outerHTML")
        soup = BeautifulSoup(element,features="html5lib")
        hotel_name = str(soup.text)
        print(hotel_name)
    except NoSuchElementException as e:
        print("hotel_name not found")
        hotel_name = ''

    # get hotel_locality
    try:
        element = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[3]/section/section[1]/section[1]/a').get_attribute("outerHTML")
        soup = BeautifulSoup(element,features="html5lib")
        hotel_locality = str(soup.text)
        print(hotel_locality)
    except NoSuchElementException as e:
        print("hotel_locality not found")
        hotel_locality = ''

    # get hotel_cuisines
    try:
        element = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[3]/section/section[1]/section[1]/div').get_attribute("outerHTML")
        soup = BeautifulSoup(element,features="html5lib")
        hotel_cuisines = []
        for i in soup.find_all('a'):
            hotel_cuisines.append(str(i.text))
        print(hotel_cuisines)
    except NoSuchElementException as e:
        print("hotel_cuisines not found")
        hotel_cuisines = ''

    # get hotel_direction
    try:
        element = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[3]/div[1]/section/a').get_attribute("outerHTML")
        soup = BeautifulSoup(element,features="html5lib")
        hotel_direction = str(soup.find('a')['href'])
        print(hotel_direction)
    except NoSuchElementException as e:
        print("hotel_direction not found")
        hotel_direction = ''

    # get hotel_openhours
    try:
        element = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[3]/section/section[1]/section[2]/span[2]').get_attribute("outerHTML")
        soup = BeautifulSoup(element,features="html5lib")
        hotel_openhours = str(soup.text)
        print(hotel_openhours)
    except NoSuchElementException as e:
        print("hotel_openhours not found")
        hotel_openhours = ''

    # get cover images
    try:
        actions = ActionChains(driver)
        driver.implicitly_wait(1)
        cover_images = []
        for j in driver.find_elements_by_xpath('//*[@id="root"]/main/div/section[2]//img'):
            actions.move_to_element(j).perform()
            cover_image_url = str(j.get_attribute("src"))
            cover_image = base64.b64encode(requests.get(cover_image_url,headers={'user-agent': 'Mozilla/5.0 (Linux; U; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13'}).content)
            cover_images.append(cover_image)
    except NoSuchElementException as e:
        cover_images = 'Not Available'
        pass


    # overview page scrapping
    try:
        driver.find_element_by_xpath("//*[@id='root']/main//section[@role='tablist']//a[contains(text(),'Overview')]").click()
        overview = True
    except (NoSuchElementException,ElementNotInteractableException):
        overview = False
        pass
    # if str(driver.current_url) == url:
    if overview:
        # get hotel_phonenumber
        try:
            element = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[4]/section/article/p').get_attribute("outerHTML")
            soup = BeautifulSoup(element,features="html5lib")
            hotel_phonenumber = str(soup.text)
            print(hotel_phonenumber)
        except NoSuchElementException as e:
            print("hotel_name not found")
            hotel_phonenumber = ''
        
        # get hotel_address
        try:
            element = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[4]/section/article/section/p').get_attribute("outerHTML")
            soup = BeautifulSoup(element,features="html5lib")
            hotel_address = str(soup.text)
            print(hotel_address)
        except NoSuchElementException as e:
            print("hotel_address not found")
            hotel_address = ''

        # get cost_for_2
        try:
            element = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[4]/section/section/article[1]/section[1]/p[2]').get_attribute("outerHTML")
            soup = BeautifulSoup(element,features="html5lib")
            cost_for_2 = str(soup.text)
            print(cost_for_2)
        except NoSuchElementException as e:
            print("cost_for_2 not found")
            cost_for_2 = ''

        # get payment_methods
        try:
            element = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[4]/section/section/article[1]/section[1]/p[4]').get_attribute("outerHTML")
            soup = BeautifulSoup(element,features="html5lib")
            payment_methods = str(soup.text)
            print(payment_methods)
        except NoSuchElementException as e:
            print("cost_for_2 not found")
            payment_methods = ''

        # get additional_details
        try:
            element = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[4]/section/section/article[1]/section[1]/div[3]').get_attribute("outerHTML")
            soup = BeautifulSoup(element,features="html5lib")
            additional_details = []
            for i in soup.findAll('p'):
                additional_details.append(str(i.text)) 
            print(additional_details)
        except NoSuchElementException as e:
            print("additional_details not found")
            additional_details = ''

        
    # # order-page scraping
    # driver.get(url+'/order')
    try:
        driver.find_element_by_xpath("//*[@id='root']/main//section[@role='tablist']//a[contains(text(),'Order')]").click()
        time.sleep(2)
        order = True
    except (NoSuchElementException,ElementNotInteractableException):
        order = False
        pass
    # if str(driver.current_url) == url+'/order':
    if order:
        # # get categories
        c_count = 2
        items = []
        while True:
            try:
                element = driver.find_element_by_xpath(f'//*[@id="root"]/main/div/section[4]/section/section[2]/section[{c_count}]/h4')
                category = element.text
                # print(category)
            except NoSuchElementException as e:
                break

            item_count = 1
            while True:
                    # get item_name
                    try:
                        element = driver.find_element_by_xpath(f'//*[@id="root"]/main/div/section[4]/section/section[2]/section[{c_count}]/div[2]/div[{item_count}]/div/div//h4')
                        actions = ActionChains(driver)
                        actions.move_to_element(element).perform()
                        item_name = element.text
                    except NoSuchElementException as e:
                        break
                    
                    # get item_price
                    try:
                        item_price = driver.find_element_by_xpath(f'//*[@id="root"]/main/div/section[4]/section/section[2]/section[{c_count}]/div[2]/div[{item_count}]//span[contains(text(),"₹")]').text
                    except NoSuchElementException as e:
                        item_price = 'Not Available'
                        pass

                    # get item_image
                    try:
                        element = driver.find_element_by_xpath(f'//*[@id="root"]/main/div/section[4]/section/section[2]/section[{c_count}]/div[2]/div[{item_count}]//img')
                        actions = ActionChains(driver)
                        actions.move_to_element(element).perform()
                        driver.implicitly_wait(1)
                        item_image_url = str(element.get_attribute("src")).split('?')[0]
                        item_image = base64.b64encode(requests.get(item_image_url,headers={'user-agent': 'Mozilla/5.0 (Linux; U; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13'}).content)
                    except NoSuchElementException as e:
                        item_image_url = 'Image Not Available'
                        pass

                    # get item_type
                    try:
                        element = driver.find_element_by_xpath(f'//*[@id="root"]/main/div/section[4]/section/section[2]/section[{c_count}]/div[2]/div[{item_count}]//div[@type]')
                        item_type = element.get_attribute("type")
                    except NoSuchElementException as e:
                        item_type = 'Not Available'
                        pass
                    
                    # get item_discription
                    try:
                        element = driver.find_element_by_xpath(f'//*[@id="root"]/main/div/section[4]/section/section[2]/section[{c_count}]/div[2]/div[{item_count}]//p')
                        item_discription = element.text if element.text != '' else 'Discription Not Available'
                    except NoSuchElementException as e:
                        item_discription = 'Discription Not Available'
                        pass

                    # get item_votes
                    try:
                        element = driver.find_element_by_xpath(f'//*[@id="root"]/main/div/section[4]/section/section[2]/section[{c_count}]/div[2]/div[{item_count}]//span[contains(text(),"votes")]')
                        item_votes = element.text if element.text != '' else 'Votes Not Available'
                    except NoSuchElementException as e:
                        item_votes = 'Votes Not Available'
                        pass
                    
                    # get if item is customizable
                    try:
                        element = driver.find_element_by_xpath(f'//*[@id="root"]/main/div/section[4]/section/section[2]/section[{c_count}]/div[2]/div[{item_count}]/div/div//span[contains(text(),"customizable")]')
                        if element.is_displayed() and element.is_enabled():   isItem_customizable = True
                        else:   isItem_customizable = False
                    except NoSuchElementException:
                        pass

                    # open customisations popup menu
                    if isItem_customizable == True:
                        addons = []
                        try:
                            driver.find_element_by_xpath(f'//*[@id="root"]/main/div/section[4]/section/section[2]/section[{c_count}]/div[2]/div[{item_count}]//span[contains(text(),"Add")]').click()
                            c = 3
                            while True:
                                # get addon_header_name
                                try:
                                    addon_header_name = driver.find_element_by_xpath(f"/html/body//div/div[2]/section[2]/div/div[{c}]/div[1]/div[1]").text
                                except NoSuchElementException:
                                    break

                                # get addon_header_discription
                                try:
                                    addon_header_discription = driver.find_element_by_xpath(f"/html/body//div/div[2]/section[2]/div/div[{c}]/div[1]/div[2]/div[1]").text
                                except NoSuchElementException:
                                    addon_header_discription = "Not Available"
                                    pass
                                
                                t = 1
                                while True:
                                    # get addon_name
                                    try:
                                        addon_name = driver.find_element_by_xpath(f'/html/body//div[{c}]/div[2]/form/div[{t}]/section/label/span').text
                                    except NoSuchElementException:
                                        break
                                    # get addon_type
                                    try:
                                        addon_type = driver.find_element_by_xpath(f'/html/body//div[{c}]/div[2]/form/div[{t}]/section/label/input').get_attribute("type")
                                    except NoSuchElementException:
                                        addon_type = 'Not Available'
                                        pass
                                    
                                    # get addon_price
                                    try:
                                        addon_price = driver.find_element_by_xpath(f'/html/body//div[{c}]/div[2]/form/div[{t}]//div[contains(text(),"₹")]').text
                                    except NoSuchElementException:
                                        addon_price = "Not Available"
                                        pass

                                    addon = {
                                        "addon_header_name":addon_header_name,
                                        "addon_header_discription":addon_header_discription,
                                        "addon_name":addon_name,
                                        "addon_type":addon_type,
                                        "addon_price":addon_price
                                        }
                                    addons.append(addon)
                                    t = t + 1
                                c = c + 1
                            # to close the customizations popup
                            try:
                                elementX = driver.find_elements_by_xpath("/html/body//div/div[2]/section[1]/i")
                                for q in elementX:
                                    try:
                                        q.click()
                                    except ElementNotInteractableException as e:
                                        pass
                            except NoSuchElementException:
                                print("# to close the customizations popup -- error")
                                break
                        except NoSuchElementException:
                            break
                    else:
                        addons = "Addons Not Available"
                    
                    # create a menu_items object
                    item = {
                        "item_name": item_name,
                        "item_price": item_price,
                        "item_category": category,
                        "item_type": item_type,
                        "item_image": item_image,
                        "item_votes": item_votes,
                        "isItem_customizable":isItem_customizable,
                        "addons":addons,
                    }
                    items.append(item)
                    item_count = item_count + 1        
            c_count = c_count + 1

            

    # # photos-page scraping
    try:
        driver.find_element_by_xpath("//*[@id='root']/main//section[@role='tablist']//a[contains(text(),'Photos')]").click()
        time.sleep(2)
        Photos = True
        images = []
    except (NoSuchElementException,ElementNotInteractableException):
        Photos = False
        images = "Not Available"
        pass
    if Photos:
        actions = ActionChains(driver)
        for j in driver.find_elements_by_xpath('//*[@id="root"]/main/div/section[4]/div/div[2]/div//img'):
            actions.move_to_element(j).perform()
            driver.implicitly_wait(1)
            image_url = str(j.get_attribute("src")).split('?')[0]
            image = base64.b64encode(requests.get(image_url,headers={'user-agent': 'Mozilla/5.0 (Linux; U; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13'}).content)
            images.append(image)

    # # reviews-page scrapping
    try:
        driver.find_element_by_xpath("//*[@id='root']/main//section[@role='tablist']//a[contains(text(),'Reviews')]").click()
        # time.sleep(2)
        Review = True
        Reviews = []
    except (NoSuchElementException,ElementNotInteractableException):
        Review = False
        Reviews = "Not Available"
        pass
    if Review:


    # create a hotel_object for inserting into db
    hotel_object = {
        "hotel_name": hotel_name,
        "hotel_cuisines": hotel_cuisines,
        "hotel_link":url,
        "hotel_phonenumber":hotel_phonenumber,
        "hotel_address":hotel_address,
        "hotel_locality":hotel_locality,
        "hotel_direction":hotel_direction,
        "hotel_openhours":hotel_openhours,
    }

    # insert data into db
    zx = hotelObject.insert_one(hotel_object)


# # finally close the driver and exit the program
# driver.close()
sys.exit()