# imports driver selections
from selenium import webdriver 
# imports the keyboard simulator
from selenium.webdriver.common.keys import Keys
# imports element types
from selenium.webdriver.common.by import By
# Waiting funtions and condition functions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# .env file imports
import os
from dotenv import load_dotenv

# loads .env file
load_dotenv()

# gets username/email and password from loaded .env file
username = os.getenv('username')
main_password = os.getenv('main_password')

# sets the browser to firefox
driver = webdriver.Firefox()

# sets wait timeout
wait = WebDriverWait(driver, timeout=10)

# waits for inital page to load
driver.implicitly_wait(.05)

# browses to the canvas page
driver.get()

# finds the link for student and clicks it sending to the google login
driver.find_element(By.ID, 'students').click()

# declares the email login textbox
google_username = driver.find_element(By.ID, 'identifierId')
# sends password to the input box then presses enter to go to the next page
google_username.send_keys(username, Keys.ENTER)

# makes program wait until it finds the password login element
# NOTE IT HAS TO BE SURROUNDED BY TWO PARENTHESIS OTHERWISE IT LOOKS FOR THE ELEMENT "By.XPATH" WHICH IS NOT WHAT ITS SUPPOSED TO BE LOOKING FOR
wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name = 'password']")))
# declares the password input box element
google_password = driver.find_element(By.XPATH, "//input[@name = 'password']")
# sends password and presses enter to submit
google_password.send_keys(main_password, Keys.ENTER)