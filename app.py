import oracledb
import os
import shutil
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

load_dotenv()

GENTRAN_LOGIN_URL = os.getenv("GENTRAN_LOGIN_URL")
GENTRAN_LOGIN_USERNAME = os.getenv("GENTRAN_LOGIN_USERNAME")
GENTRAN_LOGIN_PASSWORD = os.getenv("GENTRAN_LOGIN_PASSWORD")
GENTRAN_REPORT_DOWNLOAD_URL = os.getenv("GENTRAN_REPORT_DOWNLOAD_URL")

DOWNLOADS_DIRECTORY = os.getenv("DOWNLOADS_DIRECTORY").replace("{0}", os.getlogin())
DOWNLOADED_FILENAME = os.getenv("DOWNLOADED_FILENAME")

ARCHIVE_DIRECTORY = os.getenv("ARCHIVE_DIRECTORY")
ARCHIVE_FILENAME = os.getenv("ARCHIVE_FILENAME").replace("{0}", time.strftime("%m.%d.%y"))

SQL = ""

def create_driver():
  return webdriver.Chrome()

def gentran_login(driver):
  driver.get(GENTRAN_LOGIN_URL)
  assert "OpenText BizManager" in driver.title

  username_element = driver.find_element(By.NAME, "username")
  username_element.clear()
  username_element.send_keys(GENTRAN_LOGIN_USERNAME)

  password_element = driver.find_element(By.NAME, "password")
  password_element.clear()
  password_element.send_keys(GENTRAN_LOGIN_PASSWORD)
  password_element.send_keys(Keys.RETURN)

def download_report(driver):
  driver.get(GENTRAN_REPORT_DOWNLOAD_URL)

  download_button = driver.find_element(By.NAME, "downloadButton")
  download_button.click()

  downloaded_file_path = os.path.join(DOWNLOADS_DIRECTORY, DOWNLOADED_FILENAME)
  if not os.path.exists(DOWNLOADS_DIRECTORY):
    os.makedirs(DOWNLOADS_DIRECTORY)

  retry_count = 0
  while retry_count < 5:
    try:
      if os.path.exists(downloaded_file_path):
        break

      time.sleep(5)
      retry_count += 1
    except Exception as e:
      print(f"Attempt {retry_count + 1} failed: {e}")
      retry_count += 1
  
  return downloaded_file_path

def move_report(downloaded_file_path):
  if not os.path.exists(downloaded_file_path):
    raise FileNotFoundError(f"File not found: {downloaded_file_path}")

  archive_file_path = os.path.join(ARCHIVE_DIRECTORY, ARCHIVE_FILENAME)
  if not os.path.exists(ARCHIVE_DIRECTORY):
    os.makedirs(ARCHIVE_DIRECTORY)

  shutil.move(downloaded_file_path, archive_file_path)
  if not os.path.exists(archive_file_path):
    raise FileNotFoundError(f"File not found: {archive_file_path}")
  else:
    print(f"File moved to: {archive_file_path}")

def process_report(file_path):
  pass

def load_sql():
  fs = open("./queries/check_po_exists.sql", "r")
  SQL = fs.read()
  fs.close()

def create_oracle_connection():
  try:
    oracledb.init_oracle_client(lib_dir=r"C:\app\client\rbattle\product\12.2.0\client_1")
    
    conn = oracledb.connect(user="tabula", password="har13y", dsn="PRI")
    
    return conn
  except oracledb.DatabaseError as e:
    print(f"Database connection error: {e}")
    return None

def check_oracle_for_po(conn, po_number):
  try:
    fs = open("./queries/check_po_exists.sql", "r")
    SQL = fs.read()
    fs.close()

    cursor = conn.cursor()
    cursor.execute(SQL, poNumber=po_number)
    
    rows = cursor.fetchall()
    cursor.close()

    return len(rows) > 0
  except oracledb.DatabaseError as e:
    print(f"Database query error: {e}")
    return False

if __name__ == "__main__":
  load_sql()

  oracle_conn = create_oracle_connection()
  print(check_oracle_for_po(oracle_conn, "BHb8T6ff0"))
  # driver = create_driver()

  # gentran_login(driver)
  # downloaded_file_path = download_report(driver)

  # driver.close()

  # move_report(downloaded_file_path)