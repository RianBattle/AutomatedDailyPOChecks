from dotenv import load_dotenv
import sys
import os
services_dir = os.path.abspath("./services")
sys.path.insert(0, services_dir)

import email_module
import report_processing

if __name__ == "__main__":
  load_dotenv()
  
  try:
    po_numbers = report_processing.process_report()
  except Exception as e:
    email_module.email_error(e)