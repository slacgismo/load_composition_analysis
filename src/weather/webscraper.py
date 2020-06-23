from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import numpy as np
import pandas as pd
import os
import config_default
try:
    import config_user
except:
    raise Exception("you have not created 'config.py'")

'''
This file contains a few functions that allow one to automate webscraping LCD data from the NOAA website. The first function makes
data requests, the second function retrieves the data (downloads the relevant csv files) when it becomes available, and the third function
renames the csv files to make organization easy

I have added some basic functionality to the function that should allow it to deal with common errors
- sleep times after opening a new webpage (allows time for driver to load new html script - customize the sleep times)
- Multiple click commands (for some reason my driver would not respond to single click commands, but would click the relevant buttons 
when I used multiple click commands. I have commented out multiple click commands in the python script. You can use them if you face
similar issues)
- Retry - Sometimes the driver/wepbage throw up random errors. This is dealt with by running the script up to 3 times for each wban code.
The script will move to the next wban code once it successfully makes a request or 3 tries are up. In the latter case, the function returns
an error message and moves to the next wban code.

Scraping HTML and Javascript tends to throw up random errors which I was unable to deal with in an efficient manner. I have added some 
debugging tools to the file_requester function that help simplify dealing with the errors.
 - error list - returns a list of wban codes that couldn't be requested
 - string - sometimes the webpage doesn't process the email id properly, which leads to the script copying the term 'Climatological' from 
 the order summary table instead of the order id. The function must be re run for wban codes that return the term 'Climatological'
 - date range - some wban codes can't be ordered as they don't have data in the sufficient date range. In this case, either manually 
 request the data within the limited date range, or find the wban code of the closest station and run the script on that wban code.
'''
'''
HOW TO RUN THE CODE
#Obtaining data from 1990-01-01 to 1999-12-31
locations = pd.read_csv("locations.csv")
locations= locations[["location", "city", "zipcode"]]
zipcodes = np.array(locations["zipcode"])[:66]
wban = pd.read_csv("WBAN dir.csv")
wban_list = np.array(wban["WBAN"])
location_abbrev = np.array(locations["location"])

result = file_requester(wban_list, config.email)
#Wait until all the requests are submitted and processed and the data is available
file_downloader(result, config.email)
#Wait until all downloads are complete
file_renamer(result, wban_list, location_abbrev, "199")
'''
def file_requester(zipcodes_array, email_id):
    '''
    The function takes as input an array of WBAN numbers and an email id to use on the NOAA website. For each WBAN number,
    it navigates through the NOAA webpage and orders a CSV file of LCD data for a given date range
    '''
    zipcode_list = list(zipcodes_array)
    order_list = []
    error_list = [] #Debugging tool - tells you which WBAN numbers the webscraper was unable to make orders for
    broken_link_list = []
    string=[] #Debugging tool - Returns the order summary table for each order as a string
    for i in zipcode_list:
        for retry in range(3):
            driver = webdriver.Chrome(config.chrome)
            #You will need to change the above line to the webdrive you use and where you have it installed
            try:
                driver.get("https://www.ncdc.noaa.gov/cdo-web/datasets/LCD/stations/" + str(i) + "/detail")
                #Looks for the wepbage for the given wban code
                time.sleep(1)
                try:
                    add = driver.find_element_by_xpath("//a[text()='Add to Cart']")
                except NoSuchElementException:
                    #If webpage doesn't exist
                    print("Zipcode " + i + " has no match in the NOAA LCD database")
                    print("deleted zipcode " + i + " from list")
                    break
                else:
                    add.click()
                    driver.find_element_by_xpath("//a[@id='widgetBody']").send_keys(Keys.ENTER)
                    #Adds item to checkout cart
                    time.sleep(3)
                    driver.find_element_by_xpath("//input[@id='LCD_CUSTOM_CSV']").click()
                    #driver.find_element_by_xpath("//input[@id='LCD_CUSTOM_CSV']").click()
                    #Selects CSV option

                    start =driver.find_element_by_xpath("//input[@name='dataStartDate']")
                    driver.execute_script("arguments[0].setAttribute('value','2010-01-01')", start)
                    end =driver.find_element_by_xpath("//input[@name='dataEndDate']")
                    driver.execute_script("arguments[0].setAttribute('value','2019-12-31')", end)

                    driver.find_element_by_xpath("//input[@class='noaa-daterange-input']").send_keys("2010-01-01 to 2019-12-31")
                    #Changes date range
                    #Customize the above code to obtain a desired date range


                    driver.find_element_by_xpath("//button[@class='button cartButton floatRight']").click()
                    #driver.find_element_by_xpath("//button[@class='button cartButton floatRight']").click()
                    #driver.find_element_by_xpath("//button[@class='button cartButton floatRight']").click()
                    time.sleep(3)

                    driver.find_element_by_xpath("//input[@id='email']").send_keys(email_id)
                    driver.find_element_by_xpath("//input[@name='emailConfirmation']").send_keys(email_id)
                    #Enters email id
                    driver.find_element_by_xpath("//input[@id='buttonSubmit']").send_keys(Keys.ENTER)
                    #Submits order
                    time.sleep(3)
                    table_id = driver.find_element_by_class_name('reviewTable')
                    order = table_id.text.split('\n')[1].split(' ')[2]
                    #Extracts order id from the order summary table

                    order_list.append((i,order))
                    string.append(table_id.text.split('\n'))
                    print("deleted zipcode " + i + " from list")
                    driver.quit()
                    break
            except:
                print("Error in processing zipcode " + i)
                if retry ==2:
                    error_list.append(i)
                    print("Can't resolve error for zipcode "+ i)
                driver.quit()
                continue

    return order_list#, zipcode_list, error_list, string

def file_downloader(orders, email_id):
    '''
    Downloads data from the NOAA website once it becomes available. Takes as input a list of tuples containing WBAN code and a respective 
    order id (same format as output of file_requester) and the email id with which the order was made.
    '''
    for i in orders:
        order_id = i[1] #Extracts the order_id
        driver = webdriver.Chrome(config.chrome)
        driver.get("https://www.ncdc.noaa.gov/cdo-web/orders?email=" + email + "&id=" + order_id) #Retrieves order status page
        driver.get("https://www.ncei.noaa.gov/orders/cdo/" + order_id + ".csv")# Downloads csv file
        #time.sleep(45) #Sleep time to allow file to download in case webdriver force closes window. Uncomment if required.

def file_renamer(orders, wban_list, location_abbrev, file_suffix)
'''
Renames downloaded csv files. Takes as input the aforementioned order list, a list of wban_codes, a list of location codes and a file suffix. 
Ensure that wban_list and location_abbrev are sorted the same way. Ideally these will be extracted from the same dataset, so the sort 
should already be the same. The file suffix corresponds to the date range (199,200 or 201).
'''
    for i in orders:
        order_id = i[1]
        os.rename(config.localdata + "\\" + order_id +".csv",config.localdata+"\\"+location_abbrev[list(wban_list).index(i[0])] + "-" + file_suffix +".csv")
        #Change the above line to the location of your file downloads and where you want to store the renamed files.
        print(i[0] + " processed")