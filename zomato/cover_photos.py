from selenium import webdriver
import selenium.common.exceptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import requests
import time

driver = webdriver.Chrome("../chromedriver")
driver.maximize_window()
actions = ActionChains(driver)
url = 'https://www.zomato.com/trivandrum/zam-zam-ymr-ambalamukku'
driver.get(url)


# get cover images
try:
    driver.find_element_by_xpath('//*[@id="root"]/main/div/section[2]//img')
    driver.implicitly_wait(10)
    c_i = True
    cover_images = []
except: 
    c_i = False
    cover_images = "Not Available"
    pass

if c_i:
    s = 0
    while True:
        try:
            element = driver.find_elements_by_xpath('//*[@id="root"]/main/div/section[2]//img')[s]
            actions.move_to_element(element).perform()
            cover_image_url = str(element.get_attribute("src"))
            cover_image = requests.get(cover_image_url,headers={'user-agent': 'Mozilla/5.0 (Linux; U; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13'}).content
            img_filename = url.split('/')[4] + "_coverimage_" + f"{s}" + ".jpeg"
            with open(f"./images/{img_filename}", "wb") as f:f.write(cover_image)
            cover_images.append(img_filename)
            s = s + 1
        except Exception as e:
            print(e)
            break

print(cover_images)