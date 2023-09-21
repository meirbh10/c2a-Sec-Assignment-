import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from selenium.common.exceptions import *


windows = {}
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

wait = WebDriverWait(driver, 20)


def wait_for_window(timeout=2):
    time.sleep(timeout)
    wh_now = driver.window_handles
    wh_then = windows['window_handles']
    if len(wh_now) > len(wh_then):
        return set(wh_now).difference(set(wh_then)).pop()


url = 'https://www.demoblaze.com/'

credentials = {
  'username': 'automatedUser26@example.com',
  'password': '4r4nd0mp4ssw0rd'
}



print('\nS T A R T   T E S T: Open the website "https://www.demoblaze.com/", perform Login and Add the cheapest phone to cart')
print('Open the website: ', url)
time.sleep(5)
driver.get(url)
driver.maximize_window()
driver.implicitly_wait(5)
driver.set_script_timeout(5)




##### The Problem: Every time the system is refresh (F5), the order of the products in the table changes
##### The Solution: We can add an automatic precondition which delete (from the DB) all the cart items of the user and then we will be able to verify that the cheapest phone was added to the cart
"""
The current MANUAL solution\precondition in order to run this script: the cart of the user must be empty (in order to verify that the cheapest phone was added to the cart)
(OR: The cart should contains only items\products\phones which have the cheapest price)
"""



# CHECK 1: Open the website "https://www.demoblaze.com/", perform Login and Validate that we in Login status
try:
  wait.until(EC.element_to_be_clickable((By.ID, 'login2'))).click()  # Click on "Log In" button
  time.sleep(2)
  # wait.until(EC.element_to_be_clickable((By.ID, 'loginusername'))).click()  # Click on "Username" textox
  # ActionChains(driver).send_keys("A").perform()
  wait.until(EC.element_to_be_clickable((By.ID, 'loginusername'))).send_keys(credentials.get('username'))
  time.sleep(1)
  wait.until(EC.element_to_be_clickable((By.ID, 'loginpassword'))).send_keys(credentials.get('password'))
  time.sleep(1)
  driver.find_element(By.XPATH, '//button[@onclick="logIn()"]').click()
  time.sleep(2)
  wait.until(EC.element_to_be_clickable((By.ID, 'logout2')))
  PageTitle = driver.title
  print("PageTitle = ", PageTitle)
  if (PageTitle == "STORE"):
     print ("PASS 1: We entered successfully to the website\n")
  else:
     print ("FAIL 1: We could not access the 'website\n")
     # We can add here: 1. take and save a screenshot 2. write a comment and the exception to an Excel file (or some other report file\system)

except Exception as ExceptionError:
  print("FAIL 1: Can't Login to the website, the Error is:\n")
  print("ExceptionError: \n", ExceptionError)
  # We can add here: 1. take and save a screenshot 2. write a comment and the exception to an Excel file (or some other report file\system)
  
  




# CHECK 2: Add the cheapest phone to cart
# A. Select the "Phones" category
# B. Get all the list of the phones
# C. Check which is the cheapest
try:
  # driver.find_element(By.XPATH, '//button[@onclick="byCat("phone")"]').click()  # Click on the "Phones category"
  driver.find_elements(By.CLASS_NAME, 'list-group-item')[1].click()   # Click on the "Phones category"
  print("Phone category clicked")
  time.sleep(1)
  
  # Locate all elements with the specified class name
  elements = driver.find_elements(By.CLASS_NAME, 'col-lg-4.col-md-6.mb-4')
  i=0
  numerical_values = []
  for element in elements:
    i += 1
    h5_element = element.find_element(By.TAG_NAME, 'h5')
    PhonePrice = h5_element.text
    print("PhonePrice (as str)", i, " = ", PhonePrice)
    PhonePrice = PhonePrice[1:]
    PhonePrice = int(PhonePrice)
    print("PhonePrice (as int)", i, " = ", PhonePrice)
    numerical_values.append(PhonePrice)
  
  # Find the lowest price in the "numerical_values" list
  cheapestPhone = min(numerical_values)
  print("The cheapest phone price is: ", cheapestPhone)
  
  # Convert the cheapest phone to string and add "$"" to it
  cheapestPhoneString = str(cheapestPhone)
  cheapestPhoneString = "$" + cheapestPhoneString
  print("$cheapestPhoneString = ", cheapestPhoneString)


  # Click on the cheapest phone
  # Iterate through the elements and check if the <h5> element contains "cheapestPhoneString"
  for element in elements:
    h5_element = element.find_element(By.TAG_NAME, 'h5')
    if h5_element.text == cheapestPhoneString:
      element.click()
      time.sleep(2)
      break
  
  # Click on the "Add to cart" button
  driver.find_element(By.CLASS_NAME, 'btn.btn-success.btn-lg').click()
  # Verify that the cheapest Phone added to cart
  time.sleep(3)
  
  # Click on the alert "Product added."
  alert = driver.switch_to.alert
  alert.accept()
  time.sleep(2)
  
  window_handles = driver.window_handles
  driver.switch_to.window(window_handles[0])
  wait.until(EC.element_to_be_clickable((By.ID, 'cartur'))).click()  # Click on "Cart" button
  # driver.find_element(By.ID, 'cartur').click()
  time.sleep(3)

  # Check the "Price" of the LAST element\product of the table in the "Cart" screen (The added product is added to the bottom of the table)
  # CartTbleElement = driver.find_element(By.ID, 'tbodyid')
  CartTbleElement = wait.until(EC.element_to_be_clickable((By.ID, 'tbodyid')))
  tr_elements = CartTbleElement.find_elements(By.TAG_NAME, 'tr')
  lastCartelement = tr_elements[-1]
  LastProductPrice = lastCartelement.find_element(By.XPATH, './td[3]')
  LastProductPrice = LastProductPrice.text
  LastProductPrice = int(LastProductPrice)
  print("LastProductPrice = ", LastProductPrice)
  print("cheapestPhone = ", cheapestPhone)
  if LastProductPrice == cheapestPhone:
     print("PASS 2: The cheapest phone with the price of ", LastProductPrice, " added to cart successfully!")
  else:
     print("FAIL 2: The The cheapest phone DIDN'T added to cart")

except Exception as ExceptionError:
  print("FAIL 2: ExceptionError: \n", ExceptionError)
  # We can add here: 1. take and save a screenshot 2. write a comment and the exception to an Excel file (or some other report file\system)


# Close the browser
driver.quit()

print('E N D   T E S T')