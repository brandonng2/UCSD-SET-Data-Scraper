from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
import time
import getpass
import sys
from bs4 import BeautifulSoup
import pandas as pd
import re

# Function to login
def login(driver, username, password):
    try:
        # Change Student SSO if logging in with other methods (ie: Business Systems or Active Directory)
        wait = WebDriverWait(driver, 60)
        sign_dropdown = Select(wait.until(EC.presence_of_element_located((By.ID, "authtype"))))
        sign_dropdown.select_by_visible_text('Student SSO')

        username_bar = wait.until(EC.presence_of_element_located((By.ID, "ssousername")))
        username_bar.clear()
        username_bar.send_keys(username)

        password_bar = wait.until(EC.presence_of_element_located((By.ID, "ssopassword")))
        password_bar.clear()
        password_bar.send_keys(password)
        password_bar.send_keys(Keys.RETURN)

        # Check for login error with username or password
        try:
            driver.find_element(By.ID, '_login_error_message')
            print('Error when logging in: Incorrect username or password')
            sys.exit()
        except:
            # Processed to DUO Mobile authentication 
            duo_auth = wait.until(EC.presence_of_element_located((By.ID, "trust-browser-button")))
            duo_auth.click()

    except TimeoutException:
        print('Error when logging in: Timed out')
        sys.exit()


# Return unit dropdown element (first dropdown element on page) as Select object
def get_unit_dropdown(driver):
    wait = WebDriverWait(driver, 60)
    u_d = Select(wait.until(EC.presence_of_element_located((By.TAG_NAME, 'select'))))
    wait.until(lambda x: len(u_d.options) > 1) 
    return u_d

# Return course dropdown element (second dropdown element on page) as Select object
def get_course_dropdown(driver):
    wait = WebDriverWait(driver, 60)
    all_selects = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'select')))
    c_d = Select(all_selects[1])
    wait.until(lambda x: len(c_d.options) > 1)
    return c_d

# Return cleaned text that removes whitespace after scraping data
def clean_text(text):
    cleaned_text = text.strip()
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text

# Parse web page and concat data to DataFrame
def scrape_data(driver, df):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    set_table = soup.find(id='ContentPlaceHolder1_EvalsContentPlaceHolder_pnlSETs')
    table_body = set_table.find('tbody')
    rows = table_body.find_all('tr')
    extracted_rows = []
    for row in rows:
        cols = row.find_all('td')
        row_data = [clean_text(col.get_text()) for col in cols]
        extracted_rows.append(row_data)
        
    new_data_df = pd.DataFrame(extracted_rows, columns=df.columns)
    new_df = pd.concat([df, new_data_df], ignore_index=True)
    return new_df

# Main script
if __name__ == "__main__":
    username = str(input("Enter your TritonLink username: "))
    password = str(getpass.getpass("Enter your password: "))

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        driver.get("https://academicaffairs.ucsd.edu/Modules/Evals/SET/Reports/Search.aspx")
        
        # Login to the website
        login(driver, username, password)
        print('Successfully logged in')

        # Create initial DataFrame
        columns = ['Instructor', 'Course', 'Term','Enrolled/Response Rate','Avg Grade Recieved', 
                   'Avg Hours Worked', 'Student Learning', 'Course Structure', 'Class Environment']
        eval_df = pd.DataFrame(columns=columns)

        # Nested for-loop looping through units and respective courses and scraping data
        unit_dropdown = get_unit_dropdown(driver)
        unit_options = [option.text for option in unit_dropdown.options[1:]]
        for unit in unit_options:
            try:
                unit_dropdown.select_by_visible_text(unit)
            except StaleElementReferenceException:
                unit_dropdown = get_unit_dropdown(driver)
                unit_dropdown.select_by_visible_text(unit)
            print(f'Department: {unit}')
            time.sleep(1)
            course_dropdown = get_course_dropdown(driver)
            course_options = [option.text for option in course_dropdown.options[1:]]
            for course in course_options:
                try:
                    course_dropdown.select_by_visible_text(course)
                except StaleElementReferenceException:
                    course_dropdown = get_course_dropdown(driver)
                    course_dropdown.select_by_visible_text(course)
                wait = WebDriverWait(driver, 60)
                submit_button = wait.until(EC.presence_of_element_located((By.ID, 'ContentPlaceHolder1_EvalsContentPlaceHolder_btnSubmit')))
                submit_button.click()

                wait.until(EC.presence_of_element_located((By.ID, 'ContentPlaceHolder1_EvalsContentPlaceHolder_pnlEntirePage')))
                try:
                    driver.find_element(By.ID, 'ContentPlaceHolder1_EvalsContentPlaceHolder_pnlSETs')
                except NoSuchElementException:
                    continue
                eval_df = scrape_data(driver, eval_df)
                print(f'Course Scraped: {course}')
        
        # Add space between number and percentage in Enrolled/Response Rate column 
        def add_space(value):
            return re.sub(r'(\d+)\((\d+\.\d+%)\)', r'\1 (\2)', str(value))
        eval_df['Enrolled/Response Rate'] = eval_df['Enrolled/Response Rate'].apply(add_space)
        
        # Export DataFrame as csv
        eval_df.to_csv('sets_data.csv', index=False)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit()

    finally:
        driver.quit()
        sys.exit()