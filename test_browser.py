import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("http://127.0.0.1:5500/campaign-trail/index.html")
    time.sleep(2)

    # Click begin
    btn = driver.find_element(By.ID, "game_start")
    btn.click()
    time.sleep(1)

    # Select 2020 (value 21)
    select = driver.find_element(By.ID, "election_id")
    select.send_keys("2020")
    time.sleep(1)

    # Select candidate
    btn = driver.find_element(By.ID, "election_id_button")
    btn.click()
    time.sleep(1)

    # Select Biden (value 300)
    select = driver.find_element(By.ID, "candidate_id")
    select.send_keys("Joe Biden")
    time.sleep(1)

    btn = driver.find_element(By.ID, "candidate_id_button")
    btn.click()
    time.sleep(1)

    # Select running mate
    btn = driver.find_element(By.ID, "running_mate_id_button")
    btn.click()
    time.sleep(2)

    # Get console logs
    for entry in driver.get_log('browser'):
        print(entry)
        
    driver.quit()
except Exception as e:
    print(f"Selenium Error: {e}")
