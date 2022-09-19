import datetime
import math
import re
import datetime as dt
import sys
import time
from time import sleep

import requests as requests
from bs4 import BeautifulSoup
import urllib
import pandas as pd
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


from packaging.requirements import URL

profile = webdriver.FirefoxProfile("/Users/apple/Library/Application Support/Firefox/Profiles/0ur7nimh.default-release-11")
gecko_path="/Users/apple/doc/Git/geckodriver/geckodriver"
driver = webdriver.Firefox(firefox_profile=profile,executable_path=gecko_path)

def location_res(result):
    '''Function to extract location from Indeed search result'''

    try:  # Second try statement accounts for whether there any nested tags
        tag = result.find_element_by_css_selector("p[class^='job_org']>a[class^='t_location_link location']")
        return tag.text
    except:
        return 'NaN'


def company_res(result):
    '''Function to extract company name from Indeed search result'''
    try:  # Accounts for missing job title
        tag = result.find_element_by_css_selector("p[class^='job_org']>a[class^='t_org_link name']")
        job = tag.text
        return job
    except:
        return 'NaN'



def job_res(result):
    '''Function to extract job title'''
    try:
        tag = result.find_element_by_css_selector("h2[class^='job_title']>span")
        return tag.text
    except:
        return 'NaN'


def salary_res(result):
    '''Function to extract salary'''
    try:
        tag = result.find_element_by_css_selector("div[class^='job_description_container']>div[class^='job_characteristics']>section[class^='perks_item perks_compensation']>p[class^='data']>span[class^='data_item']")
        Salary = tag.text
        if Salary.__contains__("$"):
            return Salary
        else:
            return 'NaN'
    except:
        return 'NaN'


def job_description(result):
    try:
        lists = []
        JD_List = []
        Today = datetime.datetime.today()
        tag = result.find_element_by_css_selector("div[class^='job_title_and_org']>a")
        tag2 = tag.get_attribute('href')
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:103.0) Gecko/20100101 Firefox/103.0'}
        response = requests.get(tag2,headers=headers)
        html = response.text
        soup_ = BeautifulSoup(html, 'html.parser', from_encoding="utf-8")
        tag_JD = soup_.find(name='div', attrs={'class': 'jobDescriptionSection'})
        if tag_JD:
            job_desc = tag_JD.text
        else:
            job_desc = 'NaN'

        tag_Link = soup_.find(name='a', attrs={'class': 'data'})
        if tag_Link:
            link = tag_Link.text
        else:
            link = 'NaN'
        tag4 = soup_.find_all(name='p',attrs={'class':'job_more'})
        for i in tag4:
            tag5 = i.find(name='span', attrs={'class': 'data'})
            if tag5:
                date_ = tag5.text
                date_ = re.findall(r'\d+', date_)
                d = datetime.timedelta(days=int(date_[0]))
                a = Today - d
                Published_Date = a.strftime('%Y-%m-%d')
                break
            else:
                Published_Date = 'NaN'
                break

        lists.append(job_desc)
        lists.append(link)
        lists.append(Published_Date)
        JD_List.append(lists)
        return JD_List
    except:
        lists = []
        JD_List = []
        job_desc = 'NaN'
        link = 'NaN'
        Published_Date = 'NaN'
        lists.append(job_desc)
        lists.append(link)
        lists.append(Published_Date)
        JD_List.append(lists)
        return JD_List


def all_funcs(count,page_No,total):
    '''
    This function iterates through each result on a single Indeed.com results
    page then applies the four functions above to extract the relevant
    information. It takes a search argument in order to also keep track of the
    search term used, since location can give a different value than the actual
    city or location searched.'''
    loop_break = False
    entries = []
    for i in range(page_No):
        try:
            if i >= 1:
                search_element = driver.find_elements_by_css_selector(
                    "div[data-type^='job_results']:nth-child(" + str(i + 2) + ")")
            else:
                search_element = driver.find_elements_by_css_selector("div[data-type^='job_results']")
        except:
            return entries
        for element in search_element:
            result_set = element.find_elements_by_tag_name("article")
            for result in result_set:
                driver.execute_script('arguments[0].scrollIntoView(true);', result)
                time.sleep(3)
                result_data = []
                result_data.append(job_res(result))
                result_data.append(company_res(result))
                result_data.append(location_res(result))
                result_data.append(salary_res(result))
                Attr_List = job_description(result)
                for attribute in Attr_List:
                    for j in attribute:
                        result_data.append(j)

                # result_data.append(link(result))
                # result_data.append(Date_Published(result))
                # result_data.append(search)
                entries.append(result_data)
                count = count + 1
        if total == count:
            return entries
            break
    return entries







def scrape(cities_list,job_list, max=100):
    max_results_per_city = max
    page_no = math.ceil(max/20)
    results = []  # Empty list that will contain all results
    a = dt.datetime.now()  # Start time of process
    print(a)
    count_button = 0

    for job in job_list:
        for city in cities_list:  # Iterate through cities
            count = 0
            url = "https://www.ziprecruiter.com/candidate/search?search=" + job + "&location=" + city + "&days=&radius=50&refine_by_salary=&refine_by_tags=&refine_by_title=&refine_by_org_name="
            driver.get(url)
            if count_button == 0:
                if driver.find_elements_by_css_selector("button[class^='load_more_jobs']"):
                    driver.find_element_by_css_selector("button[class^='load_more_jobs']").click()
                    time.sleep(3)
                else:
                    print("Button not present")
            data = all_funcs(count,page_no,max_results_per_city)  # use functions from before to extract all job listing info
            if data:
                for i in range(len(data)):  # add info to results list
                    results.append(data[i])
                sleep(1)
                count_button = count_button + 1

            print(city + " DONE")
            print("Elapsed time: " + str(dt.datetime.now() - a))  # Update user on progress



        b = dt.datetime.now()
        c = b - a
        print(c)

        print(job + "Done")
        print("Elapsed time: " + str(dt.datetime.now() - a))
    d= dt.datetime.now()
    time_taken = d-a
    print(time_taken)

    # Turn results list into dataframe
    df = pd.DataFrame(results, columns=['Job Title', 'Company', 'Location', 'Salary', 'Job Description', 'Company URL', 'Publishing Date'])

    name = str(dt.datetime.now())
    df.to_csv(f'/Users/apple/PycharmProjects/pythonProject4/unclean_scraped_data/{name}.csv')  # Save data
    driver.close()


cities = ['Alabama',
'Alaska',
'Arizona',
'Arkansas',
'California',
'Colorado',
'Connecticut',
'Delaware',
'Florida',
'Georgia',
'Hawaii',
'Idaho',
'Illinois',
'Indiana',
'Iowa',
'Kansas',
'Kentucky',
'Louisiana',
'Maine',
'Maryland',
'Massachusetts',
'Michigan',
'Minnesota',
'Mississippi',
'Missouri',
'Montana',
'Nebraska',
'Nevada',
'New+Hampshire',
'New+Jersey',
'New+Mexico',
'New+York',
'North+Carolina',
'North+Dakota',
'Ohio',
'Oklahoma',
'Oregon',
'Pennsylvania',
'Rhode+Island',
'South+Carolina',
'South+Dakota',
'Tennessee',
'Texas',
'Utah',
'Vermont',
'Virginia',
'Washington',
'West+Virginia',
'Wisconsin',
'Wyoming']

jobs = ["full+stack+developer"]

scrape(cities,jobs)
driver.close()