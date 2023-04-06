import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from player import Player
from roster import Roster

def click_roster(driver: webdriver, pitcher: bool, xpath: str):
    numRows = len(driver.find_elements(By.XPATH, xpath + '/div/div/table/tbody/tr'))
    
     # Array of players on roster
    players = []
    # What positions the league allows (IE 1B, 2B, 1B/2B, etc.)
    league_positions = []
    roster_slots = []
    
    # Loop through each table row in the batter table
    for row in range(1, numRows+1):
        rowXpath = xpath + '/div/div/table/tbody/tr[' + str(row) + ']'
        try:
            '''
            Adding the current row position to the list of league positions.
            current_league_position is an array of strings for each position. So "1B/2B" would become [1B, 2B]
            '''
            current_league_position = driver.find_element(By.XPATH, rowXpath + '/td[1]/div').text
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

            # Finds all the positions the player is currently eligble for
            if pitcher:
                player_positions = ["P"]
            else:    
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
        if pitcher:
            pos_string = "P"
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
            index = int(driver.find_element(By.XPATH, xpath + '/div/div/table/tbody/tr[.//*[text()="' + slot[2] + '"]]').get_attribute("data-idx"))
            if index + 1 != slot[1]:
                driver.find_element(By.XPATH, xpath + '/div/div/table/tbody/tr[' + str(index + 1) + ']/td[3]/div/div/button').click()
                time.sleep(3)
                try:
                    driver.find_element(By.XPATH, xpath + '/div/div/table/tbody/tr[' + str(slot[1]) + ']/td[3]/div/div/button').click()
                    time.sleep(3)
                except NoSuchElementException:
                    '''
                    This is an edge case where the side doesn't let you move players directly.
                    In this case we move players to the bench first and then move them to the spot
                    '''
                    if pitcher:
                        driver.find_element(By.XPATH, xpath + '/div/div/table/tbody/tr[' + str(len(roster_slots)+1) + ']/td[3]/div/div/button').click()
                    else:
                        driver.find_element(By.XPATH, xpath + '/div/div/table/tbody/tr[' + str(numRows+1) + ']/td[3]/div/div/button').click()
                    time.sleep(3)
                    index = int(driver.find_element(By.XPATH, xpath + '/div/div/table/tbody/tr[.//*[text()="' + slot[2] + '"]]').get_attribute("data-idx"))
                    driver.find_element(By.XPATH, xpath + '/div/div/table/tbody/tr[' + str(index + 1) + ']/td[3]/div/div/button').click()
                    time.sleep(3)
                    driver.find_element(By.XPATH, xpath + '/div/div/table/tbody/tr['  + str(slot[1]) + ']/td[3]/div/div/button').click()
                    time.sleep(3)