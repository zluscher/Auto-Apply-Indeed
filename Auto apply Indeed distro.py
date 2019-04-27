#!/usr/bin/env python
# coding: utf-8

# # A Simple Scraper which accesses Job Postings and checks for specific strings

# In[ ]:
__author__ = 'Zachary C Luscher' \

from selenium import webdriver
from time import sleep

import sys

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup
import urllib.request as ur
import re
import sys



red_flags = ["senior", "contract", "staff"] #List of words to avoid in job title
#required = ["software"] #Can also check for required words

def qualifies(title):
    title = title.lower()
    #Define a function to check if a job title is worth checking out
    for word in red_flags:
        if word in title: return False
    return True

#test:
qualifies("Materials Engineer")



# Now define the Regex,
# 1. Should not have the phrase 1+ years, 1-2 Years, so on..
p1 = re.compile('Apply with your Indeed Resume')


t1 = p1.search("2+ Years of experiencce")
t2 = p1.search("0-1 Year")


print (t1, "\n",t2)




#The first page with search results
url_base = "https://www.indeed.com/jobs?q=materials+engineer&l=Salt+Lake+City%2C+UT"
pgno = 0
try:
        response = ur.urlopen(url_base)#+str(pgno))
        html_doc = response.read()
except:
        print("URL not accesible")
        exit()
soup = BeautifulSoup(html_doc, 'html.parser')
"Ready."



try:
    total_results = soup.find(id="searchCount").get_text()
    last_page = int(int(total_results[total_results.index("of")+2: total_results.index("jobs")].strip()) / 10) * 10
    print(last_page)
except:
    print ("No jobs found")


jobs_per_page = 10
goodlinks = []
for pgno in range(0,last_page,jobs_per_page):
    if pgno > 0:
        try:
            response = ur.urlopen(url_base+str(pgno))
            html_doc = response.read()
        except:
            break;
        soup = BeautifulSoup(html_doc, 'html.parser')
    for job in soup.find_all(class_='result'):
        link = job.find(class_="turnstileLink")
        try:
            jt = link.get('title')
        except:
            jt = ""
        try:
            comp = job.find(class_='company').get_text().strip()
        except:
            comp = ""

        if(qualifies(jt.lower())):
            toVisit = "http://www.indeed.com"+link.get('href')
            try:
                html_doc = ur.urlopen(toVisit).read().decode('utf-8')
            except:
                continue;
            m = p1.search(html_doc)

            if not m:
                print(jt,",",comp,":",toVisit,"\n")
                goodlinks.append(toVisit)

for i in goodlinks:
    driver = webdriver.Chrome("C:\\Users\Blu\AppData\Local\Programs\Python\Python36\selenium\webdriver\chromedriver.exe")
    driver.set_page_load_timeout(90)
    driver.get(i)
    driver.maximize_window()
    driver.implicitly_wait(1)

try:
    driver.find_element_by_xpath('//*[@id="gnav-main-container"]/div/div/div[3]/div[2]/a').click()
except:
    driver.find_element_by_xpath('// *[ @ id = "desktopGlobalHeader"] / nav / ul[2] / li[2] / a').click()
    # input your indeed username and password
    driver.find_element_by_xpath('//*[@id="login-email-input"]').send_keys('___')
    driver.find_element_by_xpath('//*[@id="login-password-input"]').send_keys('___')
    driver.find_element_by_xpath('//*[@id="login-submit-button"]').click()
    driver.find_element_by_id("indeedApplyButtonContainer").click()
    driver.get('https://apply.indeed.com/indeedapply/s/resumeApply')

    # input your resume below
    try:
        driver.find_element_by_xpath('// *[ @ id = "attachments-0"]').send_keys(
            'Desktop\Zachary Luscher Resume MSE.docx')
    except:
        driver.find_element_by_xpath('//*[@id="form-action-continue"]').click()

    """try:
        driver.find_element_by_xpath('//*[@id="input-q_6bef7ac30a27975fa2e8b17ebc33c9aa"]').send_keys('I am a Computer Program written by and applying on behalf of ____')
    except:

        try:
            driver.find_element_by_xpath('//*[@id="form-action-continue"]').click()
        except:
            driver.find_element_by_xpath('//*[@id="input-q_6bef7ac30a27975fa2e8b17ebc33c9aa"]').clear()"""

    try:
        driver.find_element_by_xpath('//*[@id="input-q_6bef7ac30a27975fa2e8b17ebc33c9aa"]').send_keys('3')
    except:
        driver.find_element_by_xpath('//*[@id="form-action-continue"]').click()

        """try:
        driver.find_element_by_xpath('Zachary Luscher has many years of Materials Engineering and Programming Experience').click()
        except:

            try:
                driver.find_element_by_xpath('//*[@id="form-action-continue"]').click()
            except:
                driver.find_element_by_xpath('//*[@id="input-q_6bef7ac30a27975fa2e8b17ebc33c9aa"]').clear()

                try:
                    driver.find_element_by_xpath('3').click()
                except:
                    driver.find_element_by_xapth('//*[@id="form-action-continue"]').click()"""









