import json
import time
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from player import Player
from roster import Roster
from click_roster import click_roster

url = os.environ.get('fantasy_url')

# Check if cookies file exists
if not os.path.isfile("cookies.json"):
    print("You do not have a cookies.json file")
# Check if environmental URL exists
elif not url:
    print("You do not have a fantasy_url environmental variable set")  
else:
    '''
    Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    '''
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_prefs = {}
    chrome_options.experimental_options['prefs'] = chrome_prefs
    chrome_prefs['profile.default_content_settings'] = {'images': 2}

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    # Load cookies instead of inputting user login
    with open("cookies.json") as fp:
        data = json.load(fp)
        for cookie in data:
            if 'sameSite' in cookie:
                if cookie['sameSite'] != 'Strict' and cookie['sameSite'] != 'Lax' and cookie['sameSite'] != 'None':
                    cookie['sameSite'] = 'Strict'
            driver.add_cookie(cookie)

    driver.set_window_size(3000,3000)
    driver.get(url)
    time.sleep(10)

    click_roster(driver, False, '//*[@id="fitt-analytics"]/div/div[3]/div/div[3]/div/div/div/div[3]/div/div[1]')
    click_roster(driver, True, '//*[@id="fitt-analytics"]/div/div[3]/div/div[3]/div/div/div/div[3]/div/div[2]')

    driver.close()