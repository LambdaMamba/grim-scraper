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
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.action_chains import ActionChains

def check_alerts(driver):
    try:

        WebDriverWait(driver, 1).until(EC.alert_is_present(),'Timed out')
        print("Alert has showed up...")
        alerts = driver.switch_to.alert
        alerts.accept()
        print("Alert dismissed...")
    except TimeoutException:
        print("No alert found...")
            


def extract_root_domain(url):
    tsd, td, tsu = extract(url)
    if tsd == "":
        top = td + '.' + tsu
    else:
        top = tsd + '.' + td + '.' + tsu
    return top


def initialize_driver(headless_mode, useragent, root_domain):
    options = webdriver.ChromeOptions()
    path = os.path.dirname(os.path.abspath(__file__))
    download_dir = path+"/"+root_domain+"/downloads"

    prefs = {
    "download.default_directory" : download_dir,
    'safebrowsing.enabled': True
    }      
    options.add_experimental_option("prefs", prefs)

    options.add_argument("user-agent="+useragent)
    options.headless = headless_mode
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    print("Driver has been initialized")
    return driver, download_dir


def take_screenshot(driver, url, root_domain):
    screenshot_loc = root_domain+"/screenshot.png"
    driver.save_screenshot(screenshot_loc)
    print("Saved screenshot of " +url+" in " + screenshot_loc)


def check_duplicate(urls, url):
    duplciate = 0
    if url[-1]=="/":
        url = url[:-1]
    
    if url in urls:
        duplicate = True
    else:
        duplicate = False
    return duplicate
    

def http_responses(driver, url, root_domain, logs):
    urls_filetype = {}
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

            duplicate = check_duplicate(urls, request.url)
            if duplicate:
                continue
            urls.append(request.url)
            urls_filetype[request.url] = request.response.headers['Content-Type']
    
    f.close()
    print("Saved HTTP request/responses info in " + csv_loc)
    return urls, urls_filetype

def save_to_csv(url, status_code, content_type):
    header = ["URL", "HTTP-Status-Code", "Content-Type"]
    data = [url, status_code]


def reap(driver, urls, url_root_domain, logs, all_resource, urls_filetype, filetype, alert, download_dir):
    print("Saving the resources...")
    try:
        for url in urls:
            i=0
            j=0

            domain = extract_root_domain(url)
            filetype_str = str(urls_filetype[url])
            if ((not all_resource) and (domain != url_root_domain)):
                continue
            if ( (filetype_str.find(filetype) == -1) and (filetype != "*")):
                continue
            driver.get(url)
            time.sleep(2)
            if alert:
                check_alerts(driver)
            src = driver.page_source
            file_path = urlparse(url).path
            file_name = os.path.basename(file_path)
            only_path = file_path.replace(file_name, '')
            domain_path = domain + only_path

            if file_name == "":
                file_name = "index"

            scrape_dir = url_root_domain +"/"+ domain_path
            

            if len(file_name) > 250:
                file_name = file_name[0:10]+"_"+file_name[-10:]
                if logs:
                    print("File name too long, changed name to "+ file_name)
            

            #Cannot make dir if a same filename exists, so rename the directory to something different
            
            if not os.path.isdir(scrape_dir):
                try:
                    Path(scrape_dir).mkdir(parents=True, exist_ok=True)
                except OSError as e:
                    temp = scrape_dir[:-1]
                    scrape_dir = temp +"_"+str(j)+"/"
                    Path(scrape_dir).mkdir(parents=True, exist_ok=True)
                if logs:
                    print("Made directory "+scrape_dir)
                time.sleep(0.5)
            else:
                if logs:
                    print(scrape_dir + " directory exists, continuing in that directory...")

            full_path = scrape_dir + file_name


            if os.path.isfile(full_path):
                new_path = scrape_dir + str(i)+"_"+file_name
                i=i+1
                if logs:
                    print(full_path + " exists, renaming to " +new_path)
                full_path = new_path

            #Check if file is inside /downloads. If so move to the proper directory
            downloaded = download_dir+"/"+file_name
            if os.path.isfile(downloaded):
                os.rename(downloaded, full_path)
                print(file_name + " exists in " +downloaded+ ", moved to "+ full_path)
            else: 
                f = open(full_path, "w")
                f.write(src)
                f.close()
                if logs:
                    print("Saved " + url + " in " + full_path)
            
    except Exception as e:
        print(e)
        print("Error saving the resources... exiting...")
        sys.exit()

    print("Saved the resources successfully in "+ url_root_domain)

def main():

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--url', required=True, help="Specify the URL")
        parser.add_argument('--filetype', required=False, help="Specify the resource filetype to save")
        parser.add_argument('--useragent', required=False, help="Specify the user agent")
        parser.add_argument('-headless', action='store_true', help="Run in headless mode")
        parser.add_argument('-log', action='store_true', help="Output logs")
        parser.add_argument('-all', action='store_true', help="Save all resources found in HTTP request/response")
        parser.add_argument('-alert', action='store_true', help="Accept pop up alert")
        args = parser.parse_args()
        url = args.url

        if checkers.is_url(url) == True:
            print("Valid URL, continuing...")
        elif checkers.is_url(url) == False:
            print("Invalid URL, exiting...")
            sys.exit()

        if args.filetype:
            filetype = args.filetype
            print("Will save resources of filetype "+filetype+"...")
        else:
            filetype = "*"
            print("Will save resources of any filetype...")

        if args.useragent:
            useragent = args.useragent
            print("Will use the uger agent "+useragent+"...")
        else:
            useragent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
            print("Will use the default user agent "+useragent+"...")
        

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


        root_domain = extract_root_domain(url)
        urls = []
        urls_filetype = {}

        if args.all:
            all_resource = True
            if (filetype == "*"):
                print("Will save all resources found in HTTP request/response...")
            else:
                print("Will save all " +filetype+" resources found in HTTP request/response...")
        else:
            all_resource = False
            if (filetype == "*"):
                print("Will only save main resources...")
            else:
                print("Will only save main resources with filetype "+filetype+"...")

        if args.alert:
            alert = True
            print("Will accept pop alert...")
        else:
            alert = False

        Path(root_domain).mkdir(parents=True, exist_ok=True)
        print("Made a directory " +root_domain)
        driver, download_dir = initialize_driver(headless_mode, useragent, root_domain)
        driver.get(url)
        time.sleep(2)

        if alert:
            check_alerts(driver)
            

        take_screenshot(driver, url, root_domain)

        urls, urls_filetype = http_responses(driver, url, root_domain, logs)

        reap(driver, urls, root_domain, logs, all_resource, urls_filetype, filetype, alert, download_dir)

    except Exception as e:
        print(e)
        print("Error... exiting")
        sys.exit()

    driver.close()


main()