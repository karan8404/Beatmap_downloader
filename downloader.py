from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import pickle


def download_beatmapets(beatmapset_ids: dict, username, password):
    global to_download_mapsets
    # Setup webdriver
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.directory_upgrade": True,
    })
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=chrome_options)

    # Navigate to the main page
    driver.get("https://osu.ppy.sh/home")

    # Open the login popup
    login_button = driver.find_element(
        By.CSS_SELECTOR, ".landing-nav__link.js-nav-toggle.js-click-menu.js-user-login--menu")
    login_button.click()

    # Fill in the username and password
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Submit the form
    password_field.submit()
    time.sleep(5)

    # Navigate to the beatmap page and start downloading beatmaps
    for beatmapset in list(beatmapset_ids):
        url = f"https://osu.ppy.sh/beatmapsets/{beatmapset_ids[beatmapset]}"
        driver.get(url)

        # Wait for the download button to be present and click it
        wait = WebDriverWait(driver, 5)  # Wait up to 5 seconds
        download_button = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".btn-osu-big.btn-osu-big--beatmapset-header")))
        download_button.click()

        time.sleep(2)
        if ("too many requests" in driver.title):
            print("Too many requests, Completing all downloads and then exiting.")
            while any(filename.endswith((".crdownload", ".tmp")) for filename in os.listdir(download_dir)):
                time.sleep(1)
            print("\nLast downloaded beatmap: ", beatmapset-1)
            driver.quit()
            print("Rerun this script after a few hours.")
            pickle.dump(to_download_mapsets, open(filepath, 'wb'))
            exit()

        print(
            f"Beatmap {beatmapset_ids[beatmapset]} download initiated! {beatmapset}/{total}")
        to_download_mapsets.pop(beatmapset)

    # Wait for the downloads to complete
    while any(filename.endswith((".crdownload", ".tmp")) for filename in os.listdir(download_dir)):
        time.sleep(1)  # Check every second

    print("Beatmaps download completed!")


filepath = 'to_download_mapsets.pkl'
to_download_mapsets: dict = pickle.load(open(filepath, 'rb'))

curr, total = min(to_download_mapsets.keys()), max(to_download_mapsets.keys())

print("Starting download from beatmap number: ", curr)


# Directory to download beatmaps
# Note- Windoes users need to use double backslashes in the path
# Replace with your where you want to download the songs
download_dir = ""
# Sign in information for osu
username = ''  # Replace with your actual username
password = ''  # Replace with your actual password

download_beatmapets(to_download_mapsets, username, password)
