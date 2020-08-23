# import json
import os
# import base64
import pprint
# import random
import sqlite3
import sys
import time

import requests

from bs4 import BeautifulSoup
# from lxml import etree
from pymongo import MongoClient
from selenium import webdriver
from selenium.common.exceptions import (ElementNotInteractableException,
                                        NoSuchElementException)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import datetime
begin_time = datetime.datetime.now()

client = MongoClient('localhost', 27017)
hotelObject = client.khra.hotels

# setting up Chrome Driver
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
driver = webdriver.Chrome("../chromedriver", options=options)
driver.maximize_window()
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
    return [ dict(zip(columns, row)) for row in cursor.fetchall()]

# # loading links from database to a list.
con = sqlite3.connect("zomato_db.sqlite3")
c = con.cursor()
c.execute("SELECT * FROM hotel_links")
hotels = dictfetchall(c)
con.close()



# visit every link in db and collect data



# # itrating through each hotel in hotels list 
for i in hotels:
    print(i)
    if i['isScaned'] == 'True' : continue
    url = str(i['hotel_link'])
    hl_id = i['hl_id']
    # url = 'https://www.zomato.com/trivandrum/zam-zam-ymr-ambalamukku'
    # url = 'https://www.zomato.com/kozhikode/dominos-pizza-arrakinar'
    driver.get(url)
    # Scrap page-header details
    # get hotel_name
    try:
        hotel_name = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[3]/section/section[1]/h1').text
    except NoSuchElementException as e:
        hotel_name = 'Not Available'

    # get hotel_locality
    try:
        hotel_locality = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[3]/section/section[1]/section[1]/a').text
    except NoSuchElementException as e:
        hotel_locality = 'Not Available'

    # get hotel_cuisines
    try:
        element = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[3]/section/section[1]/section[1]/div').get_attribute("outerHTML")
        soup = BeautifulSoup(element,features="html5lib")
        hotel_cuisines = []
        for i in soup.find_all('a'):
            hotel_cuisines.append(str(i.text))
    except NoSuchElementException as e:
        hotel_cuisines = 'Not Available'

    # get hotel_direction
    try:
        element = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[3]/div[1]/section/a').get_attribute("outerHTML")
        soup = BeautifulSoup(element,features="html5lib")
        hotel_direction = str(soup.find('a')['href'])
    except NoSuchElementException as e:
        hotel_direction = 'Not Available'

    # get hotel_openhours
    try:
        hotel_openhours = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[3]/section/section[1]/section[2]/span[2]').text
    except NoSuchElementException as e:
        hotel_openhours = 'Not Available'

    # get cover images
    try:
        driver.find_elements_by_xpath('//*[@id="root"]/main/div/section[2]//img')
        c_i = True
    except: 
        c_i = False
        cover_images = "Not Available"
        pass

    if c_i:
        cover_images = []
        s = 0
        while True:
            try:
                elements = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="root"]/main/div/section[2]//img')))
                element = elements[s]
                actions = ActionChains(driver)
                actions.move_to_element(element).perform()
                cover_image_url = str(element.get_attribute("src"))
                cover_image = requests.get(cover_image_url,headers={'user-agent': 'Mozilla/5.0 (Linux; U; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13'}).content
                img_filename = url.split('/')[4] + "_coverimage_" + f"{s}" + ".webp"
                with open(f"./images/{img_filename}", "wb") as f:f.write(cover_image)
                cover_images.append(img_filename)
                s = s + 1
            except Exception as e:
                print('cover_image\n')
                print(e)
                break
    else:
        cover_images = 'Not Available'

    # get dining_rating
    try:
        dining_rating = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[3]/section/section[2]/section[1]/div[1]/p').text
    except NoSuchElementException:
        dining_rating = 'Not Available'
        pass

    # get delivery_rating
    try:
        delivery_rating = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[3]/section/section[2]/section[2]/div[1]/p').text
    except NoSuchElementException:
        delivery_rating = 'Not Available'
        pass

    # print(hotel_name)
    # print(hotel_locality)
    # print(hotel_cuisines)
    # print(hotel_direction)
    # print(hotel_openhours)
    # print(dining_rating)
    # print(delivery_rating)

    # overview page scrapping
    try:
        driver.find_element_by_xpath("//*[@id='root']/main//section[@role='tablist']//a[contains(text(),'Overview')]").click()
        el = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/section/section/section/article/section/h3[text()="About this place"]')))
        overview = True
    except Exception as e:
        print(e)
        overview = False
        pass
    if overview:
        # get hotel_phonenumber
        try:
            hotel_phonenumber = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[4]/section/article/p').text
        except:
            pass
        
        # get hotel_address
        try:
            hotel_address = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[4]/section/article/section/p').text
        except:
            pass

        # get cost_for_2
        try:
            cost_for_2 = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[4]/section/section/article[1]/section[1]/p[contains(text(),"₹")]').text
        except:
            pass

        # get payment_methods
        try:
            payment_methods = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[4]/section/section/article[1]/section[1]/p[contains(text(),"accepted")]').text
        except:
            pass

        # get additional_details
        try:
            element = driver.find_element_by_xpath('//*[@id="root"]/main/div/section[4]/section/section/article[1]/section[1]/div[3]').get_attribute("outerHTML")
            soup = BeautifulSoup(element,features="html5lib")
            additional_details = []
            for i in soup.findAll('p'):
                additional_details.append(str(i.text)) 
        except:
            pass
    else:
        additional_details = 'Not Available'
        payment_methods = 'Not Available'
        cost_for_2 = 'Not Available'
        hotel_address = 'Not Available'
        hotel_phonenumber = 'Not Available'


    # # order-page scraping
    try:
        driver.find_element_by_xpath("//*[@id='root']/main//section[@role='tablist']//a[contains(text(),'Order')]").click()
        el = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/section[4]//div[text()="Order Online"]')))
        order = True
    except Exception as e:
        print(e)
        order = False
        pass
    
    if order:
        # # get categories
        c_count = 2
        items = []
        while True:
            try:
                category = driver.find_element_by_xpath(f'//*[@id="root"]/main/div/section[4]/section/section[2]/section[{c_count}]/h4').text
            except:
                break

            item_count = 1
            while True:
                    # get item_name
                    try:
                        # element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="root"]/main/div/section[4]/section/section[2]/section[{c_count}]/div[2]/div[{item_count}]/div/div//h4')))
                        element = driver.find_element_by_xpath(f'//*[@id="root"]/main/div/section[4]/section/section[2]/section[{c_count}]/div[2]/div[{item_count}]/div/div//h4')
                        actions = ActionChains(driver)
                        actions.move_to_element(element).perform()
                        item_name = element.text
                    except Exception as e:
                        break
                    
                    # get item_price
                    try:
                        item_price = driver.find_element_by_xpath(f'//*[@id="root"]/main/div/section[4]/section/section[2]/section[{c_count}]/div[2]/div[{item_count}]//span[contains(text(),"₹")]').text
                    except NoSuchElementException as e:
                        item_price = 'Not Available'
                        pass

                    # get item_image
                    try:
                        driver.find_element_by_xpath(f'//*[@id="root"]/main/div/section[4]/section/section[2]/section[{c_count}]/div[2]/div[{item_count}]//img')
                        iimg = True
                    except:
                        iimg = False
                        pass
                    if iimg:
                        try:
                            element = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="root"]/main/div/section[4]/section/section[2]/section[{c_count}]/div[2]/div[{item_count}]//img')))
                            actions = ActionChains(driver)
                            actions.move_to_element(element).perform()
                            item_image_url = str(element.get_attribute("src")).split('?')[0]
                            item_image = requests.get(item_image_url,headers={'user-agent': 'Mozilla/5.0 (Linux; U; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13'}).content
                            img_filename = url.split('/')[4] + "_item_image_" + item_name + ".webp"
                            with open(f"./images/{img_filename}", "wb") as f:f.write(item_image)
                            item_image = img_filename
                        except:
                            pass
                    else:
                        item_image = 'Not Available'

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
                        isItem_customizable = False
                        pass

                    # open customisations popup menu
                    if isItem_customizable == True:
                        addons = []
                        try:
                            element = driver.find_element_by_xpath(f'//*[@id="root"]/main/div/section[4]/section/section[2]/section[{c_count}]/div[2]/div[{item_count}]//span[contains(text(),"Add")]')
                            actions = ActionChains(driver)
                            actions.move_to_element(element).click().perform()
                            el = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, f'/html/body//div/div[2]/section[2]/div/div/button//span[text()="Add to order"]')))
                            c = 3
                            while True:
                                # get addon_header_name
                                try:
                                    # addon_header_name = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, f"/html/body//div/div[2]/section[2]/div/div[{c}]/div[1]/div[1]"))).text
                                    addon_header_name = driver.find_element_by_xpath(f"/html/body//div/div[2]/section[2]/div/div[{c}]/div[1]/div[1]").text
                                except:
                                    break

                                # get addon_header_discription
                                try:
                                    addon_header_discription = driver.find_element_by_xpath(f"/html/body//div/div[2]/section[2]/div/div[{c}]/div[1]/div[2]/div[1]").text
                                except:
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
                                for q in reversed(elementX):
                                    try:
                                        # actions = ActionChains(driver)
                                        # actions.move_to_element(q).click().perform()
                                        q.click()
                                    except Exception as e:
                                        print(e)
                                        pass
                            except Exception as e:
                                print(e)
                                print('addon not closable')
                                break
                        except Exception as e:
                            print(f"addon of {item_count}")
                            print(e)
                            break
                    else:
                        addons = "Not Available"
                    # print(addons)
                    # create a menu_items object
                    item = {
                        "item_name": item_name,
                        "item_price": item_price,
                        "item_category": category,
                        "item_type": item_type,
                        "item_image": item_image,
                        "item_votes": item_votes,
                        "item_discription":item_discription,
                        "isItem_customizable":isItem_customizable,
                        "addons":addons,
                    }
                    items.append(item)
                    item_count = item_count + 1        
            c_count = c_count + 1
    else:
        items = 'Not Available'

    # photos-page scraping
    try:
        driver.find_element_by_xpath("//*[@id='root']/main//section[@role='tablist']//a[contains(text(),'Photos')]").click()
        el = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/section[4]//h4[contains(text(),"Photos")]')))
        Photos = True
    except Exception as e:
        print(e)
        Photos = False
        images = "Not Available"
        pass
    
    if Photos:
        images = []
        s = 0
        while True:
            try:
                # elements = WebDriverWait(driver, 7).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="root"]/main/div/section[4]/div/div[2]/div//img')))
                # element = elements[s]
                element = driver.find_elements_by_xpath('//*[@id="root"]/main/div/section[4]/div/div[2]/div//img')[s]
                actions = ActionChains(driver)
                actions.move_to_element(element).perform()
                el = WebDriverWait(driver, 4).until(EC.visibility_of(element))
                image_url = str(element.get_attribute("src")).split('?')[0]
                image = requests.get(image_url,headers={'user-agent': 'Mozilla/5.0 (Linux; U; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13'}).content
                img_filename = url.split('/')[4] + "_image_" + f"{s}" + ".webp"
                with open(f"./images/{img_filename}", "wb") as f:f.write(image)
                images.append(img_filename)
                s = s + 1
            except Exception as e:
                print('photos-page')
                print(e)
                break
    else:
        images = 'Not Available'
            

    # # reviews-page scrapping
    try:
        driver.find_element_by_xpath("//*[@id='root']/main//section[@role='tablist']//a[contains(text(),'Reviews')]").click()
        el = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/section[4]//h4[text()="Reviews"]')))
        Review = True
    except:
        Review = False
        Reviews = "Not Available"
        pass
    if Review:
        # get list of all review-blocks and itrate through each review
        Reviews, reviewer, review, rating = [],[],[],[]
        t = 2
        flag = 0
        while True:
            # wait to load
            try:
                element = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="root"]/main/div/section[4]/div/div/section[2]/div[3]/div[2]/div')))
                # element = driver.find_elements_by_xpath('//*[@id="root"]/main/div/section[4]/div/div/section[2]/div[3]/div[2]/div')
                actions = ActionChains(driver)
                actions.move_to_element(element).perform()
            except:
                pass

            # get reviewer name
            try:
                elements = driver.find_elements_by_xpath('//*[@id="root"]/main/div/section[4]/div/div/section[2]/div[2]//div/div/a/p')
                # elements = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="root"]/main/div/section[4]/div/div/section[2]/div[2]//div/div/a/p')))
                for x in elements:
                    reviewer.extend([x.text])
            except :
                pass
            # get review
            try:
                elements = driver.find_elements_by_xpath('//*[@id="root"]/main/div/section[4]/div/div/section[2]/div[2]/p')
                # elements = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="root"]/main/div/section[4]/div/div/section[2]/div[2]/p')))
                for x in elements:
                    review.extend([x.text])
            except:
                pass
            # get rating
            try:
                elements = driver.find_elements_by_xpath('//*[@id="root"]/main/div/section[4]/div/div/section[2]/div[2]//section/div/p')
                # elements = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="root"]/main/div/section[4]/div/div/section[2]/div[2]//section/div/p')))
                for x in elements:
                    rating.extend([x.text])
            except :
                pass
            # go to next review-page
            try:
                if flag == 0:
                    element = driver.find_elements_by_xpath('//*[@id="root"]/main/div/section[4]/div/div/section[2]/div[3]/div[2]/div/a/i')[0]
                    actions = ActionChains(driver)
                    actions.move_to_element(element).click().perform()
                    flag = 1
                else:
                    element = driver.find_elements_by_xpath('//*[@id="root"]/main/div/section[4]/div/div/section[2]/div[3]/div[2]/div/a/i')[1]
                    actions = ActionChains(driver)
                    actions.move_to_element(element).click().perform()
            except Exception as e:
                print('review-page')
                print(e)
                break     
            
            # create a review object and add it to Reviews list
            Reviews = [{"reviewer":i,"review":j,"rating":k} for i, j, k in zip(reviewer,review,rating)]
    else:
        Reviews = 'Not Available'
    # pprint.pprint(Reviews)
    # print (len(reviewer))


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
        "cover_images":cover_images,
        "dining_rating":dining_rating,
        "delivery_rating":delivery_rating,
        "cost_for_2":cost_for_2,
        "payment_methods":payment_methods,
        "additional_details":additional_details,
        "items":items,
        "images":images,
        "Reviews":Reviews
    }
    pprint.pprint(hotel_object)

    # insert data into db
    try:
        zx = hotelObject.insert_one(hotel_object)
    except Exception as e:
        print(e)
        pass

    # update the isScaned status to True
    try:
        with sqlite3.connect('zomato_db.sqlite3') as con:
            con.execute(f"UPDATE hotel_links SET isScaned = 'True' WHERE hl_id = {hl_id}")
    except Exception as e:
        print(e)
    finally:
        con.close()

    # con = sqlite3.connect("zomato_db.sqlite3")
    # c = con.cursor()
    # stat = 'True'
    # query = f"UPDATE hotel_links SET isScaned = 'True' WHERE hotel_link = {url}"
    # c.execute(query)
        
# # finally close the driver and exit the program
driver.close()
print(datetime.datetime.now() - begin_time)
sys.exit()
