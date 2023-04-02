from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import time
import os
from selenium import webdriver
from player import Player
from roster import Roster
from selenium.common.exceptions import NoSuchElementException


'''Sets chrome options for Selenium.
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

with open("cookies.json") as fp:
    data = json.load(fp)

url = os.environ.get('fantasy_url')

driver.get(url)

for cookie in data:
    if 'sameSite' in cookie:
        if cookie['sameSite'] != 'Strict' and cookie['sameSite'] != 'Lax' and cookie['sameSite'] != 'None':
            cookie['sameSite'] = 'Strict'
    driver.add_cookie(cookie)

driver.set_window_size(3000,3000)
driver.get(url)
time.sleep(10)

numRows = len(driver.find_elements(By.XPATH, '//*[@id="fitt-analytics"]/div/div[3]/div/div[3]/div/div/div/div[3]/div/div[1]/div/div/table/tbody/tr'))
startXPATH = '//*[@id="fitt-analytics"]/div/div[3]/div/div[3]/div/div/div/div[3]/div/div[1]/div/div/table/tbody/tr['

player_table = []
league_slots = []
slots = []

for row in range(1, numRows+1):
    rowXpath = startXPATH + str(row) + ']'
    try:
        current_slot = driver.find_element(By.XPATH, rowXpath + '/td[1]/div').text.split("/")
        if current_slot[0] != "Bench":
            if not league_slots:
                league_slots.append([current_slot, 1])
            else:
                increment = False
                for slot in league_slots:   
                    if slot[0] == current_slot:
                        slot[1] += 1
                        increment = True
                if not increment:
                    league_slots.append([current_slot, 1])
        positions = driver.find_element(By.XPATH, rowXpath + '/td[2]/div/div/div[2]/div/div[2]/span[2]').text.split(", ")
        positions.append("UTIL")
        status = bool(driver.find_element(By.XPATH, rowXpath + '/td[5]/div').text)
        name = driver.find_element(By.XPATH, rowXpath + '/td[2]/div/div/div[2]/div/div[1]/span/a').text
        injured = True
        try:
            el = driver.find_element(By.XPATH, rowXpath + '/td[2]/div/div/div[2]/div/div[1]/span[2]')
            if not el.text:
                injured = False
        except NoSuchElementException:
            injured = False
        player_item = Player(name, positions, status, injured, 1)
        player_table.append(player_item)
    except NoSuchElementException:
        pass

roster = Roster(player_table, league_slots)
roster.solve()
final_roster = roster.get_roster()

numRows = len(driver.find_elements(By.XPATH, '//*[@id="fitt-analytics"]/div/div[3]/div/div[3]/div/div/div/div[3]/div/div[1]/div/div/table/tbody/tr'))

for slot in final_roster:
    s = "/"
    pos_string = s.join(slot[0])
    slot.append(pos_string)

formatted_roster = []
for slot in final_roster:
    for player in slot[1]:
        formatted_roster.append([slot[2], player])

positions = []
for row in range(1, numRows+1):
    rowXpath = startXPATH + str(row) + ']'
    current_slot = driver.find_element(By.XPATH, rowXpath + '/td[1]/div').text
    if current_slot != "Bench":
        positions.append([current_slot, row])

for pos in positions:
    for index, player in enumerate(formatted_roster):
        if pos[0] == player[0]:
            pos.append(player[1])
            del formatted_roster[index]
            break

print(positions)

for slot in positions:
    if 3 == len(slot):
        index = int(driver.find_element(By.XPATH, '//*[@id="fitt-analytics"]/div/div[3]/div/div[3]/div/div/div/div[3]/div/div[1]/div/div/table/tbody/tr[.//*[text()="' + slot[2] + '"]]').get_attribute("data-idx"))
        if index + 1 != slot[1]:
            driver.find_element(By.XPATH, '//*[@id="fitt-analytics"]/div/div[3]/div/div[3]/div/div/div/div[3]/div/div[1]/div/div/table/tbody/tr[' + str(index + 1) + ']/td[3]/div/div/button').click()
            time.sleep(3)
            try:
                driver.find_element(By.XPATH, '//*[@id="fitt-analytics"]/div/div[3]/div/div[3]/div/div/div/div[3]/div/div[1]/div/div/table/tbody/tr[' + str(slot[1]) + ']/td[3]/div/div/button').click()
                time.sleep(3)
            except NoSuchElementException:
                driver.find_element(By.XPATH, '//*[@id="fitt-analytics"]/div/div[3]/div/div[3]/div/div/div/div[3]/div/div[1]/div/div/table/tbody/tr[' + str(len(positions)+1) + ']/td[3]/div/div/button').click()
                time.sleep(3)
                index = int(driver.find_element(By.XPATH, '//*[@id="fitt-analytics"]/div/div[3]/div/div[3]/div/div/div/div[3]/div/div[1]/div/div/table/tbody/tr[.//*[text()="' + slot[2] + '"]]').get_attribute("data-idx"))
                driver.find_element(By.XPATH, '//*[@id="fitt-analytics"]/div/div[3]/div/div[3]/div/div/div/div[3]/div/div[1]/div/div/table/tbody/tr[' + str(index + 1) + ']/td[3]/div/div/button').click()
                time.sleep(3)
                driver.find_element(By.XPATH, '//*[@id="fitt-analytics"]/div/div[3]/div/div[3]/div/div/div/div[3]/div/div[1]/div/div/table/tbody/tr[' + str(slot[1]) + ']/td[3]/div/div/button').click()
                time.sleep(3)
                print("here")

# Pitcher
numRows = len(driver.find_elements(By.XPATH, '//*[@id="fitt-analytics"]/div/div[3]/div/div[3]/div/div/div/div[3]/div/div[2]/div/div/table/tbody/tr'))
startXPATH = '//*[@id="fitt-analytics"]/div/div[3]/div/div[3]/div/div/div/div[3]/div/div[2]/div/div/table/tbody/tr['

player_table = []
league_slots = []
slots = []

for row in range(1, numRows+1):
    rowXpath = startXPATH + str(row) + ']'
    try:
        current_slot = driver.find_element(By.XPATH, rowXpath + '/td[1]/div').text.split("/")
        if current_slot[0] != "Bench" and current_slot[0] != "IL":
            if not league_slots:
                league_slots.append([current_slot, 1])
            else:
                increment = False
                for slot in league_slots:   
                    if slot[0] == current_slot:
                        slot[1] += 1
                        increment = True
                if not increment:
                    league_slots.append([current_slot, 1])
        positions = ["P"]
        status = bool(driver.find_element(By.XPATH, rowXpath + '/td[5]/div').text)
        name = driver.find_element(By.XPATH, rowXpath + '/td[2]/div/div/div[2]/div/div[1]/span/a').text
        injured = True
        try:
            el = driver.find_element(By.XPATH, rowXpath + '/td[2]/div/div/div[2]/div/div[1]/span[2]')
            if not el.text:
                injured = False
        except NoSuchElementException:
            injured = False
        player_item = Player(name, positions, status, injured, 1)
        player_table.append(player_item)
    except NoSuchElementException:
        pass

roster = Roster(player_table, league_slots)
roster.solve()
final_roster = roster.get_roster()

numRows = len(driver.find_elements(By.XPATH, '//*[@id="fitt-analytics"]/div/div[3]/div/div[3]/div/div/div/div[3]/div/div[2]/div/div/table/tbody/tr'))

for slot in final_roster:
    s = "/"
    pos_string = s.join(slot[0])
    slot.append(pos_string)

formatted_roster = []
for slot in final_roster:
    for player in slot[1]:
        formatted_roster.append([slot[2], player])

positions = []
for row in range(1, numRows+1):
    rowXpath = startXPATH + str(row) + ']'
    current_slot = driver.find_element(By.XPATH, rowXpath + '/td[1]/div').text
    if current_slot != "Bench" and current_slot != "IL":
        positions.append([current_slot, row])

for pos in positions:
    for index, player in enumerate(formatted_roster):
        if pos[0] == player[0]:
            pos.append(player[1])
            del formatted_roster[index]
            break

print(positions)

for slot in positions:
    if 3 == len(slot):
        index = int(driver.find_element(By.XPATH, '//*[@id="fitt-analytics"]/div/div[3]/div/div[3]/div/div/div/div[3]/div/div[2]/div/div/table/tbody/tr[.//*[text()="' + slot[2] + '"]]').get_attribute("data-idx"))
        if index + 1 != slot[1]:
            driver.find_element(By.XPATH, '//*[@id="fitt-analytics"]/div/div[3]/div/div[3]/div/div/div/div[3]/div/div[2]/div/div/table/tbody/tr[' + str(index + 1) + ']/td[3]/div/div/button').click()
            time.sleep(3)
            try:
                driver.find_element(By.XPATH, '//*[@id="fitt-analytics"]/div/div[3]/div/div[3]/div/div/div/div[3]/div/div[2]/div/div/table/tbody/tr[' + str(slot[1]) + ']/td[3]/div/div/button').click()
                time.sleep(3)
            except NoSuchElementException:
                driver.find_element(By.XPATH, '//*[@id="fitt-analytics"]/div/div[3]/div/div[3]/div/div/div/div[3]/div/div[2]/div/div/table/tbody/tr[' + str(len(positions)+1) + ']/td[3]/div/div/button').click()
                time.sleep(3)
                index = int(driver.find_element(By.XPATH, '//*[@id="fitt-analytics"]/div/div[3]/div/div[3]/div/div/div/div[3]/div/div[2]/div/div/table/tbody/tr[.//*[text()="' + slot[2] + '"]]').get_attribute("data-idx"))
                driver.find_element(By.XPATH, '//*[@id="fitt-analytics"]/div/div[3]/div/div[3]/div/div/div/div[3]/div/div[2]/div/div/table/tbody/tr[' + str(index + 1) + ']/td[3]/div/div/button').click()
                time.sleep(3)
                driver.find_element(By.XPATH, '//*[@id="fitt-analytics"]/div/div[3]/div/div[3]/div/div/div/div[3]/div/div[2]/div/div/table/tbody/tr[' + str(slot[1]) + ']/td[3]/div/div/button').click()
                time.sleep(3)
                print("here")



driver.close()
