from selenium import webdriver
import selenium.common.exceptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import pprint
import time

driver = webdriver.Chrome("../chromedriver")
driver.maximize_window()
actions = ActionChains(driver)
url = 'https://www.zomato.com/trivandrum/zam-zam-ymr-ambalamukku'
driver.get(url)

# # reviews-page scrapping
try:
    driver.find_element_by_xpath("//*[@id='root']/main//section[@role='tablist']//a[contains(text(),'Reviews')]").click()
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
        driver.implicitly_wait(10)
        time.sleep(2)
        try:
            element = driver.find_elements_by_xpath('//*[@id="root"]/main/div/section[4]/div/div/section[2]/div[3]/div[2]/div')
            actions.move_to_element(element).perform()
        except:
            pass

        # get reviewer name
        try:
            driver.implicitly_wait(10)
            for x in driver.find_elements_by_xpath('//*[@id="root"]/main/div/section[4]/div/div/section[2]/div[2]//div/div/a/p'):
                # actions.move_to_element(x).perform()
                reviewer.extend([x.text])
        except :
            pass
        # get review
        try:
            driver.implicitly_wait(10)
            for x in driver.find_elements_by_xpath('//*[@id="root"]/main/div/section[4]/div/div/section[2]/div[2]/p'):
                # actions.move_to_element(x).perform()
                review.extend([x.text])
        except:
            pass
        # get rating
        try:
            driver.implicitly_wait(10)
            for x in driver.find_elements_by_xpath('//*[@id="root"]/main/div/section[4]/div/div/section[2]/div[2]//section/div/p'):
                # actions.move_to_element(x).perform()
                rating.extend([x.text])
        except :
            pass
        # go to next review-page
        try:
            # driver.implicitly_wait(10)
            if flag == 0:
                element = driver.find_elements_by_xpath('//*[@id="root"]/main/div/section[4]/div/div/section[2]/div[3]/div[2]/div/a/i')[0]
                actions.move_to_element(element).click().perform()
                flag = 1
            else:
                element = driver.find_elements_by_xpath('//*[@id="root"]/main/div/section[4]/div/div/section[2]/div[3]/div[2]/div/a/i')[1]
                actions.move_to_element(element).click().perform()
        except Exception as e:
            print(e)
            break     
        
        # create a review object and add it to Reviews list
        Reviews = [{"reviewer":i,"review":j,"rating":k} for i, j, k in zip(reviewer,review,rating)]
pprint.pprint(Reviews)
print (len(reviewer))

