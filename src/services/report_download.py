import os
import time

import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def create_driver():
  return selenium.webdriver.Chrome()

def gentran_login(driver):
  driver.get(os.getenv("GENTRAN_LOGIN_URL"))
  assert "OpenText BizManager" in driver.title

  username_element = driver.find_element(By.NAME, "username")
  username_element.clear()
  username_element.send_keys(os.getenv("GENTRAN_LOGIN_USERNAME"))

  password_element = driver.find_element(By.NAME, "password")
  password_element.clear()
  password_element.send_keys(os.getenv("GENTRAN_LOGIN_PASSWORD"))
  password_element.send_keys(Keys.RETURN)

def download_report(driver):
  driver.get(os.getenv("GENTRAN_REPORT_DOWNLOAD_URL"))

  download_button = driver.find_element(By.NAME, "downloadButton")
  download_button.click()

  downloads_directory = os.getenv("DOWNLOADS_DIRECTORY").replace("{0}", os.getlogin())
  downloaded_filename = os.getenv("DOWNLOADED_FILENAME")
  downloaded_file_path = str(os.path.join(downloads_directory, downloaded_filename))
  if not os.path.exists(downloads_directory):
    os.makedirs(downloads_directory)

  retry_count = 0
  while retry_count < 5:
    try:
      if os.path.exists(downloaded_file_path):
        break

      time.sleep(5)
      retry_count += 1
    except Exception as e:
      retry_count += 1
  
  return downloaded_file_path