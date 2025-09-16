import os
import smtplib
from email.message import EmailMessage

def email_missing_pos(missing_pos):
  sender = os.getenv("SENDER_EMAIL")
  recipient = os.getenv("RECIPIENT_EMAIL")
  subject = os.getenv("EMAIL_SUBJECT")
  body = "The following PO Numbers are missing in the database:\n\n" + "\n".join(missing_pos)
  
  smtp_server = os.getenv("SMTP_SERVER")
  smtp_port = int(os.getenv("SMTP_PORT", 25))

  try:
    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
      server.send_message(message)
  except smtplib.SMTPException as e:
    print(f"SMTP error: {e}")
  except Exception as e:
    print(f"Error sending email: {e}")

def email_error(error_message):
  sender = os.getenv("SENDER_EMAIL")
  recipient = os.getenv("RECIPIENT_EMAIL")
  subject = "Error in Daily PO Checks"
  body = f"An error occurred during the Daily PO Checks process:\n\n{error_message}"

  smtp_server = os.getenv("SMTP_SERVER")
  smtp_port = int(os.getenv("SMTP_PORT", 25))

  try:
    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
      server.send_message(message)
  except smtplib.SMTPException as e:
    print(f"SMTP error: {e}")
  except Exception as e:
    print(f"Error sending email: {e}")