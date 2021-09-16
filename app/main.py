import json
import time
import sys
import os
import socket
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from pymongo import MongoClient

client = MongoClient(os.environ.get("MONGO_URI", "mongodb://root:example@mongo:27017/"))

db = client.malt

def run_thread(arg):
    options = Options()
    ua = UserAgent(verify_ssl=False)
    userAgent = ua.chrome
    options.add_argument(f'user-agent={userAgent}')
    options.add_argument("--disable-extensions")
    options.add_argument('--no-sandbox')
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
                Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
                })
            """
    })
    driver.maximize_window()
    url = "https://www.malt.fr/s?q=" + arg
    driver.get(url)
    with open('cookies.json', 'r', newline='') as inputdata:
        cookies = json.load(inputdata)
    for cookie in cookies:
        cookie.pop('sameSite')
        driver.add_cookie(cookie)
    time.sleep(5)
    driver.get(url)
    scrap(driver, arg)


def scrap(driver, techno):
    time.sleep(6)
    elements = driver.find_elements_by_class_name(
        "profile-card.freelance-linkable")
    for element in elements:
        time.sleep(1)
        data = element.get_attribute("outerHTML")
        name = element.find_element_by_class_name(
            "profile-card-header__full-name").text
        data_named = {"name": name.replace(
            " ", "_") + "_" + techno, "content": json.dumps(data)}
        collection = db[techno]
        collection.insert_one(data_named)
        #send data_named to somethig but i have no idea of what
    next_page = driver.find_element_by_class_name("c-pagination__next")
    time.sleep(5)
    ActionChains(driver).move_to_element(
        next_page).click(next_page).perform()
    scrap(driver, techno)


for arg in sys.argv:
    if(arg != "main.py"):
        try:
            thread = Thread(target=run_thread, args=(arg,))
            thread.start()
        except:
            print("Error: unable to start thread")
