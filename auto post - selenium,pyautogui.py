from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import pyautogui
import datetime

# Set up the webdriver for Instagram
instagram_url = 'https://www.instagram.com/'
instagram_driver = webdriver.Chrome()
instagram_driver.maximize_window()
instagram_driver.get(instagram_url)


def login_to_instagram(username, password):
    try:
        username_input = WebDriverWait(instagram_driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
        username_input.send_keys(username)

        password_input = instagram_driver.find_element(By.NAME, 'password')
        password_input.send_keys(password)

        login_button = instagram_driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()

        WebDriverWait(instagram_driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='New post']")))
        print("Logged in successfully!")
        return True
    except Exception as e:
        print(f"Login failed: {e}")
        return False    

def create_post(image_path, caption):

    new_post_button = instagram_driver.find_element(By.XPATH, "//*[@aria-label='New post']")
    new_post_button.click()

    WebDriverWait(instagram_driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Select from computer']")))
    select_from_computer_button = instagram_driver.find_element(By.XPATH, "//button[text()='Select from computer']")
    select_from_computer_button.click()

    time.sleep(2)
    pyautogui.typewrite(image_path)
    time.sleep(1)  # Adjust the delay if needed for the image upload to complete
    pyautogui.press('enter')
    time.sleep(2)

    pyautogui.press(['tab','tab','enter'])
    time.sleep(2)

    pyautogui.press(['tab','tab','enter'])
    time.sleep(2)


    pyautogui.press(['tab','tab','tab','tab','tab'])
    time.sleep(2)
    pyautogui.typewrite(caption)
    time.sleep(2)

    pyautogui.hotkey('shift','tab')
    pyautogui.hotkey('shift','tab')
    pyautogui.hotkey('shift','tab')
    pyautogui.press('enter')
    time.sleep(10)

    pyautogui.press(['tab','enter'])
    time.sleep(1)
    pyautogui.press(['tab','enter'])

    print(f"Posted: {caption}")

# Login to Instagram
username = 'MrBeanX12'      

password = 'MrBeanX123'

file_path = r"C:\Users\Administrator\Documents\Python\Top_Posts.csv"
df = pd.read_csv(file_path)

if login_to_instagram(username, password):

    start_time = datetime.datetime.now()

    for index, row in df.iterrows():
        caption = row['Title']      
        
        image_name = row['ID']
        image_path = rf"C:\Users\Administrator\Documents\Python\images\{image_name}.png"

        try:
            create_post(image_path, caption)
        except Exception as e:
            print(f"Error posting {caption}: {e}")

        # Calculate time difference for next post
        time_elapsed = (datetime.datetime.now() - start_time).seconds
        time_to_wait = max(120 - time_elapsed, 0)  # Ensure minimum wait is 0 seconds
        
        time.sleep(time_to_wait)  # Wait for calculated time before next post
        start_time = datetime.datetime.now() 

    # Close the browser after posting
    instagram_driver.quit()
else:
    print("Login failed. Exiting...")
