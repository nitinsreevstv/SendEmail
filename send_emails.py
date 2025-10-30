import smtplib
from email.message import EmailMessage
import csv
import time
from jinja2 import Environment, FileSystemLoader
from jinja2 import Template
from dotenv import load_dotenv
import os

load_dotenv() 


# Your email credentials
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Jinja2 environment
env = Environment(loader=FileSystemLoader('.'))  # Looks for template in current dir
template = env.get_template('template.html')


# Set up SMTP
smtp_server = "smtp.gmail.com"
smtp_port = 465

# Read recipients from CSV
with open("emails.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    recipients = list(reader)

# Connect to SMTP server
with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    for person in recipients:
        msg = EmailMessage()
        subject_template = Template("Application for QA Role at {{ company_name }}")
        msg['Subject'] = subject_template.render(company_name=person['company_name'])
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = person["email"]

        # Render the HTML content with Jinja2
        html_content = template.render(
            name=person['name'],
            company_name=person['company_name']
        )        
        msg.set_content(f"Hi {person['name']},\nThis is your plain text fallback.")
        msg.add_alternative(html_content, subtype='html')

        # Attach resume
        with open("Priyanshu QA.pdf", "rb") as f:
            file_data = f.read()
            file_name = "Priyanshu QA.pdf"
            msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

        smtp.send_message(msg)
        print(f"Sent HTML email to {person['email']}")

        time.sleep(2)  # Optional delay
