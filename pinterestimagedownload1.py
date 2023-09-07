import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

current_dir = os.getcwd()
data_folder = os.path.join(current_dir, 'data')
file_path = os.path.join(data_folder, 'linkimage.txt')
driver_path = os.path.join(data_folder, 'chromedriver.exe')
save_folder = os.path.join(current_dir, 'images')

# Read the image URLs from the text file
with open(file_path, 'r') as file:
    image_urls = file.readlines()

# Set up Chrome webdriver options
chrome_options = Options()
# Specify the path to AdGuard Adblocker extension
extension_path = os.path.join(data_folder, 'adguard.crx')

# Add the extension using add_extension method
chrome_options.add_extension(''+extension_path+'')

# Set up the Chrome webdriver with the relative path to chromedriver.exe and headless mode
selenium_service = Service(driver_path)
driver = webdriver.Chrome(service=selenium_service, options=chrome_options)


# Create the save folder if it doesn't exist
os.makedirs(save_folder, exist_ok=True)
driver.get('https://pinterestdownloader.com/pinterest-image-downloader')

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
# Enter image URL and submit

input_box = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/input')
input_box.send_keys(image_urls)
time.sleep(2)
#klikdownload = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/button').click()
#time.sleep(3)

# Wait for the download button to appear
time.sleep(5)  # Adjust the wait time if needed
download_button = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/div[2]/div/div[2]/div/div[1]')
download_button.click()

# Wait for the download button to appear
time.sleep(3)  # Adjust the wait time if needed
download_button2 = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/div[2]/div/div[2]/div/div[2]/div[2]/a[2]')
download_button2.click()
time.sleep(3)

# Iterate through each image URL and download the image
for url in image_urls:
    url = url.strip()  # Remove leading/trailing whitespaces and newlines
    time.sleep(5)
    # Enter image URL and submit
    input_box = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/input')
    input_box.send_keys(url)
    klikdownload = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/form/button').click()
    time.sleep(3)
    
    # Wait for the download button to appear
    time.sleep(5)  # Adjust the wait time if needed
    download_button = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/div[2]/div/div[2]/div/div[1]')
    download_button.click()
    
    # Wait for the download button to appear
    time.sleep(3)  # Adjust the wait time if needed
    download_button2 = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/div[2]/div/div[2]/div/div[2]/div[2]/a[2]')
    download_button2.click()
    time.sleep(3)
    

    print(f"Downloaded: {url}")

print("All images downloaded successfully.")

# Close the browser
driver.quit()
