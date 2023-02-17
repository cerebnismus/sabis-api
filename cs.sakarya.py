#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#  -*- cerebnismus -*-
 
# Sakarya University 
# Computer Science Department

import random, time, os
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import requests

def cs_sakarya():
    url = "https://cs.sakarya.edu.tr/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    title_strings = soup.find_all("h5", {"class": "blog-list-title"})
    title_detail_strings = soup.find_all("p", {"class": "blog-list-meta small-text"})
    title_date_strings = soup.find_all("div", {"class": "calendar-haber"})

# print the news feed. title and title detail.
    print('SAU HABERLER')
    print('-'*64)
    for i in range(4):
      print(title_date_strings[i].text, title_strings[i].text)
      print(title_detail_strings[i].text)
      print()
  
# print the announcements feed. title and title detail. from 4 to 9.
    print('SAU DUYURULAR')
    print('-'*64)
    for i in range(4, 9):
      print(title_date_strings[i].text, title_strings[i].text)
      print(title_detail_strings[i].text)
      print()

  
class DriverOptions(object):

    def __init__(self):

        self.options = Options()
        self.options.headless = False
        self.options.binary_location = '/Applications/Chrome.app/Contents/MacOS/Google Chrome'
        self.options.add_argument('--no-sandbox')
        # self.options.add_argument('--start-maximized')
        # self.options.add_argument('--start-fullscreen')
        self.options.add_argument('--single-process')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--incognito')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_argument('disable-infobars')
        self.options.add_argument('--disable-infobars')
        #self.options.add_argument('--profile-directory=1')

        # following options reduce the RAM usage
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--disable-application-cache')
        self.options.add_argument('--disable-gpu')

        self.options.add_argument('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15"')
        # self.options.add_argument('--proxy-server=%s' % self.helperSpoofer.ip)
        # self.options.add_argument('--proxy-server=%s' % didsoft_proxy)
        
        # proxy with user and password
        # self.options.add_argument('--proxy-server=%s' % didsoft_proxy)
        # self.options.add_argument('--proxy-server=%s:%s@%s:%s' % (PROXY_USER, PROXY_PASS, PROXY_HOST, PROXY_PORT))


class WebDriver(DriverOptions):

    def __init__(self, path=''):
        DriverOptions.__init__(self)
        self.driver_instance = self.get_driver()

    def get_driver(self):

        webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True

        # If you want to use geckodriver then getting error like below
        # Message: Unable to find a matching set of capabilities
        # service = Service('/usr/local/bin/geckodriver')
        # driver = webdriver.Chrome(service=service, options=self.options)

        driver = webdriver.Chrome(options=self.options)
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source":
                "const newProto = navigator.__proto__;"
                "delete newProto.webdriver;"
                "navigator.__proto__ = newProto;"
        })

        return driver

  
login_url = "https://obs.sabis.sakarya.edu.tr"
login_data = {
	"Username": "",
	"Password": ""
}


def main():
  
	cs_sakarya()
  
	driver = WebDriver()
	driverinstance = driver.driver_instance
	wait = WebDriverWait(driverinstance, 60)
	driverinstance.get(login_url)