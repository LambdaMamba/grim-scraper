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
import csv
import argparse


def extract_root_domain(url):
    tsd, td, tsu = extract(url)
    root_domain = td + '.' + tsu
    return root_domain


def initialize_driver(headless_mode):
    options = webdriver.ChromeOptions()
    options.headless = headless_mode
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    print("Driver has been initialized")
    return driver


def take_screenshot(driver, url, root_domain):
    screenshot_loc = root_domain+"/screenshot.png"
    Path(root_domain).mkdir(parents=True, exist_ok=True)
    driver.save_screenshot(screenshot_loc)
    print("Saved screenshot of " +url+" in " + screenshot_loc)

def http_responses(driver, url, root_domain, logs):
    urls = []
    csv_loc = root_domain+"/http_responses.csv"
    f = open(csv_loc, "w")
    writer = csv.writer(f)
    header = ["URL", "HTTP-Status-Code", "Content-Type"]
    writer.writerow(header)
    if logs:
        print("URL HTTP-Status-Code Content-Type")

    for request in driver.requests:
        if request.response:
            responses = request.url, request.response.status_code, request.response.headers['Content-Type']
            if logs:
                print(responses)
            writer.writerow(responses)
            urls.append(request.url)
    f.close()
    print("Saved HTTP responses info in " + csv_loc)
    return urls

def save_to_csv(url, status_code, content_type):
    header = ["URL", "HTTP-Status-Code", "Content-Type"]
    data = [url, status_code]


def reap(driver, urls, url_root_domain, logs):
    print("Saving the resources...")
    i = 0
    try:
        for url in urls:
            driver.get(url)
            time.sleep(1)
            src = driver.page_source
            file_path = urlparse(url).path
            file_name = os.path.basename(file_path)
            only_path = file_path.replace(file_name, '')
            domain = extract_root_domain(url)
            domain_path = domain + only_path

            if file_name == "":
                file_name = str(i)
                i = i+1

            scrape_dir = url_root_domain +"/"+ domain_path
            full_path = scrape_dir + file_name

            Path(scrape_dir).mkdir(parents=True, exist_ok=True)
            f = open(full_path, "w")
            f.write(src)
            f.close()
            if logs:
                print("Saved " + url + " in " + full_path)

        print("Saved the resources successfully in "+ url_root_domain)
    except Exception as e:
        print("Error saving the resources... exiting")
        sys.exit()



def main():

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--url', required=True)
        parser.add_argument('-headless', action='store_true', help="Run in headless mode")
        parser.add_argument('-log', action='store_true', help="Output logs")
        args = parser.parse_args()
        url = args.url
        if args.headless:
            headless_mode = True
            print("Will run in headless mode...")
        else:
            headless_mode = False
            print("Will run in non-headless mode...")

        if args.log:
            logs = True
            print("Will output logs...")
        else:
            logs = False
            print("Will not output logs...")

        if checkers.is_url(url) == True:
            print("Valid URL, continuing...")
        elif checkers.is_url(url) == False:
            print("Invalid URL, exiting...")
            sys.exit()

        root_domain = extract_root_domain(url)
        urls = []

        driver = initialize_driver(headless_mode)
        driver.get(url)
        time.sleep(5)

        take_screenshot(driver, url, root_domain)

        urls = http_responses(driver, url, root_domain, logs)

        reap(driver, urls, root_domain, logs)

    except Exception as e:
        print("Error... exiting")
        sys.exit()

    driver.close()


main()