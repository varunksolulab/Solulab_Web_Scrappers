import re
from time import sleep
import datetime as dt
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd


profile = webdriver.FirefoxProfile("/Users/apple/Library/Application Support/Firefox/Profiles/0ur7nimh.default-release-11")
gecko_path="/Users/apple/doc/Git/geckodriver/geckodriver"
driver = webdriver.Firefox(firefox_profile=profile,executable_path=gecko_path)

def link(Company_Name,Country):
    Link_List = []
    lists = []
    tag= ""
    Industry=""
    driver.get("https://www.google.com/search?q=")
    try:
        m = driver.find_element_by_css_selector("input[class^='gLFyf gsfi']")
    except:
        print("Captcha")
    # enter search text
    Country = re.sub('[^A-Za-z0-9]+', ' ', Country)
    m.send_keys(Company_Name+" "+ Country +" "+ "LinkedIn profile")
    time.sleep(0.2)
    m.send_keys(Keys.ENTER)
    time.sleep(7)
    try:
        tag = driver.find_element_by_css_selector("h3[class^='LC20lb MBeuO DKV0Md']").text
    except:
        print("No Google Page Found for this property")
    if tag.lower().__contains__(Company_Name.lower()):
        driver.find_element_by_css_selector("h3[class^='LC20lb MBeuO DKV0Md']").click()
        time.sleep(5)
        if driver.current_url.__contains__("authwall"):
            LinkedIn_Url = 'NaN'
        else:
            LinkedIn_Url = driver.current_url
        try:
            funding = driver.find_element_by_css_selector("p[class^='t-14 t-bold']").text
            if funding.__contains__("$"):
                Funding = funding
            else:
                Funding = 'NaN'
        except:
            Funding = 'NaN'
        try:
            driver.find_element_by_css_selector("ul[class^='org-page-navigation__items ']>li:nth-child(2)").click()
        except:
            print("It's not the company page")
        time.sleep(4)
        try:
            company_url = driver.find_element_by_css_selector("dd:nth-child(2)").text
            Company_URL = company_url
        except:
            Company_URL = 'NaN'
        try:
            employees = driver.find_element_by_css_selector("dd:nth-child(6)").text
            industry = driver.find_element_by_css_selector("dd:nth-child(4)").text

            if employees.__contains__("employees"):
                Num_Employees = employees
            else:
                employees = ""
                employees = driver.find_element_by_css_selector("dd:nth-child(8)").text
                if employees.__contains__("employees"):
                    Num_Employees = employees
                else:
                    Num_Employees = 'NaN'
            if bool(re.search(r'\d',industry)):
                Industry = driver.find_element_by_css_selector("dd:nth-child(6)").text
            else:
                Industry = industry
        except:
            Num_Employees = 'NaN'
        Company_name = Company_Name
        lists.append(Company_name)
        lists.append(LinkedIn_Url)
        lists.append(Company_URL)
        lists.append(Num_Employees)
        lists.append(Funding)
        lists.append(Industry)
        Link_List.append(lists)
        return Link_List
    else:
        Company_name = 'NaN'
        LinkedIn_Url = 'NaN'
        Company_URL = 'NaN'
        Num_Employees = 'NaN'
        Funding = 'NaN'
        Industry = 'NaN'
        lists.append(Company_name)
        lists.append(LinkedIn_Url)
        lists.append(Company_URL)
        lists.append(Num_Employees)
        lists.append(Funding)
        lists.append(Industry)
        Link_List.append(lists)
        return Link_List


indeed = pd.read_csv("/Users/apple/PycharmProjects/pythonProject4/unclean_scraped_data/CareerBuilder_Full_Stack.csv",index_col=[0])
Company_List = indeed.iloc[:, 1]
Company_List = list(set(Company_List))
Country_List = ["USA"]
results= []
count = 0
for Country in Country_List:
    for Company_Name in Company_List:
        List = link(Company_Name, Country)
        for i in range(len(List)):
            count = count + 1
            print(count)
            results.append(List[i])
        sleep(1)

# Turn results list into dataframe
df = pd.DataFrame(results, columns=['Company Name','LinkedIn URL','Company URL','Company Size','Funding','Industry'])

name = str(dt.datetime.now())
df.to_csv(f'/Users/apple/PycharmProjects/pythonProject4/unclean_scraped_data/CareerBuilder_Full_Stack.csv')  # Save data


driver.close()


