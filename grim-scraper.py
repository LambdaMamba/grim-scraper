from bs4 import BeautifulSoup
from selenium import webdriver
from seleniumwire import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
import requests
from urllib.parse import urlparse
import os
from pathlib import Path
from tldextract import extract
import validators
import sys
from validator_collection import validators, checkers

try:
    link = input("Enter the URL: ")
    if checkers.is_url(link) == True:
        print("Valid URL, continuing...")
    elif checkers.is_url(link) == False:
        print("Invalid URL, exiting...")
        sys.exit()

    tsd, td, tsu = extract(link)
    url_domain = td + '.' + tsu
    options = webdriver.ChromeOptions()
    options.headless = False

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    urls = []

    driver.get(link)
    time.sleep(5)

    screenshot_loc = url_domain+"/screenshot.png"
    Path(url_domain).mkdir(parents=True, exist_ok=True)

    print("Saving screenshot of " +link+" in " + screenshot_loc)

    driver.save_screenshot(screenshot_loc)

    print("URL HTTP-Status-Code Content-Type")

    for request in driver.requests:
        if request.response:
            print(
                request.url,
                request.response.status_code,
                request.response.headers['Content-Type']
            )
            urls.append(request.url)
except Exception as e:
    print("Error... exiting")
    sys.exit()


print("Saving the resources.....")
i = 0
try:
    for url in urls:
        driver.get(url)
        time.sleep(1)
        src = driver.page_source
        file_path = urlparse(url).path
        file_name = os.path.basename(file_path)
        only_path = file_path.replace(file_name, '')
        tsd, td, tsu = extract(url)
        domain = td + '.' + tsu
        domain_path = domain + only_path

        if file_name == "":
            file_name = str(i)
            i = i+1

        scrape_dir = url_domain +"/"+ domain_path
        full_path = scrape_dir + file_name

        Path(scrape_dir).mkdir(parents=True, exist_ok=True)
        f = open(full_path, "w")
        f.write(src)
        f.close()
        print("Saved " + url + " in " + full_path)

    print("Saved the resources successfully")
except Exception as e:
    print("Error saving the resources... exiting")
    sys.exit()

driver.close()
