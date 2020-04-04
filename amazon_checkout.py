import os
import random
from twilio.rest import Client
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

###############################
# User specific info goes here 
###############################

AMAZON_EMAIL_ID = os.environ['AMAZON_EMAIL_ID']
AMAZON_PASSWORD = os.environ['AMAZON_PASSWORD']
FROM_NUMBER='+1XXXXXXXXXX'  ##Number generated through your Twilio account 
TO_NUMBER='+1XXXXXXXXXX'
# Download chrome webdriver as per your Chrome version from here: https://chromedriver.chromium.org/downloads
# Also, set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN as system environment variables as per your Twilio credentials
###############################

DEFAULT_ERROR="program ended abruptly. please check"

def sendMessage(slot_available=False, message="Test message"):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message_client = client.messages.create(
                              body=message,
                              from_=FROM_NUMBER,
                              to=TO_NUMBER
                          )

    if slot_available==True and message != DEFAULT_ERROR:
        call_client = client.calls.create(
                            twiml='<Response><Say>You'+ message +'</Say></Response>',
                            from_=FROM_NUMBER,
                            to=TO_NUMBER
                        )

def check_availability(all_availabilities):
    try:
        available_bool=False
        if len(all_availabilities) > 0:
            sendMessage(slot_available=True,message="Slot POSSIBLY available")
        else:
            for availability in all_availabilities:
                availability_innerHTML=availability.get_attribute('innerHTML').strip().lower()
                print(availability_innerHTML)
                if availability_innerHTML != "not available":
                    available_bool=True
                    sendMessage(slot_available=True,message="Slot available!!!")
                    break;

            if available_bool==False:
                print("Slot DEFINITELY NOT available")
    except:
        sendMessage(slot_available=True,message="Exception reading slots. Slot POSSIBLY available")

    
def main():
    browser=webdriver.Chrome()
    browser.fullscreen_window()
    browser.get("https://www.amazon.com/alm/storefront?almBrandId=QW1hem9uIEZyZXNo")
    sleep(2)
    account_login_label=browser.find_element_by_id('nav-link-accountList')
    account_login_label.click()
    login_email=browser.find_element_by_id('ap_email')
    login_email.send_keys(AMAZON_EMAIL_ID)
    sleep(5)
    browser.find_element_by_id('continue').click()
    browser.find_element_by_id('ap_password').send_keys(AMAZON_PASSWORD)
    sleep(6)
    browser.find_element_by_id('signInSubmit').click()
    sleep(1)
    #browser.find_element_by_css_selector("input[type='radio'][value='sms']").click()
    sleep(2)
    browser.find_element_by_id('continue').click()

    #waits for a minute for you to enter the OTP
    WebDriverWait(browser, 60).until(lambda browser: len(browser.find_element_by_name('code').get_attribute('value')) == 6)
    sleep(5)
    browser.find_element_by_css_selector("input[class='a-button-input']").submit()
    sleep(8)
    try:
        browser.find_element_by_name('proceedToFreshCheckout').submit()
    except:
        print("First access method failed. Amazon is being smart. Trying another way")
        browser.find_element_by_id('nav-cart').click()
        sleep(2)
        browser.find_element_by_css_selector("input[class='a-button-input'][value='Proceed to checkout']").submit()
    sleep(2)
    browser.find_element_by_name('proceedToCheckout').click() 
    refresh_intervals=[154,128,86,132,93,121]
    while True:
        check_availability(browser.find_elements_by_xpath("//input[contains(@type, 'radio') and contains(@name, 'slotsRadioGroup') and not(@disabled)]"))
        refresh_interval=random.choice(refresh_intervals)
        print('Refreshing in {} secs...'.format(str(refresh_interval))) 
        sleep(refresh_interval)
        browser.refresh()
        sleep(5)


if __name__=="__main__":
    try:
        main()
    except:
        print("Something went wrong in the program. Please check")
        sendMessage(slot_available=True,message=DEFAULT_ERROR)
        raise