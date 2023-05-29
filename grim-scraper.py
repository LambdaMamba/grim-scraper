from bs4 import BeautifulSoup
from selenium import webdriver
from seleniumwire import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
import requests
from urllib.parse import urlparse
import os

link = input("Enter the URL: ")

options = webdriver.ChromeOptions()
options.headless = False

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
urls = []

driver.get(link)
time.sleep(5)

print("Saving screenshot of " +link+" as screenshot.png")

driver.save_screenshot("screenshot.png")

print("URL HTTP-Status-Code Content-Type")

for request in driver.requests:
    if request.response:
        print(
            request.url,
            request.response.status_code,
            request.response.headers['Content-Type']
        )
        urls.append(request.url)


i = 0

print("Saving the resources.....")

for url in urls:
    driver.get(url)
    time.sleep(1)
    src = driver.page_source
    file_path = urlparse(url).path
    file_name = os.path.basename(file_path)
    try:
        f = open(file_name, "w")
        f.write(src)
        f.close()
        print("Saved " + url + " in " + file_name)
    except FileNotFoundError as e:
        f = open(str(i), "w")
        f.write(src)
        f.close()
        print("Saved " + url + " in " + str(i))
        i = i+1
        
driver.close()
