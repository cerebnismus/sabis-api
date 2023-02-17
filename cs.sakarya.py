#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#  -*- cerebnismus -*-
 
# Sakarya University 
# Computer Science Department

import random, time, os, re # re for regular expressions
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

# Global Variables
login_url = "https://obs.sabis.sakarya.edu.tr"
username = ""
password = ""

def cs_sakarya():
    url = "https://cs.sakarya.edu.tr/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    title_strings = soup.find_all("h5", {"class": "blog-list-title"})
    title_detail_strings = soup.find_all("p", {"class": "blog-list-meta small-text"})
    title_date_strings = soup.find_all("div", {"class": "calendar-haber"})

# print the news feed. title and title detail.
    print('\nHaberler')
    print('-'*40)
    for i in range(4):
      print(title_date_strings[i].text, title_strings[i].text)
      print(title_detail_strings[i].text)
  
# print the announcements feed. title and title detail. from 4 to 9.
    print('\nDuyurular')
    print('-'*40)
    for i in range(4, 9):
      print(title_date_strings[i].text, title_strings[i].text)
      print(title_detail_strings[i].text)

  
class DriverOptions(object):

    def __init__(self):

        self.options = Options()
        self.options.headless = True
        # self.options.binary_location = '/Applications/Chrome.app/Contents/MacOS/Google Chrome'
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--start-maximized')
        # self.options.add_argument('--start-minimized')
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
        # self.options.add_argument('--disable-gpu')
        # self.options.add_experimental_option('w3c', True)
        # self.options.add_argument('--disable-web-security')
        # self.options.add_argument('--allow-running-insecure-content')
        
        # self.options.add_argument('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15"')
        # self.options.add_argument('--proxy-server=%s' % self.helperSpoofer.ip)
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



def main():
  
  cs_sakarya()
  driver = WebDriver()
  driverinstance = driver.driver_instance
  wait = WebDriverWait(driverinstance, 20)
  driverinstance.get(login_url)
  time.sleep(2)
  
  _email_input = wait.until(EC.presence_of_element_located((By.ID, 'Username')))
  _email_input.send_keys(username)
  _password_input = wait.until(EC.presence_of_element_located((By.ID, 'Password')))
  _password_input.send_keys(password)
  _login_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="kt_login_form"]/div[4]/button')))
  _login_button.click()
  time.sleep(2)
  
  wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'text-muted')))
  
   # scrape 'duyurular' with beautifulsoup
  soup = BeautifulSoup(driverinstance.page_source, 'html.parser')
  time.sleep(2)
  print('\nDuyurular')
  print('-'*40)
  driverinstance.implicitly_wait(2)
  
  dates = soup.find_all('span', class_='text-muted')
  titles = soup.find_all('a', class_='text-warning')
  descriptions = soup.find_all('div', class_='text-dark font-weight-bold')
  
  # TODO: Colorize the output with colorama or termcolor or something else !
  for i in range(len(dates)):
    try:
      print(dates[i].text)
      first_alpha = re.search('[a-zA-Z0-9]', titles[i].text).start()
      last_alpha = re.search('[a-zA-Z0-9]', titles[i].text[::-1]).start()
      print(titles[i].text[first_alpha:len(titles[i].text)-last_alpha])
      
      # get first any alphabet or numeric characters from the description
      first_alpha = re.search('[a-zA-Z0-9]', descriptions[i].text).start()
      last_alpha = re.search('[a-zA-Z0-9]', descriptions[i].text[::-1]).start()
      print(descriptions[i].text[first_alpha:len(descriptions[i].text)-last_alpha])

    except IndexError:
      pass
    
  # scrape 'dersprogrami' with beautifulsoup
  driverinstance.get('https://obs.sabis.sakarya.edu.tr/Program')
  button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="kt_calendar"]/div[1]/div[3]/div/button[4]')))
  driverinstance.implicitly_wait(2)
  # ActionChains(driver).move_to_element(button).click(button).perform()
  button.click()
  time.sleep(1)
  
  soup = BeautifulSoup(driverinstance.page_source, 'html.parser')
  print('\nDers Programı')
  print('-'*40)
 
  days = soup.find_all('a', class_='fc-list-heading-main')
  dates = soup.find_all('a', class_='fc-list-heading-alt')
  times = soup.find_all('td', class_='fc-list-item-time')
  titles = soup.find_all('td', class_='fc-list-item-title')
  descriptions = soup.find_all('div', class_='fc-description')
  
  for i in range(len(days)):
    print(dates[i].text, days[i].text, times[i].text)
    print(titles[i].text[:-12], descriptions[i].text)
  
  time.sleep(2222)
  # driverinstance.quit()
    
if __name__ == "__main__":

    while True:
        try:
            main()
        except Exception as e:
            print(e)
            continue
        break
    
# most of the time it can't get the IP address from the proxy and raise the error below
# selenium.common.exceptions.WebDriverException: Message: unknown error: net::ERR_TUNNEL_CONNECTION_FAILED