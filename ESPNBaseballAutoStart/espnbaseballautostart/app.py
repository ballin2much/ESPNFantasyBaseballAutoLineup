import json
import time
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from player import Player
from roster import Roster

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

    batterXPATH = '//*[@id="fitt-analytics"]/div/div[3]/div/div[3]/div/div/div/div[3]/div/div[1]'
    numRows = len(driver.find_elements(By.XPATH, batterXPATH + '/div/div/table/tbody/tr'))

    # Array of players on roster
    players = []
    # What positions the league allows (IE 1B, 2B, 1B/2B, etc.)
    league_positions = []
    roster_slots = []
    
    # Loop through each table row in the batter table
    for row in range(1, numRows+1):
        rowXpath = batterXPATH + '/div/div/table/tbody/tr[' + str(row) + ']'
        try:
            '''
            Adding the current row position to the list of league positions.
            current_league_position is an array of strings for each position. So "1B/2B" would become [1B, 2B]
            '''
            current_league_position = driver.find_element(By.XPATH, rowXpath + '/td[1]/div').text
            if current_league_position != "Bench":
                roster_slots.append([current_league_position, row])
                if not league_positions:
                    league_positions.append([current_league_position, 1])
                else:
                    increment = False
                    for slot in league_positions:   
                        if slot[0] == current_league_position:
                            slot[1] += 1
                            increment = True
                    if not increment:
                        league_positions.append([current_league_position, 1])

            # Finds all the positions the player is currently eligble for
            player_positions = driver.find_element(By.XPATH, rowXpath + '/td[2]/div/div/div[2]/div/div[2]/span[2]').text.split(", ")
            player_positions.append("UTIL")

            has_game = bool(driver.find_element(By.XPATH, rowXpath + '/td[5]/div').text)
            name = driver.find_element(By.XPATH, rowXpath + '/td[2]/div/div/div[2]/div/div[1]/span/a').text
            
            # Logic to determine if a player is injured or not
            injured = True
            try:
                el = driver.find_element(By.XPATH, rowXpath + '/td[2]/div/div/div[2]/div/div[1]/span[2]')
                if not el.text:
                    injured = False
            except NoSuchElementException:
                injured = False
            
            # Create Player object using above info and add to players array
            player = Player(name, player_positions, has_game, injured, 1)            
            players.append(player)
        except NoSuchElementException:
            pass

    # Create Roster object using players array and save solved_roster
    roster = Roster(players, league_positions)
    final_roster = roster.solve()

    # Creating string from array to match with format of site
    for slot in final_roster:
        s = "/"
        pos_string = s.join(slot[0])
        slot.append(pos_string)

    # Loading roster into array in better format for actually clicking buttons
    formatted_roster = []
    for slot in final_roster:
        for player in slot[1]:
            formatted_roster.append([slot[2], player])

    # Adding the actuals players into the formatted roster slot
    for pos in roster_slots:
        for index, player in enumerate(formatted_roster):
            if pos[0] == player[0]:
                pos.append(player[1])
                del formatted_roster[index]
                break
    
    # Clicking the buutton to move players to the correct slot
    for slot in roster_slots:
        if 3 == len(slot):
            index = int(driver.find_element(By.XPATH, batterXPATH + '/div/div/table/tbody/tr[.//*[text()="' + slot[2] + '"]]').get_attribute("data-idx"))
            if index + 1 != slot[1]:
                driver.find_element(By.XPATH, batterXPATH + '/div/div/table/tbody/tr[' + str(index + 1) + ']/td[3]/div/div/button').click()
                time.sleep(3)
                try:
                    driver.find_element(By.XPATH, batterXPATH + '/div/div/table/tbody/tr[' + str(slot[1]) + ']/td[3]/div/div/button').click()
                    time.sleep(3)
                except NoSuchElementException:
                    '''
                    This is an edge case where the side doesn't let you move players directly.
                    In this case we move players to the bench first and then move them to the spot
                    '''
                    driver.find_element(By.XPATH, batterXPATH + '/div/div/table/tbody/tr[' + str(numRows+1) + ']/td[3]/div/div/button').click()
                    time.sleep(3)
                    index = int(driver.find_element(By.XPATH, batterXPATH + '/div/div/table/tbody/tr[.//*[text()="' + slot[2] + '"]]').get_attribute("data-idx"))
                    driver.find_element(By.XPATH, batterXPATH + '/div/div/table/tbody/tr[' + str(index + 1) + ']/td[3]/div/div/button').click()
                    time.sleep(3)
                    driver.find_element(By.XPATH, batterXPATH + '/div/div/table/tbody/tr['  + str(slot[1]) + ']/td[3]/div/div/button').click()
                    time.sleep(3)

    # Pitcher
    pitcherXPATH = '//*[@id="fitt-analytics"]/div/div[3]/div/div[3]/div/div/div/div[3]/div/div[2]'
    numRows = len(driver.find_elements(By.XPATH, pitcherXPATH +' /div/div/table/tbody/tr'))
    
    # Array of pitchers on roster
    pitchers = []
    # What positions the league allows (IE 1B, 2B, 1B/2B, etc.). Will be all P in this case.
    league_positions = []
    roster_slots = []

    for row in range(1, numRows+1):
        rowXpath = pitcherXPATH + '/div/div/table/tbody/tr[' + str(row) + ']'
        try:
            current_league_position = driver.find_element(By.XPATH, rowXpath + '/td[1]/div').text
            # Also need to check for IL in case of pitchers.
            if current_league_position != "Bench" and current_league_position != "IL":
                roster_slots.append([current_league_position, row])
                if not league_positions:
                    league_positions.append([current_league_position, 1])
                else:
                    increment = False
                    for slot in league_positions:   
                        if slot[0] == current_league_position:
                            slot[1] += 1
                            increment = True
                    if not increment:
                        league_positions.append([current_league_position, 1])
            # Just use P as position since it can be SP or RP in fantasy
            positions = ["P"]
            has_game = bool(driver.find_element(By.XPATH, rowXpath + '/td[5]/div').text)
            name = driver.find_element(By.XPATH, rowXpath + '/td[2]/div/div/div[2]/div/div[1]/span/a').text
            injured = True
            try:
                el = driver.find_element(By.XPATH, rowXpath + '/td[2]/div/div/div[2]/div/div[1]/span[2]')
                if not el.text:
                    injured = False
            except NoSuchElementException:
                injured = False
            pitcher = Player(name, positions, has_game, injured, 1)
            pitchers.append(pitcher)
        except NoSuchElementException:
            pass

    roster = Roster(pitchers, league_positions)
    final_roster = roster.solve()

    for slot in final_roster:
        slot.append("P")

    formatted_roster = []
    for slot in final_roster:
        for player in slot[1]:
            formatted_roster.append([slot[2], player])

   # Adding the actuals players into the formatted roster slot
    for pos in roster_slots:
        for index, player in enumerate(formatted_roster):
            if pos[0] == player[0]:
                pos.append(player[1])
                del formatted_roster[index]
                break
    
    # Clicking the buutton to move players to the correct slot
    for slot in roster_slots:
        if 3 == len(slot):
            index = int(driver.find_element(By.XPATH, pitcherXPATH + '/div/div/table/tbody/tr[.//*[text()="' + slot[2] + '"]]').get_attribute("data-idx"))
            if index + 1 != slot[1]:
                driver.find_element(By.XPATH, pitcherXPATH + '/div/div/table/tbody/tr[' + str(index + 1) + ']/td[3]/div/div/button').click()
                time.sleep(3)
                try:
                    driver.find_element(By.XPATH, pitcherXPATH + '/div/div/table/tbody/tr[' + str(slot[1]) + ']/td[3]/div/div/button').click()
                    time.sleep(3)
                except NoSuchElementException:
                    '''
                    This is an edge case where the side doesn't let you move players directly.
                    In this case we move players to the bench first and then move them to the spot
                    '''
                    driver.find_element(By.XPATH, pitcherXPATH + '/div/div/table/tbody/tr[' + str(len(roster_slots)+1) + ']/td[3]/div/div/button').click()
                    time.sleep(3)
                    index = int(driver.find_element(By.XPATH, pitcherXPATH + '/div/div/table/tbody/tr[.//*[text()="' + slot[2] + '"]]').get_attribute("data-idx"))
                    driver.find_element(By.XPATH, pitcherXPATH + '/div/div/table/tbody/tr[' + str(index + 1) + ']/td[3]/div/div/button').click()
                    time.sleep(3)
                    driver.find_element(By.XPATH, pitcherXPATH + '/div/div/table/tbody/tr['  + str(slot[1]) + ']/td[3]/div/div/button').click()
                    time.sleep(3)
    driver.close()
