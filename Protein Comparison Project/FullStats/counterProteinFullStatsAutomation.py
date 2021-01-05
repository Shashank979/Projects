###IMPORTS###
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
###IMPORTS###

###TBD###
#Should there be way so that if file has been moved (os.path.exists) then something is printed?
###TBD###


file_name = 'pdb_seqres.txt'


def download_automation():
    #downloading the pdb_seqres.txt from the rcsb website 
    opts = Options()
    #opts.headless = True
    driver = webdriver.Chrome('/Users/shashank/Library/Mobile Documents/com~apple~CloudDocs/ExtraTime/Programming/Python/Webscraping/Selenium/chromedriver', options = opts) 
    driver.get('https://www.rcsb.org/pdb/static.do?p=general_information/about_pdb/summaries.html')
    link = driver.find_element_by_link_text('pdb_seqres.txt')
    link.click()
    #waiting for pdb_segres.txt file to be in downloads file before quitting driver 
    time_counter = 0
    iteration_wait = 5
    minutes_unusual_download = 20 
    while True:
        #if the file is in the downloads folder then exits 
        if os.path.exists('/Users/shashank/Downloads/' + file_name):
            print("~Elapsed Download Time:", iteration_wait * time_counter, "Seconds")
            break
        #exits if certain amount of time has elapsed 
        elif time_counter * iteration_wait >= minutes_unusual_download * 60:
            print("Quit driver due to unusually long download time")
            print("~Time Elapsed Before Driver Quit: ", time_counter * iteration_wait)
            break
        #else sleeps for certain amount of time 
        else:
            print("Downloading...")
            time.sleep(iteration_wait)
            time_counter += 1
    driver.quit()
    #moves file 
    old_path = '/Users/shashank/Downloads/' + file_name 
    new_path = '/Users/shashank/Library/Mobile Documents/com~apple~CloudDocs/ExtraTime/Biology/BioProgramming/DataAnalysis/CounterProtein/FullStats/pdb_seqres.txt'
    os.rename(old_path, new_path)