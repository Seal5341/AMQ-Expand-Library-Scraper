# -*- coding: utf-8 -*-
"""
@author: Seal

"""

import csv
import traceback
import time
from datetime import datetime
from userpass import userpass_combo
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
# from selenium.webdriver.common.action_chains import ActionChains

filename = datetime.now().strftime("%Y%m%d") + '.csv'

count = 0
prev_link = ''
old_anime_name = ''
lengthdict = {}

print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Starting run')
starttime = time.time()

# start web browser
driver = webdriver.Firefox() # firefox is faster than chrome and edge, not sure if headless works
driver.maximize_window()
# action = ActionChains(driver)

# login - enter your own username and password
driver.get("https://animemusicquiz.com/")
loginUser = driver.find_element_by_id("loginUsername")
loginUser.send_keys(userpass_combo()[0])
loginPass = driver.find_element_by_id("loginPassword")
loginPass.send_keys(userpass_combo()[1])
loginPass.send_keys(Keys.RETURN)

# expandlibrary
print('Waiting for menu to load...')
expandbutton = WebDriverWait(driver, 9999).until(EC.presence_of_element_located((By.ID,'mpExpandButton')))
loading_screen = driver.find_element_by_id('loadingScreen')
WebDriverWait(driver, 9999).until(EC.invisibility_of_element_located(loading_screen))
cookie = driver.find_element_by_class_name('cc-compliance')
cookie.click()
expandbutton.click()
print('Waiting for expand library to load...')
expand = WebDriverWait(driver, 9999).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'elQuestion')))
totalnumberofentries = len(expand) - 1 # first entry is a dummy
lengthdict[0] = totalnumberofentries
print('Expand library loaded with', totalnumberofentries, 'anime')

# open file for saving data
file = open(filename, 'w', newline='', encoding='utf-8')
file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
file_writer.writerow(['Anime Name', 'Song Type', 'Song Name', 'Song Artist', 'Mp3 Link', 'Webm Link'])

# calls to driver
mp3button = driver.find_element_by_id('elSelectorOptionMp3')
inputvideo = driver.find_element_by_id('elInputVideo')

# iterate through anime list
try:
    for elQuestion in expand[1:]: # first entry is a dummy
        try:
            # open anime box
            driver.execute_script('arguments[0].scrollIntoView();', elQuestion)
            anime_name = elQuestion.find_element_by_xpath('.//div[@class="elQuestionAnimeName"]').text
            elQuestion.click()
            
            # song box
            songinfos = elQuestion.find_elements_by_xpath('.//div[@class="elQuestionSongInfo"]')
            
            linecontainer = []
            for song_info in songinfos:
                
                # click on song
                driver.execute_script("arguments[0].scrollIntoView();", song_info)
                song_info.click()
                
                webm_link = inputvideo.get_attribute('src').split('/')[-1]
                if webm_link != prev_link:
                    prev_link = webm_link
                else:
                    webm_link = 'Not Found'
                
                try:
                    mp3button.click() # element not interactable error if doesnt exist
                    mp3_link = inputvideo.get_attribute('src').split('/')[-1]
                    if mp3_link != prev_link:
                        prev_link = mp3_link
                    else:
                        mp3_link = 'Not Found'
                except:
                    mp3_link = 'Not Found'
                
                # get song info and save
                song_type = song_info.find_element_by_xpath('.//div[@class="elQuestionSongType"]').text
                song_name = song_info.find_element_by_xpath('.//div[@class="elQuestionSongName"]').text
                song_artist = song_info.find_element_by_xpath('.//div[@class="elQuestionSongArtist"]').text
                
                linecontainer.append([anime_name, song_type, song_name, song_artist, mp3_link, webm_link])
            
            # click to close anime box
            # driver.execute_script('arguments[0].scrollIntoView();', elQuestion)
            # elQuestion.click()
            
            for ln in linecontainer:
                file_writer.writerow(ln)
            
            count += 1
            old_anime_name = anime_name
            if count%10 == 0:
                print('Anime #' + str(count) + ':', linecontainer[-1])
        
        except NoSuchElementException: # for first elQuestion object
            print('Element not found')
            continue
except ElementClickInterceptedException:
    print('Click intercepted, restarting browser')
except ElementNotInteractableException:
    print('Scroll intercepted, restarting browser')
except:
    traceback.print_exc()

print('Last Anime: #' + str(count), old_anime_name)
file.close() # close periodically to save data
driver.quit()

print('Initial run complete, running loop now')
runcount = 1

# iterate through anime list
while count < totalnumberofentries:
    # open file for saving data
    file = open(filename, 'a+', newline='', encoding='utf-8')
    file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # file_writer.writerow(['Anime Name', 'Song Type', 'Song Name', 'Song Artist', 'Mp3 Link', 'Webm Link'])
    
    print('Waiting for auto logout...\n')
    time.sleep(30) # dodge login confirmation due to imcomplete logout
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Loop #' + str(runcount))
    
    # start web browser
    driver = webdriver.Firefox() # firefox is faster than chrome and edge, not sure if headless works
    driver.maximize_window()
    # action = ActionChains(driver)
    
    try:
        # login - enter your own username and password
        driver.get("https://animemusicquiz.com/")
        loginUser = driver.find_element_by_id("loginUsername")
        loginUser.send_keys(userpass_combo()[0])
        loginPass = driver.find_element_by_id("loginPassword")
        loginPass.send_keys(userpass_combo()[1])
        loginPass.send_keys(Keys.RETURN)
        
        # expandlibrary
        print('Waiting for menu to load...')
        expandbutton = WebDriverWait(driver, 9999).until(EC.presence_of_element_located((By.ID,'mpExpandButton')))
        loading_screen = driver.find_element_by_id('loadingScreen')
        WebDriverWait(driver, 9999).until(EC.invisibility_of_element_located(loading_screen))
        cookie = driver.find_element_by_class_name('cc-compliance')
        cookie.click()
        expandbutton.click()
        print('Waiting for expand library to load...')
        expand = WebDriverWait(driver, 9999).until(EC.presence_of_all_elements_located((By.CLASS_NAME,'elQuestion')))
        totalentries = len(expand) - 1
        lengthdict[runcount] = totalentries
        print('Expand library loaded with', totalentries, 'anime') # first entry is a dummy
        
        # calls to driver
        mp3button = driver.find_element_by_id('elSelectorOptionMp3')
        inputvideo = driver.find_element_by_id('elInputVideo')
        
        for elQuestion in expand[count+1:]:
            # open anime box
            driver.execute_script('arguments[0].scrollIntoView();', elQuestion)
            anime_name = elQuestion.find_element_by_xpath('.//div[@class="elQuestionAnimeName"]').text
            elQuestion.click()
            
            # song box
            songinfos = elQuestion.find_elements_by_xpath('.//div[@class="elQuestionSongInfo"]')
            
            linecontainer = []
            for song_info in songinfos:
                
                # click on song
                driver.execute_script("arguments[0].scrollIntoView();", song_info)
                song_info.click()
                
                webm_link = inputvideo.get_attribute('src').split('/')[-1]
                if webm_link != prev_link:
                    prev_link = webm_link
                else:
                    webm_link = 'Not Found'
                
                try:
                    mp3button.click() # element not interactable error if doesnt exist
                    mp3_link = inputvideo.get_attribute('src').split('/')[-1]
                    if mp3_link != prev_link:
                        prev_link = mp3_link
                    else:
                        mp3_link = 'Not Found'
                except:
                    mp3_link = 'Not Found'
                
                # get song info and save
                song_type = song_info.find_element_by_xpath('.//div[@class="elQuestionSongType"]').text
                song_name = song_info.find_element_by_xpath('.//div[@class="elQuestionSongName"]').text
                song_artist = song_info.find_element_by_xpath('.//div[@class="elQuestionSongArtist"]').text
                
                linecontainer.append([anime_name, song_type, song_name, song_artist, mp3_link, webm_link])
            
            # click to close anime box
            # driver.execute_script('arguments[0].scrollIntoView();', elQuestion)
            # elQuestion.click()
            
            for ln in linecontainer:
                file_writer.writerow(ln)
            
            count += 1
            old_anime_name = anime_name
            if count%10 == 0:
                print('Anime #' + str(count) + ':', linecontainer[-1])
            
    except ElementClickInterceptedException:
        print('Click intercepted, restarting browser')
    except ElementNotInteractableException:
        print('Scroll intercepted, restarting browser')
    except KeyboardInterrupt:
        print('Keyboard Interrupt')
        file.close()
        break
    except:
        traceback.print_exc()
    
    print('Last Anime: #' + str(count), old_anime_name)
    file.close() # close periodically to save data
    driver.quit()
    runcount += 1

file.close()
timetaken = time.time() - starttime
print('Time taken:', timetaken/3600, 'hours')
print('Total anime scraped:', count)
print(lengthdict)