import csv
import os
import shutil
import time

import report_download

def process_report():
  with report_download.create_driver() as driver:
    report_download.gentran_login(driver)
    downloaded_file_path = report_download.download_report(driver)
  
  archived_file_path = move_report(downloaded_file_path)
  po_numbers = get_pos_from_report(archived_file_path)
  rename_processed_report(archived_file_path)

  check_for_missing_pos(po_numbers)

def move_report(downloaded_file_path):
  if not os.path.exists(downloaded_file_path):
    raise FileNotFoundError(f"File not found: {downloaded_file_path}")
  
  archive_directory = os.getenv("ARCHIVE_DIRECTORY")
  archive_filename = os.getenv("ARCHIVE_FILENAME").replace("{0}", time.strftime("%m.%d.%y"))

  archive_file_path = os.path.join(archive_directory, archive_filename)
  if not os.path.exists(archive_directory):
    os.makedirs(archive_directory)
  
  if (os.path.exists(archive_file_path)):
    os.remove(archive_file_path)

  shutil.move(downloaded_file_path, archive_file_path)
  if not os.path.exists(archive_file_path):
    raise FileNotFoundError(f"File not found: {archive_file_path}")
  else:
    print(f"File moved to: {archive_file_path}")
  
  return archive_file_path

def get_pos_from_report(file_path):
  po_numbers = []
  with open(file_path, mode="r") as file:
    csv_reader = csv.reader(file)

    for row in csv_reader:
      po_number = row[4].replace(" (PO No.)", "")
      if po_number == "Document Number":
        continue
      
      po_numbers.append(po_number)
  
  return po_numbers

def rename_processed_report(file_path):
  new_file_path = file_path.replace(".csv", "X.csv")
  if os.path.exists(new_file_path):
    os.remove(new_file_path)
  
  os.rename(file_path, new_file_path)

def check_for_missing_pos(po_numbers):
  from data_access import create_oracle_connection, get_missing_pos
  from email_module import email_missing_pos

  with create_oracle_connection() as conn:
    if conn is not None:
        missing_pos = get_missing_pos(conn, po_numbers)
        if missing_pos:
          email_missing_pos(missing_pos)
    else:
      raise ConnectionError("Failed to connect to Oracle database.")