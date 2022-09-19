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

from packaging.requirements import URL


def location_res(result):
    '''Function to extract location from Indeed search result'''

    tag = result.find(name='span', attrs={'class': 'JobPosting-labelWithIcon jobposting-location'})  # find appropriate tag
    try:
        tag2 = tag.select('span')
        location = tag2[0].text
        return location
    except:
        return 'NaN'


def company_res(result):
    '''Function to extract company name from Indeed search result'''

    tag = result.find(name='div', attrs={'class': 'jobposting-subtitle'})  # find appropriate tag
    try:  # Second try statement accounts for whether there any nested tags
        tag2 = tag.select('span:nth-child(1)')
        Name = tag2[0].text
        return Name
    except:
        return 'NaN'



def job_res(result):
    '''Function to extract job title'''

    try:  # Accounts for missing job title
        tag = result.find(name='h3', attrs={'class': 'jobposting-title'})
        job = tag.text
        return job
    except:
        return 'NaN'


def salary_res(result):
    '''Function to extract salary'''
    try:
        tag = result.find(name='div', attrs={'class': 'SerpJob-metaInfoLeft'})
        tag2 = tag.select('div')
        Salary = tag2[0].text
        if Salary.__contains__("$"):
            return Salary
        else:
            return 'NaN'
    except:
        return 'NaN'

def job_description(result):
    try:
        Lists = []
        Today = datetime.datetime.today()
        tag = result.find(name='a', attrs={'class': 'SerpJob-link card-link'})['data-mdref']
        url_href = "https://www.simplyhired.com" + tag
        time.sleep(2)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0'}
        response = requests.get(url_href,headers=headers)
        html = response.text
        soup_ = BeautifulSoup(html, 'html.parser', from_encoding="utf-8")
        tag2 = soup_.find(name='div', attrs={'class': 'viewjob-jobDescription'})
        if tag2:
            job_desc = tag2.text
        else:
            job_desc = 'NaN'

        Date_tag = soup_.find(name='span',attrs={'class':'viewjob-labelWithIcon viewjob-age'})
        if Date_tag:
            date_ = re.findall(r'\d+', Date_tag.text)
            d = datetime.timedelta(days=int(date_[0]))
            a = Today - d
            Published_Date = a.strftime('%Y-%m-%d')
        else:
            Published_Date = 'NaN'
        Lists.append(job_desc)
        Lists.append(Published_Date)

        return Lists
    except:
        return 'NaN'


def all_funcs(search):
    '''
    This function iterates through each result on a single Indeed.com results
    page then applies the four functions above to extract the relevant
    information. It takes a search argument in order to also keep track of the
    search term used, since location can give a different value than the actual
    city or location searched.'''

    entries = []
    try:
        tag = search.find(name='ul', attrs={'class': 'jobs'})
        for result in tag.find_all(name='li'):
            result_data = []
            result_data.append(job_res(result))
            result_data.append(company_res(result))
            result_data.append(location_res(result))
            result_data.append(salary_res(result))
            JD_List = job_description(result)
            for attribute in JD_List:
                result_data.append(attribute)
            # result_data.append(search)
            entries.append(result_data)
        return entries
    except:
        return entries


def scrape(cities_list,job_list, max=20):
    max_results_per_city = max
    page_no = math.ceil(max/25)
    results = []  # Empty list that will contain all results
    a = dt.datetime.now()  # Start time of process
    print(a)

    for job in job_list:
        for city in cities_list:  # Iterate through cities
            for start in range(page_no):  # Iterate through results pages
                url = "https://www.simplyhired.com/search?q="+job+"&l="+city+"&job=QHLqscVbEB-jqamn7BlL3DCHfcUavMskTdl37U57Fw15Gan1-Dngaw"
                html = urllib.request.urlopen(url).read()
                soup = BeautifulSoup(html, 'html.parser', from_encoding="utf-8")
                data = all_funcs(soup)  # use functions from before to extract all job listing info
                for i in range(len(data)):  # add info to results list
                    results.append(data[i])
                sleep(1)
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
    df = pd.DataFrame(results, columns=['Job Title', 'Company', 'Location', 'Salary', 'Job Description', 'Publishing Date',''])

    name = str(dt.datetime.now())
    df.to_csv(f'/Users/apple/PycharmProjects/pythonProject4/unclean_scraped_data/SimplyHired_Java.csv')  # Save data


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

jobs = ["Java%20Developer",
"Remote%20React/Java%20Developer",
"Java%20Developer%20-%20J2EE/Spring%20Boot",
"Java/Kotlin%20Developer",
"Java%20Architect",
"Java%20Developer%20–%20Core%20Java",
"java%20SSE%20AWS",
"Java%20(Spring%20Boot)%20Developer",]

scrape(cities,jobs)
