from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import getpass
import datetime
import time
import sys
delay = 10 # seconds

# Input credentials
print('MyTutor credentials:')
MT_email = input('What is your MyTutor email?')
MT_password = getpass.getpass('What is your MyTutor password? (your password will not be shown when typing)')
pages = input('How many pages of invoices do you want to scan?')

SQL_password = getpass.getpass('What is your SQL password? (your password will not be shown when typing)')
SQL_db = input('What is your SQL database name?')

PATH = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(PATH)

# SQL credentials
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=SQL_password,
  database = SQL_db
)

# Create SQL table 'invoices'
mycursor = mydb.cursor()
mycursor.execute("DROP TABLE IF EXISTS invoices")
mycursor.execute("CREATE TABLE invoices (id INT PRIMARY KEY, date DATETIME, student_name VARCHAR(20), payment DECIMAL(4,2), charge DECIMAL(4,2), vat DECIMAL(4,2), inv_date DATE)")
sql = "INSERT INTO invoices (id, date, student_name, payment, charge, vat, inv_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"

# MyTutor credentials
email = MT_email
password = MT_password
url = 'https://www.mytutor.co.uk/tutors/secure/invoices.html'

# Launch browser
driver.get(url)

# Enter email
email_field = driver.find_element_by_id('form:email:input')
email_field.send_keys(email)
email_field.send_keys(Keys.RETURN)

# Wait for loading and enter password
password_field = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'form:password:input')))
password_field.send_keys(password)
password_field.send_keys(Keys.RETURN)

# Wait for loading and filter dates
date_filter = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'summaryForm:currentDateFilter:input_label')))
date_filter.click()

# Wait for loading and change date range
ranges = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'summaryForm:currentDateFilter:input_6')))
ranges.click()

# Iterate through pages
page_num = 1
time.sleep(0.2)

while True:
    # Wait for loading and find invoice rows
    inv_table = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'tutorInvoicesForm:paidTutorialsTable_data')))
    inv_rows = inv_table.find_elements_by_tag_name('tr')

    # Iterate through rows
    for row in inv_rows:
        # Form data into array
        data_array = []
        temp_data_array = row.find_elements_by_tag_name('td')
        for data in temp_data_array:
            data_array.append(data.text)

        # FORMATTING
        # Data is in form ['lesson' lesson_id, lesson_date lesson_time, forename surname, price, charge, vat, inv_date]

        # Delete 'lesson' from first element
        data_array[0] = data_array[0].replace('Lesson ','')

        # Change datetime format from DD/MM/YYYY HH:MM to YYYY-MM-DD HH:MM:SS
        data_array[1] = datetime.datetime.strptime(data_array[1], '%d/%m/%Y %H:%M').strftime('%Y-%m-%d %H:%M') + ':00'

        # Format prices by removing £
        for i in range(3,6):
            data_array[i] = data_array[i].replace('£','')

        # Change inv_date format
        data_array[6] = datetime.datetime.strptime(data_array[6], '%d/%m/%Y').strftime('%Y-%m-%d')

        # Insert data into TABLE
        mycursor.execute(sql, data_array)
        mydb.commit()

        print(data_array)

    # Check if page in range (TODO: automatic check)
    if(page_num < int(pages)):
        next_button = driver.find_element_by_xpath('//div[@id="tutorInvoicesForm:paidTutorialsTable_paginator_bottom"]/a[4]')
        next_button.click()
        time.sleep(0.1) # seconds

        page_num += 1

    else:
        print('Iteration ended on page ' + str(page_num))
        driver.quit()
        sys.exit()
