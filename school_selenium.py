# imports driver selections
import time
from selenium import webdriver 
# imports the keyboard simulator
from selenium.webdriver.common.keys import Keys
# imports element types
from selenium.webdriver.common.by import By
# Waiting funtions and condition functions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

# .env file imports
import os
from dotenv import load_dotenv
#import time to get to sortable format
from datetime import datetime

# Function to detect the due date in format so it can be converted
def detect_date_format(date_str):
    # Define regex patterns for different date formats
    patterns = [
        r"Due (\w{3} \d{1,2} at \d{1,2}:\d{2}[APMapm]{2})",  # Format 1: "Due Month Day at Hour:MinuteAM/PM"
        r"(\w{3} \d{1,2})",                                   # Format 2: "Month Day"
        r"(\w{3} \d{1,2}, \d{4})",                            # Format 3: "Month Day, Year"
        r"(\w{3} \d{1,2}, \d{4} at \d{1,2}:\d{2}[APMapm]{2})",  # Format 4: "Month Day, Year at Hour:MinuteAM/PM"
    ]

    for idx, pattern in enumerate(patterns, start=1):
        match = re.match(pattern, date_str)
        if match:
            return idx  # Return the format number if a match is found

    return 0  # Unknown format




# Function to convert due date in format "July 4 at 4pm" to "YYYY-MM-DD HH:MM:SS" so it can be sorted
def convert_date_string(date_str, format_choice):
    try:
        if format_choice == 1:
            # Format: "Due Month Day at Hour:MinuteAM/PM"
            date_object = datetime.strptime(date_str, "Due %b %d at %I:%M%p")
        elif format_choice == 2:
            # Format: "Month Day"
            # Assume the due time is 11:59pm
            date_str += " at 11:59pm"
            date_object = datetime.strptime(date_str, "%b %d at %I:%M%p")
        elif format_choice == 3:
            # Format: "Month Day, Year"
            # Assume the due time is 11:59pm
            date_str += " at 11:59pm"
            date_object = datetime.strptime(date_str, "%b %d, %Y at %I:%M%p")
        elif format_choice == 4:
            # Format: "Month Day, Year at Hour:MinuteAM/PM"
            date_object = datetime.strptime(date_str, "%b %d, %Y at %I:%M%p")
        else:
            return "!No due date!"
    except ValueError:
        pass

    return date_object.strftime("%Y-%m-%d %H:%M:%S") if date_object else None


# loads .env file
load_dotenv()

half_assignment_info_list = []
assignment_info_list = []

# sets the browser to firefox
driver = webdriver.Firefox()

# sets wait timeout
wait = WebDriverWait(driver, timeout=10)


def online():
    # sets url, username, and password
    url = os.getenv('online_url')
    username = os.getenv('email')
    online_password = os.getenv('online_password')

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

    enumerate_assignments()




def regular():
    # gets username/email and password from loaded .env file
    username = os.getenv('email')
    main_password = os.getenv('main_password')
    url = os.getenv('main_url')

    # waits for inital page to load
    driver.implicitly_wait(.05)

    # browses to the canvas page
    driver.get(url)

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

    enumerate_assignments()

def check_grade(class_link):
    grade_link = class_link + "/grades"

    driver.get(grade_link)

    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div[2]/div[3]/div[2]/aside/div/div[1]/span[1]")))
    time.sleep(2)
    grade = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[2]/div[3]/div[2]/aside/div/div[1]/span[1]")

    print(grade)
    grade = grade.text
    print(grade)
    print(grade.strip("%"))
    grade = float(grade.strip("%"))/100

    return grade

def enumerate_assignments():
    # waits until it finds the element the class name
    # NOTE IT HAS TO BE SURROUNDED BY TWO PARENTHESIS OTHERWISE IT LOOKS FOR THE ELEMENT "By.CLASS_NAME" WHICH IS NOT WHAT ITS SUPPOSED TO BE LOOKING FOR
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ic-DashboardCard__link")))

    class_links = []

    # Find all courses' link
    dashboard_links = driver.find_elements(By.CLASS_NAME, "ic-DashboardCard__link")

    # I put this in a seperate link list because if I navigate to other pages the selenium objects break
    for dashboard_link in dashboard_links:
        linked = dashboard_link.get_attribute("href")
        class_links.append(linked)
        print(class_links)
        print("\n")

    # Find all Course names
    course_names = driver.find_elements(By.CLASS_NAME, "ic-DashboardCard")

    courses = []

    for course_name in course_names:
        lablenm = course_name.get_attribute("aria-label")
        courses.append(lablenm)
        print(lablenm)



    # Gets base url to piece together the half url from href
    base_url = driver.current_url

    # Set counter to get the right course name from the list
    c = 0

    # Loop through the found elements and extract their href
    for link in class_links:
        href = link
        class_name = courses[c]
        assignment_page = True
        class_grade = check_grade(href)
        if href:
            # Combine base url with half href to make it complete
            print("printing base_url: ", base_url, "\nprinting href: ", href, "\n")
            absolute_url =  href + "/assignments"
            # debug check
            print("printing absolute_url", absolute_url)
            # Navigate to whole url
            driver.get(absolute_url)

            # Checks if the course actually goes to the assignments page(checks if the page is the main course url which in the case of no assignments page it will be redirected to) 
            # If the course does not have a assignments page navigate to modules page instead.
            if driver.current_url != absolute_url:
                print("! Course doesn't have a Assignments page going to Modules page !")
                assignment_page = False
                driver.get( href + "/modules")

            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ig-info")))
            #inside course
            time.sleep(2)
            # Find all parent elements with class "ig-info"
            ig_info_elements = driver.find_elements(By.CLASS_NAME, "ig-info")


            for ig_info in ig_info_elements:
                print(ig_info)
                assignment_data1 = {}
                
                if assignment_page:
                    # Extract assignment name and href on assignments page
                    ig_title = ig_info.find_element(By.CLASS_NAME, "ig-title")
                    assignment_data1["name"] = ig_title.text
                    assignment_data1["href"] = ig_title.get_attribute("href")

                    try:
                        ig_details = ig_info.find_element(By.CLASS_NAME, "ig-info")
                        due_date_element = ig_details.find_element(By.CLASS_NAME, "ig-details__item.assignment-date-due")
                        print(due_date_element)
                        due_date_text = due_date_element.find_element(By.TAG_NAME, "span").text
                        print(due_date_text)
                        # Decide what format it is and add it to formatnum to be passed in to tell the converter which format converter to use
                        formatnum = detect_date_format(due_date_text)
                        # Convert the date string to the right format and store it in the dictionary
                        assignment_data1["due_date"] = convert_date_string(due_date_text, formatnum)
                    except:
                        # No due date case
                        assignment_data1["due_date"] = "N/A"
                        print("! No due date for this assignment !")

                    assignment_data1["class"] = course_name
                    assignment_data1["class_grade"] = class_grade
                    # Add the assignment data to the list
                    print(assignment_data1)
                    half_assignment_info_list.append(assignment_data1)

                else:
                    ig_title = ig_info.find_element(By.TAG_NAME, "a")
                    
                    if (ig_info.find_element(By.XPATH, "../span")).get_attribute("title") == "Page" :
                        print("its a page......")
                        pass
                    print(ig_title)
                    link = ig_title.get_attribute("href")
                    print(link+"\n")
                    assignment_data1["name"] = ig_title.text
                    assignment_data1["href"] = ig_title.get_attribute("href")

                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "due_date_display")))

                    due_date_text = driver.find_element(By.CLASS_NAME, "due_date_display")

                    print(due_date_text)

                    due_date_text = due_date_text.text

                    formatnum = detect_date_format(due_date_text)

                    assignment_data1["due_date"] = convert_date_string(due_date_text, formatnum)
                    assignment_data1["class"] = course_name
                    assignment_data1["class_grade"] = class_grade
                    print(assignment_data1)
                    half_assignment_info_list.append(assignment_data1)
        
        print("Changing class now")
        c += 1

    add_completion_check(half_assignment_info_list)

    driver.close()

def add_completion_check(unfinished_list):
    for each in unfinished_list:
        assignment_data = {}

        name = each["name"]
        href = each["href"]
        due_date = each["due_date"]
        class_name = each["class"]
        class_grade = each["class_grade"]

        print(href)
        driver.get(href)

        # Attempt to get status of assignment via progress circle screen reader object
        try:
            circle_element = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[2]/div[3]/div[1]/div/div/div[2]/div[1]/span/span[1]/span/span[2]/div/span/span[1]/div/span/progress")
            circle_progress = circle_element.get_attribute("value")

            if circle_progress == "1":
                # TODO finish this \/ \/ \/ \/ \/ \/ \/ \/
                # Need to Submit, this is really the only one I need
                assignment_data["name"] = name
                assignment_data["href"] = href
                assignment_data["due_date"] = due_date
                assignment_data["class"] = class_name
                assignment_data["class_grade"] = class_grade
                assignment_info_list.append(assignment_data)
            elif circle_progress == "2":
                # Submitted and review feedback
                print(name+" is submitted and review feedback")
            elif circle_progress == "3":
                # Still need to find an instance to tell what the value 3 means :(
                print(name+" is the special 3 value")
            else:
                print("! error no circle value found !")
                print("Trying grade method.....")
                # TODO grade method for special case like math
                try:
                    pass
                except:
                    pass
        except: 
            print("error")

def assignment_sort():
    today = datetime.now()
    sorted_list = sorted(assignment_info_list, key=lambda x: (datetime.fromisoformat(x["due_date"]), x["class_grade"]))
    return sorted_list

def assignment_print(sorted_assignment_info_list):
    # give some room between the debug prints
    print("\n\n\n\n\n\n")

    # Print the half_assignment_info_list containing dictionaries full of the assignment the data 
    for assignment_data in sorted_assignment_info_list:
        print("Name: ", assignment_data["name"])
        print("Link: ", assignment_data["href"])
        print("Due Date (Sortable): ", assignment_data["due_date"])
        print("Class: ", assignment_data["class"])
        print("Class Grade: ", assignment_data["class_grade"])
        print("\n")



online()
enumerate_assignments()
regular()
enumerate_assignments()

sorted_list = assignment_sort()
assignment_print(sorted_list)