import os
import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    st.title("Pinterest Image Downloader")

    # File paths
    current_dir = os.getcwd()
    data_folder = os.path.join(current_dir, 'data')
    file_path = os.path.join(data_folder, 'linkimage.txt')
    driver_path = os.path.join(data_folder, 'chromedriver.exe')
    save_folder = os.path.join(current_dir, 'images')

    # Set up Chrome webdriver options
    chrome_options = Options()
    # Specify the path to AdGuard Adblocker extension
    extension_path = os.path.join(data_folder, 'adguard.crx')

    # Add the extension using add_extension method
    chrome_options.add_extension(extension_path)

    # Set up the Chrome webdriver with the relative path to chromedriver.exe and headless mode
    selenium_service = Service(driver_path)
    driver = webdriver.Chrome(service=selenium_service, options=chrome_options)

    # Create the save folder if it doesn't exist
    os.makedirs(save_folder, exist_ok=True)
    driver.get('https://pinterestdownloader.com/id')

    time.sleep(5)

    # Get the handle of the currently active tab
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)
    current_handle = driver.current_window_handle
    # Close all tabs except the active one
    for handle in driver.window_handles:
        if handle != current_handle:
            driver.switch_to.window(handle)
            driver.close()

    # Switch back to the active tab
    driver.switch_to.window(current_handle)

    # Create an ActionChains object
    action_chains = ActionChains(driver)

    # Iterate through each image URL and download the image
    with open(file_path, 'r') as file:
        image_urls = file.readlines()
        for url in image_urls:
            url = url.strip()  # Remove leading/trailing whitespaces and newlines

            try:
                # Enter image URL and submit
                input_box = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/input')
                input_box.clear()  # Clear the input box
                input_box.send_keys(url)
                time.sleep(2)
                klikdownload = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/button').click()
                time.sleep(3)

                # Wait for the download button to appear
                wait = WebDriverWait(driver, 10)
                download_button = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[1]/div[2]/a[2]')))
                download_button.click()

                st.write(f"Downloaded: {url}")

            except Exception as e:
                st.write(f"Error downloading {url}: {str(e)}")
                # Reload the page and continue to the next loop
                driver.refresh()
                continue

    st.write("All images downloaded successfully.")

    # Close the browser
    driver.quit()

if __name__ == '__main__':
    main()
