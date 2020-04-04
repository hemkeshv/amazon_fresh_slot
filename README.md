# amazon_fresh_slot
COVID-19 Amazon Fresh Delivery Slot Detector: Notify user by text and call when new delivery window is released which was otherwise unavailable due to increased demand using Python, Selenium and Twilio. 

# Instructions:

How to run?
>> python amazon_checkout.py

## Prerequisites:

Install Python 3.x

pip install -U selenium
pip install twilio

Download chrome webdriver as per your Chrome version from here: https://chromedriver.chromium.org/downloads

Create Twilio account: https://bit.ly/3aIcEwB

Set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN as system environment variables as per your Twilio credentials

Read the top part of the code to set required parameters
Provide the path of the folder containing the chromedriver in the System PATH variable. 

## Notes:
1. During Automation, Amazon will ask you to enter OTP, after you enter the OTP (within 60 secs) DO NOT click on continue. The code will do it for you.
2. Add items to your cart beforehand so that upon notification you can quickly checkout items
