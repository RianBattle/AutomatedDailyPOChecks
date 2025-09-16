from dotenv import load_dotenv

import data_access
import email_module
import report_processing

if __name__ == "__main__":
  load_dotenv()
  
  try:
    po_numbers = report_processing.process_report()
    with data_access.create_oracle_connection() as conn:
      if conn is not None:
          missing_pos = data_access.get_missing_pos(conn, po_numbers)
          if missing_pos:
            email_module.email_missing_pos(missing_pos)
  except Exception as e:
    email_module.email_error(e)