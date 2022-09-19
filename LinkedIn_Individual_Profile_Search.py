import re
from time import sleep
import datetime as dt
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd


def link(First_name,Second_name,Company_name):
    tags= ""
    lists = []
    Link_List = []
    LinkedIn_URL=""
    driver.get("https://www.google.com/search?q=")
    try:
        m = driver.find_element_by_css_selector("input[class^='gLFyf gsfi']")
    except:
        print("Captcha")
    # enter search text
    if Second_name.__contains__("."):
        Second_name = ""
    m.send_keys(First_name+" "+ Second_name +" "+Company_name+" "+ "LinkedIn profile")
    time.sleep(0.2)
    m.send_keys(Keys.ENTER)
    time.sleep(7)
    try:
        tags = driver.find_elements_by_css_selector("h3[class^='LC20lb MBeuO DKV0Md']")
        for tag in tags:
            t_name = tag.text
            if t_name.lower().__contains__(First_name.lower()):
                tag.click()
                time.sleep(10)
                LinkedIn_URL = driver.current_url
                if LinkedIn_URL.__contains__("404"):
                    LinkedIn_URL = 'NaN'
                break
                time.sleep(5)
            else:
                continue
    except:
        LinkedIn_URL = 'NaN'
        print("No Google Page Found for this property")
    lists.append(First_name)
    lists.append(Second_name)
    lists.append(Company_name)
    lists.append(LinkedIn_URL)
    Link_List.append(lists)
    return Link_List



indeed = pd.read_csv("/Users/apple/Desktop/LinkedIn_URLs_5.csv")
First_Name = indeed["first_name"]
Second_Name = indeed["Last Name"]
Company_name = indeed["company"]

results= []
count = 0


for i in range(len(First_Name)):
    if (i+1)%2 == 0:
        profile = webdriver.FirefoxProfile(
            "/Users/apple/Library/Application Support/Firefox/Profiles/0ur7nimh.default-release-11")
        gecko_path = "/Users/apple/doc/Git/geckodriver/geckodriver"
        driver = webdriver.Firefox(firefox_profile=profile, executable_path=gecko_path)
        List = link(First_Name[i], Second_Name[i], Company_name[i])
        driver.close()
    else:
        profile = webdriver.FirefoxProfile("/Users/apple/Library/Application Support/Firefox/Profiles/i6ypfrfw.Solulab")
        gecko_path = "/Users/apple/doc/Git/geckodriver/geckodriver"
        driver = webdriver.Firefox(firefox_profile=profile, executable_path=gecko_path)
        List = link(First_Name[i], Second_Name[i], Company_name[i])
        driver.close()

    for i in range(len(List)):
        count = count + 1
        print(count)
        results.append(List[i])
    sleep(1)

    if count%131 == 0:

        # Turn results list into dataframe
        df = pd.DataFrame(results, columns=['First Name', 'Second Name', 'Company Name', 'LinkedIn URL'])

        name = str(dt.datetime.now())
        df.to_csv(f'/Users/apple/PycharmProjects/pythonProject4/unclean_scraped_data/{name}.csv')  # Save data







driver.close()


