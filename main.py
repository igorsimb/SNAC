import os
import urllib
import uuid
from collections import namedtuple

import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

from time import sleep

from selenium.common import NoSuchElementException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from dotenv import load_dotenv

load_dotenv()


# https://pybit.es/articles/python-tips-carbon-selenium/

# counter = 1

def type_text(element, text):
    for letter in text:
        element.send_keys(letter)
        sleep(0.05)


def rename_file(path: str, file: str, new_name: str) -> str:
    """
    Takes relative or absolute path, file name and gives it a new name.
    """

    ext = ".png"
    try:
        os.rename(path+"/"+file+ext, path+"/"+new_name+ext)
    except FileExistsError:
        new_name += f"_{uuid.uuid4()}"
        os.replace(path + "\\" + file + ext, path + "\\" + new_name + ext)
        print(f"File with this name already exists! New file name: '{new_name}{ext}'. It is advised to rename it.")
    return os.getenv("BASE_DIR")+"carbon_images\\"+new_name+ext

chrome_options = Options()
# Installing extensions
chrome_options.add_extension('chrome-extensions/CensorTracker.crx')
chrome_options.add_extension('chrome-extensions/DesktopForInstagram.crx')

# setting up files download directory
prefs = {"download.default_directory": os.getenv("BASE_DIR")+"carbon_images"}
chrome_options.add_experimental_option("prefs", prefs)

# https://selenium-python.readthedocs.io/waits.html
browser = webdriver.Chrome(options=chrome_options)
browser.maximize_window()
wait = WebDriverWait(browser, 2)
sleep(2)

# locator
# tab_one = current tab minus 2
tab_one = browser.window_handles[2]
browser.switch_to.window(tab_one)

with open('cool_tip.py', 'r') as file:
    code = file.read()
header = urllib.parse.quote_plus('This is cool')
code = urllib.parse.quote_plus(code)

# link contains header and code for carbon.now.sh
CARBON = f'https://carbon.now.sh/?bg=rgba%28171%2C+184%2C+195%2C+1%29&t=blackboard&wt=boxy&l=python&width=500&ds=true' \
         f'&dsyoff=20px&dsblur=68px&wc=true&wa=false&pv=56px&ph=56px&ln=false&fl=1&fm=Hack&fs' \
         f'=14px&lh=133%25&si=false&es=2x&wm=false&code={code}&tb={header}'

browser.get(CARBON)
# sleep(3)

# carbon export png locator
export_button = browser.find_element(By.XPATH, '//button[@data-cy="quick-export-button"]')

export_button.click()
sleep(2)

downloaded_file = rename_file("carbon_images", "carbon", "cool_new_name")

sleep(2)

# Instagram or use instabot: https://instagrambot.github.io/docs/en/For_developers.html
browser.get("https://www.instagram.com/")
sleep(2)
allow_cookies = browser.find_element(By.XPATH, "//button[contains(text(), 'Allow essential and optional cookies')]")
allow_cookies.click()
sleep(2)

instagram_username_field = browser.find_element(By.XPATH, "//input[@aria-label='Phone number, username, or email']")
instagram_password_field = browser.find_element(By.XPATH, "//input[@aria-label='Password']")
instagram_login_button = browser.find_element(By.XPATH, "//button[@type='submit']/div[.='Log In']")

instagram_username_field.send_keys(os.getenv("INSTAGRAM_USERNAME"))
instagram_password_field.send_keys(os.getenv("INSTAGRAM_PASSWORD"))
sleep(2)
instagram_login_button.submit()

sleep(7)
# Create new Post
instagram_new_post_button = browser.find_element(By.XPATH, "//div[@class='QBdPU ']/*[name()='svg'][@aria-label='New "
                                                           "Post']")
instagram_new_post_button.click()
sleep(2)
instagram_upload_button = browser.find_element(By.XPATH, "//button[contains(text(), 'Select from computer')]")
instagram_upload_button.click()
sleep(1)
print(f"{downloaded_file=}")
pyautogui.write(downloaded_file)
sleep(1)
pyautogui.press('enter')
sleep(1)

aspect_ratio_button = browser.find_element(By.XPATH, "/html/body/div[6]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div/div[2]/div/button/div/*[name()='svg'][@aria-label='Select Crop']")
aspect_ratio_button.click()

sleep(1)
sixteen_by_nine = browser.find_element(By.XPATH, "/html/body/div[6]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div/div[1]/div/button[4]/div/div[2]/*[name()='svg'][@aria-label='Crop Landscape Icon']")

sixteen_by_nine.click()
sleep(1)
next_button = browser.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
next_button.click()
sleep(2)
next_button = browser.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
next_button.click()
sleep(2)

post_text_field = browser.find_element(By.XPATH, "//textarea[@aria-label='Write a caption...']")
type_text(post_text_field, "Well shit. Looks like it's working")

sleep(10)
browser.quit()
