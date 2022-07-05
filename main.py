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
        os.rename(path + "/" + file + ext, path + "/" + new_name + ext)
    except FileExistsError:
        new_name += f"_{uuid.uuid4()}"
        os.replace(path + "\\" + file + ext, path + "\\" + new_name + ext)
        print(f"File with this name already exists! New file name: '{new_name}{ext}'. It is advised to rename it.")
    return os.getenv("BASE_DIR") + "carbon_images\\" + new_name + ext


chrome_options = Options()
# Installing extensions
chrome_options.add_extension('chrome-extensions/CensorTracker.crx')
chrome_options.add_extension('chrome-extensions/DesktopForInstagram.crx')

# setting up files download directory
prefs = {"download.default_directory": os.getenv("BASE_DIR") + "carbon_images"}
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
    code_lines = file.readlines()
header = urllib.parse.quote_plus('This is cool')
code = urllib.parse.quote_plus(code)

print(len(code_lines))

# link contains header and code for carbon.now.sh
CARBON = f'https://carbon.now.sh/?bg=rgba%28171%2C+184%2C+195%2C+1%29&t=blackboard&wt=boxy&l=python&width=500&ds=true' \
         f'&dsyoff=20px&dsblur=68px&wc=true&wa=false&pv=56px&ph=56px&ln=false&fl=1&fm=Hack&fs' \
         f'=14px&lh=133%25&si=false&es=2x&wm=false&code={code}&tb={header}'

vk_public_page = "https://vk.com/public213721986"

# CARBON
browser.get(CARBON)
# sleep(3)

# carbon export png locator
export_button = browser.find_element(By.XPATH, '//button[@data-cy="quick-export-button"]')

export_button.click()
sleep(2)

downloaded_file = rename_file("carbon_images", "carbon", "cool_new_name")

sleep(2)

# INSTAGRAM
# or use instabot: https://instagrambot.github.io/docs/en/For_developers.html

browser.get("https://www.instagram.com/")
sleep(2)
allow_cookies = browser.find_element(By.XPATH, "//button[contains(text(), 'Allow essential and optional cookies')]")
allow_cookies.click()
sleep(2)

instagram_username_field = browser.find_element(By.XPATH, "//input[@aria-label='Phone number, username, or email']")
instagram_password_field = browser.find_element(By.XPATH, "//input[@aria-label='Password']")
instagram_login_button = browser.find_element(By.XPATH, "//button[@type='submit']/div[.='Log In']")

sleep(1)
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

aspect_ratio_button = browser.find_element(By.XPATH,
                                           "/html/body/div[6]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div/div[2]/div/button/div/*[name()='svg'][@aria-label='Select Crop']")
aspect_ratio_button.click()

# TODO: if code is more than <= 9 <= 19 lines, use aspect ratio 1:1; if > 19, use 16:9
sleep(1)
sixteen_by_nine = browser.find_element(By.XPATH,
                                       "/html/body/div[6]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[1]/div/div[1]/div/button[4]/div/div[2]/*[name()='svg'][@aria-label='Crop Landscape Icon']")
sixteen_by_nine.click()
sleep(1)

original_aspect_ratio = browser.find_element(By.XPATH,
                                       '//*[name()="svg"][@aria-label="Photo Outline Icon"]')

# //*[name()='svg']//*[name()='circle']
# square.click()

original_aspect_ratio.click()
sleep(1)
next_button = browser.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
next_button.click()
sleep(2)
next_button = browser.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
next_button.click()
sleep(2)

post_text_field = browser.find_element(By.XPATH, "//textarea[@aria-label='Write a caption...']")
type_text(post_text_field, "This is how you print a for loop")
#
# sleep(2)
# instagram_share_button = browser.find_element(By.XPATH, "//button[contains(text(), 'Share')]")
# instagram_share_button.click()
#
# sleep(10)
#
# # VKONTAKTE
# browser.get(vk_public_page)
# sleep(3)
# vk_signin_button = instagram_share_button = browser.find_element(By.XPATH, "//button[contains(text(), 'Sign in')]")
# vk_signin_button.click()
# sleep(1)
#
# vk_login_field = browser.find_element(By.NAME, "login")
# vk_login_field.send_keys(os.getenv("VK_USERNAME"))
# sleep(1)
#
# # vk_continue_button = browser.find_element(By.XPATH, "//div[contains(text(), 'Continue')]")
# vk_continue_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
# vk_continue_button.click()
#
# sleep(2)
# vk_password_field = browser.find_element(By.NAME, "password")
# vk_password_field.send_keys(os.getenv("VK_PASSWORD"))
# sleep(1)
#
# vk_continue_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
# vk_continue_button.click()
# sleep(5)
#
# vk_post_field = browser.find_element(By.ID, "post_field")
# type_text(vk_post_field, "Все круто!")
#
# # vk_add_photo_button = browser.find_element(By.XPATH, '//*[@id="page_add_media"]/div/a/span/*[name="svg"][@fill="none"]')
# vk_add_photo_button = browser.find_element(By.CLASS_NAME, "ms_item_photo")
# vk_add_photo_button.click()
# sleep(2)
#
# print("Searching for upload photo button")
# vk_upload_photo = browser.find_element(By.ID, "photos_choose_upload_area_label15415913_-14")
# vk_upload_photo.click()
# sleep(2)
# pyautogui.write(downloaded_file)
# sleep(1)
# pyautogui.press('enter')
# sleep(2)
# vk_publish_button = browser.find_element(By.ID, "send_post")
# vk_publish_button.click()
#

print("ALL DONE!")
sleep(10)
browser.quit()
