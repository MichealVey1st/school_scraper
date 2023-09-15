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

# sets url, username, and password
url = os.getenv('online_url')
username = os.getenv('username')
online_password = os.getenv('online_password')

# sets the browser to firefox
driver = webdriver.Firefox()

# sets wait timeout
wait = WebDriverWait(driver, timeout=10)

# waits for inital page to load
driver.implicitly_wait(.05)

# gets url
driver.get(url)

# finds username input element via id
element_username = driver.find_element(by=By.ID, value="pseudonym_session_unique_id")
# types username into username element
element_username.send_keys(username)

# finds password input element via id
element_password = driver.find_element(by=By.ID, value='pseudonym_session_password')
# types password into the password element
element_password.send_keys(online_password)
# submits the login
element_password.submit()

# waits until it finds the element the class name
# NOTE IT HAS TO BE SURROUNDED BY TWO PARENTHESIS OTHERWISE IT LOOKS FOR THE ELEMENT "By.CLASS_NAME" WHICH IS NOT WHAT ITS SUPPOSED TO BE LOOKING FOR
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ic-DashboardCard__link")))

# todo
# find each link to my courses from dashboard
# iterate through all the assignments in a course
# get due date, name, and link to assignment
# take each assignment and sort according to due date
# possibly put certain classes assignmets first
# navigate to other canvas as put together in addon.py

course_links = driver.find_element(By.LINK_TEXT, "courses")


driver.close()