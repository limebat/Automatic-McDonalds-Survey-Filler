from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
import time
import pyperclip
import random

def generate_response():
    responses = [
        "The friendly staff and quick service at McDonald's always make my day.",
        "McDonald's consistently delivers on taste and quality with their diverse menu.",
        "I'm a fan of the clean and welcoming environment at McDonald's restaurants.",
        "The convenience of McDonald's drive-thru and speedy service is unmatched.",
        "McDonald's never fails to provide a satisfying and enjoyable dining experience.",
        "The variety of options on the menu ensures there's something for everyone.",
        "The tasty and affordable meals at McDonald's keep me coming back for more.",
        "McDonald's commitment to quality ingredients is evident in every bite.",
        "The efficient and courteous service at McDonald's sets the standard for fast food.",
        "I appreciate the effort McDonald's puts into maintaining a clean and hygienic space."
    ]
    return random.choice(responses)

def XPathSearchByValue(answer_value):
    # Find the radio button by the value attribute
    element_button = driver.find_element_by_xpath(f"//input[@value='{answer_value}']")
    # Click the radio button
    try:
        element_button.click()
    except ElementClickInterceptedException:
        # If ElementClickInterceptedException occurs, try clicking using JavaScript
        driver.execute_script("arguments[0].click();", element_button)
    
def XPathSearch(search_text):
    # Find elements containing the specified text using XPath
    elements_with_text = driver.find_elements_by_xpath(f"//*[contains(text(), '{search_text}')]")
    for element in elements_with_text:
        element.click()

def Click(element_id):
    try:
        # Wait for the element to be clickable
        element_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, element_id))
        )
        element_button.click()
    except ElementClickInterceptedException:
        try:
            # If ElementClickInterceptedException occurs, try clicking using JavaScript
            element_button = driver.find_element_by_id(element_id)
            driver.execute_script("arguments[0].click();", element_button)
        except NoSuchElementException:
            print(f"Element with ID {element_id} not found.")
            # Handle the exception as needed
    except NoSuchElementException:
        print(f"Element with ID {element_id} not found.")
        # Handle the exception as needed

def insert_clipboard_into_array(string_array):
    # Get the contents of the clipboard
    clipboard_content = pyperclip.paste()
    # Split the clipboard content using '-' as the delimiter
    split_content = clipboard_content.split('-')
    string_array.extend(split_content)

debugTime = 380  

# Specify the path to chromedriver.exe
chromedriver_path = r'C:\Users\willi\OneDrive\Documents\Visual Studio Code [Not Microsoft]\McDonaldSurvey\chromedriver-win64\chromedriver.exe'
driver = webdriver.Chrome(executable_path=chromedriver_path)

# Open the website
driver.get("https://www.mcdvoice.com/")

# Array to store survey passwords
password = []

previous_clipboard_content = pyperclip.paste()

while pyperclip.paste() == previous_clipboard_content:
    time.sleep(1)  # Add a small delay to avoid continuous checking

insert_clipboard_into_array(password)
print("The current password is", password)

# Loop to find survey code input elements by ID
for i, password in enumerate(password):
    element_id = f"CN{i + 1}"  # Increment by 1 to match the list index of McDonalds
    survey_code_input = driver.find_element_by_id(element_id)
    survey_code_input.send_keys(str(password))  # Convert the password to a string and send it

time.sleep(0.5)

# Find and click the "Start" button to begin survey
start_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "NextButton"))
)
start_button.click()

#START THE SURVEY
for i in range(18):  # You can adjust the range as needed
    try:
        # Check if the specified string is present
        if driver.find_elements_by_xpath("//th[@id='textR016000']"):
            XPathSearchByValue(2)
        else:
            XPathSearchByValue(1)

        # Check if there are elements with the value 5
        if driver.find_elements_by_xpath("//input[@value='5']"):
            # Find all label elements associated with input elements having value="5"
            label_elements = driver.find_elements_by_xpath('//input[@value="5"]/following-sibling::label')

            # Loop through each label element and click it
            for label in label_elements:
                try:
                    label.click()
                    print(f"Clicked on label associated with input ID: {label.find_element_by_xpath('preceding-sibling::input').get_attribute('id')}")
                except NoSuchElementException:
                    print("Element not found")
    except:
        # Find the textarea by ID
        textarea_element = driver.find_element_by_id("S081000")
        responses = generate_response()
        textarea_element.click()
        textarea_element.send_keys(responses)
    Click("NextButton")
    
# Wait for the validation code element to be present
validation_code_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "ValCode"))
)

# Extract the validation code text
validation_code_text = validation_code_element.text

# Print the validation code
print("Validation Code:", validation_code_text)

# You can perform additional actions or print statements here if needed
# Close the browser after a brief pause (you can adjust the time if needed)
time.sleep(debugTime)
driver.quit()