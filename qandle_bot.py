import sys
import time
import yagmail
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

URL = os.getenv("QANDLE_URL")
EMAIL = os.getenv("QANDLE_EMAIL")
PASSWORD = os.getenv("QANDLE_PASSWORD")

def send_email(status):
    yag = yagmail.SMTP(
        os.getenv("EMAIL_SENDER"),
        os.getenv("EMAIL_APP_PASSWORD")
    )
    yag.send(
        to=os.getenv("EMAIL_RECEIVER"),
        subject=f"Qandle {status} Success",
        contents=f"Attendance {status} completed successfully."
    )

def open_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless=new")  # keep browser hidden

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    return driver

def login(driver):
    driver.get(URL)
    time.sleep(3)

    # Update selectors based on actual Qandle page
    driver.find_element(By.NAME, "email").send_keys(EMAIL)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[contains(text(),'Sign In')]").click()
    time.sleep(5)

def clock_in(driver):
    driver.find_element(
        By.XPATH,
        "//button[.//span[text()='Clock In']]"
    ).click()
    time.sleep(3)

def clock_out(driver):
    wait = WebDriverWait(driver, 30)

    # Click Clock Out button
    clockout_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Clock Out']]"))
    )
    clockout_btn.click()
    print("Clicked Clock Out")

    # Wait for popup modal to appear
    modal = wait.until(
        EC.visibility_of_element_located((By.ID, "summary"))
    )
    print("Summary modal appeared")

    # Now find YES button INSIDE the modal
    yes_btn = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//div[@id='summary']//button[.//span[text()='Yes']]"
        ))
    )
    yes_btn.click()
    print("Confirmed Clock Out")

    time.sleep(5)
  
def main():
    action = sys.argv[1]  # clockin or clockout
    driver = open_browser()

    try:
        login(driver)

        if action == "clockin":
            clock_in(driver)
            print(f"clocked in successfully")
            # send_email("Clock In")

        elif action == "clockout":
            clock_out(driver)
            print(f"clocked out successfully")
            # send_email("Clock Out")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()