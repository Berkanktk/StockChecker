import logging
import os
import smtplib
import ssl
import sys
from email.message import EmailMessage
from time import sleep
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from discord_webhook import DiscordWebhook

""""
    Author: @Berkanktk
"""

# *************************************************************
# TODO: Add credentials inside the .env file
""""
    Remember to make a copy of the .env.example file.
    Then rename the copy from '.env.example' to '.env',
    and begin filling out the needed values/credentials.
"""

# TODO: Insert product information below
link = ''
name = ''

# TODO: How often should a lookup be performed?
check_timer = 3  # seconds

# TODO: What to look after
error_msg = 'Not in stock'
success_msg = 'Add to basket'

# TODO: Email validation to see if the script is still running (Optional)
validation = True
validation_timer = 24  # 24 = Every 12 Hours if check_timer is 1800.

# TODO: Add CC recipients (Optional)
CC = ''  # Multiple recipients are seperated with a comma

# TODO: Discord announcement wanted
discord_announcement = False

# *************************************************************
# Initial lists/values
attempt = 1
script_test = 0

# Load .env file
load_dotenv()

# Disable WDM logs
logging.getLogger('WDM').setLevel(logging.NOTSET)
os.environ['WDM_LOG'] = "false"

# Add contents from the .env file
DISCORD_WEBHOOK = os.getenv('DISCORD_WEBHOOK')
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
SMTP_SERVER = os.getenv('SMTP_SERVER')
PORT = os.getenv('PORT')

# SMTP configurations
port = PORT
smtp_server = SMTP_SERVER
sender = EMAIL_ADDRESS
recipient = EMAIL_ADDRESS
sender_password = EMAIL_PASSWORD

# Chrome Driver options
chrome_options = Options()
chrome_options.add_argument("--headless")

# Setting up the chromedriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  # Without GUI


def mail_sender_CC(subject, from_mail, to_mail, cc, content):
    # Creating Email
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_mail
    msg['To'] = to_mail
    msg['cc'] = cc
    msg.set_content(content)

    # Sending Email
    send(smtp_server, PORT, EMAIL_ADDRESS, EMAIL_PASSWORD, msg)


def mail_sender(subject, from_mail, to_mail, content):
    # Creating Email
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_mail
    msg['To'] = to_mail
    msg.set_content(content)

    # Sending Email
    send(smtp_server, PORT, EMAIL_ADDRESS, EMAIL_PASSWORD, msg)


def send(server, port, sender_mail, sender_password, msg):
    SSL_context = ssl.create_default_context()

    with smtplib.SMTP(server, int(port)) as server:
        server.starttls(context=SSL_context)
        server.login(sender_mail, sender_password)
        server.send_message(msg)
        server.quit()


def validationWanted(user_choice):
    if user_choice:
        return True
    elif not user_choice:
        return False


def discordAlert(user_choice, msg):
    if user_choice:
        webhook = DiscordWebhook(
            url=DISCORD_WEBHOOK,
            content=msg)
        webhook.execute()
    else:
        print("Skipping Discord Announcement")


flag = True
while flag:

    # Launch URL
    driver.get(link)

    # Get contents
    element = driver.find_element(By.TAG_NAME, 'body')
    element_text = element.text

    if element_text.find(success_msg) != -1:
        # Performing check
        subject = 'Product in stock!'
        content = name + " is now in stock!"
        print(content)

        # Sending Discord Announcement
        discordAlert(discord_announcement, content)

        # Creating and sending mail
        mail_sender_CC(subject, EMAIL_ADDRESS, EMAIL_ADDRESS, CC, content)

        # Ending script
        flag = False
        driver.close()
        sys.exit()
    elif element_text.find(error_msg):
        print(name, "is still not in stock... Attempt: #", attempt)

        # Incrementing alert variables
        attempt += 1
        script_test += 1

        # Validator
        if script_test >= validation_timer and validationWanted(validation):
            subject = 'StockChecker Validation Test'
            content = 'Script is still running.'

            # Creating and sending test mail
            mail_sender(subject, EMAIL_ADDRESS, EMAIL_ADDRESS, content)

            script_test = 0

        # Initiating restart
        sleep(check_timer)
        driver.refresh()
    else:
        print("Something went wrong.")
        subject = 'StockChecker Alert'
        content = 'Something went wrong, and the script is therefore no longer running.'

        # Creating and sending test mail
        mail_sender(subject, EMAIL_ADDRESS, EMAIL_ADDRESS, content)

        # Ending script
        flag = False
        driver.close()
        sys.exit()
