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
from selenium.webdriver.common.by import By
import importlib  
from bs4 import BeautifulSoup


def check_alerts(driver):
    try:
        #Wait unti a Javascript pop up alert shows up
        WebDriverWait(driver, 1).until(EC.alert_is_present(),'Timed out')
        print("Alert has showed up...")
        alerts = driver.switch_to.alert
        #Accept the alert
        alerts.accept()
        print("Alert accepted...")
    except TimeoutException:
        print("No alert found...")


def dismiss_alert(driver):
    try:
        #Wait unti a Javascript pop up alert shows up
        WebDriverWait(driver, 1).until(EC.alert_is_present(),'Timed out')
        if (EC.alert_is_present()):
            print("Alert has showed up...")
            alerts = driver.switch_to.alert
            #dismiss the alert
            alerts.dismiss()
            print("Alert dismissed...")
            return True
    except TimeoutException:
        return False



def extract_root_domain(url):
    tsd, td, tsu = extract(url)
    if tsd == "":
        top = td + '.' + tsu
    else:
        #Include subdomain if it exists
        top = tsd + '.' + td + '.' + tsu
    return top


def initialize_driver(headless_mode, useragent, root_domain, proxy, proxycred):
    try:
        options = webdriver.ChromeOptions()
        path = os.path.dirname(os.path.abspath(__file__))
        #Download files inside the /root_domain/downloads
        download_dir = path+"/"+root_domain+"/downloads"
        #Use these preferences to bypass the "This Type of File Can Harm Your Computer" alert, and download the files
        prefs = {
        "download.default_directory" : download_dir,
        'safebrowsing.enabled': True
        }      
        options.add_experimental_option("prefs", prefs)

        options.add_argument("user-agent="+useragent)

        #options.add_argument('--proxy-server='+str(proxy))
        options.headless = headless_mode

        #If proxy is set, set these options in selenium-wire
        if proxy != "":
            if (proxycred != ""):
                seleniumwire_options = {
                    'proxy': {
                        'http': f'http://{proxycred}@{proxy}',
                        'https': f'https://{proxycred}@{proxy}',
                    },
                }
            else:
                #If no username and password is provided
                seleniumwire_options = {
                    'proxy': {
                        'http': f'http://{proxy}',
                        'https': f'https://{proxy}',
                    },
                } 
            
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options, seleniumwire_options=seleniumwire_options)
        else:
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        print("Driver has been initialized")
        return driver, download_dir

    except Exception as e:
        print(e)
        print("Error initializing driver...")
        return False, False

def take_screenshot(driver, url, root_domain, num):
    #Take screenshot and save it in /root_domain/screenshot.png
    if num == 0:
        screenshot_loc = root_domain+"/screenshot.png"
    else:
        num = num.replace("/", "-" )
        screenshot_loc = root_domain+"/screenshot_"+str(num)+".png"
    driver.save_screenshot(screenshot_loc)
    print("Saved screenshot of " +url+" in " + screenshot_loc)


def check_duplicate(urls, url):
    #Use this to check for duplicate URLs in the HTTP requests/responses to prevent visiting URL multiple times
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
            #Write the HTTP request/response to root_domain/http_responses.csv
            writer.writerow(responses)

            duplicate = check_duplicate(urls, request.url)
            #Skip if URL is duplicate
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
    

def href_find(file_name, page_string):
    links = []
    soup = BeautifulSoup(page_string, "html.parser")
    print("Links found inside " +file_name+" from 'href':")
    for link in soup.findAll('a'):
        url = link.get('href')
        print(url)
        links.append(url)
    return links


def file_utils(url_now, domain, root_domain, download_dir, src, logs, i, j):
    try:
        file_path = urlparse(url_now).path
        file_name = os.path.basename(file_path)
        only_path = file_path.replace(file_name, '')
        domain_path = domain + only_path
        #If file has no name, name it as "index"
        if file_name == "":
            file_name = "index"

        scrape_dir = root_domain +"/"+ domain_path

        
        #Truncate if file name is too long. Take first 10 and last 10 characters, and concatanate with _ between
        if len(file_name) > 250:
            file_name = file_name[0:10]+"_"+file_name[-10:]
            if logs:
                print("File name too long, changed name to "+ file_name)
        

        #Check if directory exists, if not make one
        if not os.path.isdir(scrape_dir):
            try:
                Path(scrape_dir).mkdir(parents=True, exist_ok=True)
            except OSError as e:
                #Cannot make dir if a same filename exists, so rename the directory
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

        #Check if file exists, if yes rename the file
        if os.path.isfile(full_path):
            new_path = scrape_dir + str(i)+"_"+file_name
            i=i+1
            if logs:
                print(full_path + " exists, renaming to " +new_path)
            full_path = new_path

        downloaded = download_dir+"/"+file_name
        f = open(full_path, "w")
        f.write(src)
        f.close()
        if logs:
            print("Saved " + url_now + " in " + full_path)
        #Check if file is inside /root_domain/downloads. If yes move to the proper directory
        # if os.path.isfile(downloaded):
        #     os.rename(downloaded, full_path)
        #     print(file_name + " exists in " +downloaded+ ", moved to "+ full_path)
        # else: 
        #     f = open(full_path, "w")
        #     f.write(src)
        #     f.close()
        #     if logs:
        #         print("Saved " + url_now + " in " + full_path)

        return True
    except Exception as e:
        print(e)
        print("Error with files...")
        return False
    

def reap(driver, urls, url_root_domain, logs, all_resource, urls_filetype, filetype, alert, download_dir, wait_time, root_domain, main_url, href):
    #Reap the resources
    print("Saving the resources...")
    try:
        main_index = ""
        for url in urls:
            i=0
            j=0
            domainn = extract_root_domain(url)
            filetype_str = str(urls_filetype[url])
            #If -all not enabled, only reap resources under root domain (exclude redirect cases)
            if ((not all_resource) and (domainn != url_root_domain)):
                continue
            #If --filetype is specified, get the file type from the HTTP request/response for the URL
            if ( (filetype_str.find(filetype) == -1) and (filetype != "*")):
                continue

            driver.set_page_load_timeout(wait_time)
            driver.get(url)
            dismiss_alert(driver)
            if alert:
                check_alerts(driver)
            #In case of redirect, check the current URL of driver
            src = driver.page_source
            url_now = driver.current_url
            domain = extract_root_domain(url_now)

            #Save main index src
            if (main_url == url) or (main_url+"/" == url):
                main_index = src

            #Check if redirect occured
            if (url != url_now):
                print("Redirect has occured: " + url + " -> " + url_now)

            result = file_utils(url_now, domain, root_domain, download_dir, src, logs, i, j)
        
        if (href):
            links = href_find(main_url, main_index)
            for link in links:
                i=0
                j=0
                #Check if full link is inside href
                if not (main_url.lower().strip("/") in link.lower()):
                    if not ("http" in link.lower()):
                        link = main_url.strip("/")+"/"+link.lower().strip("/")

                print("Going to " +link+"...")
                driver.set_page_load_timeout(wait_time)
                driver.get(link)
                dismiss_alert(driver)
                if alert:
                    check_alerts(driver)
                #Take screenshot of href
                take_screenshot(driver, link, root_domain, urlparse(link).path.strip("/").strip("..").strip("../"))
                #In case of redirect, check the current URL of driver
                src = driver.page_source
                url_now = driver.current_url
                domain = extract_root_domain(url_now)
                result = file_utils(url_now, domain, root_domain, download_dir, src, logs, i, j)
        print("Saved the resources successfully in "+ root_domain)
        return True
            
    except Exception as e:
        print(e)
        print("Error saving the resources... exiting...")
        return False
        





def check_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True, help="Specify the URL")
    parser.add_argument('--filetype', required=False, help="Specify the resource filetype to save")
    parser.add_argument('--useragent', required=False, help="Specify the user agent. Default is 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'")
    parser.add_argument('--time', required=False, help="Seconds to wait for page to load. Default is 30 seconds")
    parser.add_argument('--status', required=False, help="Specify status code of main page. Do not scrape if main page does not match this status code.")
    parser.add_argument('--proxy', required=False, help="Specify proxy PROXY:PORT")
    parser.add_argument('--proxycred', required=False, help="Specify proxy credentials USER:PASS")
    parser.add_argument('-headless', action='store_true', help="Run in headless mode")
    parser.add_argument('-log', action='store_true', help="Output logs")
    parser.add_argument('-all', action='store_true', help="Save all resources found in HTTP request/response")
    parser.add_argument('-alert', action='store_true', help="Accept pop up alert")
    parser.add_argument('-login', action='store_true', help="Attempt login using dummy email and password")
    parser.add_argument('-href', action='store_true', help="Scrape all href links from main page and take screenshot")
    args = parser.parse_args()
    url = args.url

    if checkers.is_url(url) == True:
        print("Valid URL, continuing...")
        txt = False
    elif checkers.is_url(url) == False:
        if os.path.isfile(url):
            print("Will use the URLs inside "+url+"...")
            txt = True
        else:
            print("Invalid URL, exiting...")
            sys.exit()

    if args.status:
        statuscode = args.status
        print("Will only scrape if main page has status code " + statuscode + "...")
    else:
        statuscode = "*"
        #print("Will scrape main page regardless of status code...")
    
    if args.proxy:
        proxy = args.proxy
        if args.proxycred:
            proxycred = args.proxycred
        else:
            proxycred = ""
    else:
        proxy = ""
        proxycred = ""

    if (args.proxycred) and (proxy == ""):
        print("Please specify proxy before specifying credentials!! Exiting...")
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
        #Defailut user agent is Linux Chrome, "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        useragent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        print("Will use the default user agent "+useragent+"...")

    if args.time:
        wait_time = float(args.time)
        print("Will wait "+str(wait_time)+" seconds for pages to load...")
    else:
        #Default wait time is 30 seconds
        wait_time = 30
    

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

    if args.login:
        login = True
        print("Will attempt to login using a dummy email and password...")
    else:
        login = False

    if args.href:
        href = True
        print("Will scrape all links found inside HREF inside index...")
    else:
        href = False



    return url, filetype, useragent, headless_mode, logs, all_resource, alert, wait_time, txt, statuscode, proxy, proxycred, login, href



def check_dir(root_domain):
    i = 0

    new_dir = root_domain
    #Check if directory exists, if yes rename
    while os.path.isdir(new_dir):
        #Try appending a number to the end of the directory until its unique
        print(new_dir + " directory already exists...")
        new_dir = root_domain+"_"+str(i)
        i = i+1
    
    #Make a directory /new_dir
    Path(new_dir).mkdir(parents=True, exist_ok=True)
    print("Made a directory " +new_dir)
    return new_dir

def rm_dir(root_domain):
    try:
        if os.path.isdir:
            os.rmdir(root_domain)
        return True
    except Exception as e:
        print(e)
        print("Error removing "+ root_domain)
        return False


def read_txt(filename):
    url_txt = []
    txt_file = open(filename, 'r')
    Lines = txt_file.readlines()
    for line in Lines:
        noline = line.replace("\n", "")
        if checkers.is_url(noline) == True:
            print(noline+" is a valid URL...")
            url_txt.append(noline)
        else:
            print(noline+" is an invalid URL, skipping...")
    return url_txt


def attempt_login(driver):
    try:
        time.sleep(2)
        #Attempt all these Elements for username field
        user_list = ["input[type='text']", "input[type='email']", "input[name='email']", "input[name='username']", "input[name='user']", "input[name='id']", "input[name='name']"]
        for text in user_list:
            res = key_send(driver, text)
            if res:
                print("Successfully inputted fake login credentials...")
                return True
        print("Failed to input fake login credentials...")
        return False
    except Exception as e:
        print("Failed to input fake login credentials...")
        return False


def key_send(driver, username):
    try:
        user_field = driver.find_element(By.CSS_SELECTOR, username)
        user_field.send_keys("john@randommail.com")
        time.sleep(0.5)
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        password_field.send_keys("RandomPassword")
        password_field.send_keys(Keys.ENTER)
        return True
    except Exception as e:
        return False

def grim(url, filetype, useragent, headless_mode, logs, all_resource, alert, wait_time, txt, statuscode, proxy, proxycred, login, href):
    try:
        root_domain = extract_root_domain(url)
        url_root_domain = root_domain
        urls = []
        urls_filetype = {}
        responses = 0
        #This will be the working directory
        root_domain = check_dir(root_domain)

        driver, download_dir = initialize_driver(headless_mode, useragent, root_domain, proxy, proxycred)
        if (driver == False):
            print("Due to error in driver initialization, exiting...")
            return False
        driver.set_page_load_timeout(wait_time)
        driver.get(url)

        #Dismiss alerts if found by default. Will not dismiss if -alert is set
        if not alert:
            res = dismiss_alert(driver)

        #Find the status code of the main page
        for request in driver.requests:
            if request.response:
                if (request.url == url) or (request.url == url+"/"):
                    responses = request.response.status_code
                    break
        

        print("Status code of " +url+ " is " + str(responses))

        #Only scrape if status code matches the specified status code. If it doesn't match, remove the directory and quit.
        if (statuscode != "*") and (str(responses) != str(statuscode)):
            print("Status code of " +url+ " does not match "  + str(statuscode) + " removing " + root_domain + " directory and quitting...")
            rm = rm_dir(root_domain)
            driver.close()
            return False
        
        else:
            num = 0
            #If -alert is enabled, check for Javascript popup alert and accept
            if alert:
                check_alerts(driver)

            url1 = driver.current_url

            take_screenshot(driver, url, root_domain, num)
            if login:
                #Check behavior of site if attempting fake login using dummy email and password
                num = num + 1
                logged = attempt_login(driver)
                url2 = driver.current_url
                if logged:
                    #Take screenshot after fake login
                    take_screenshot(driver, url, root_domain, num)
                else:
                    print("Failed dummy login...")

            urls, urls_filetype = http_responses(driver, url, root_domain, logs)

            result = reap(driver, urls, url_root_domain, logs, all_resource, urls_filetype, filetype, alert, download_dir, wait_time, root_domain, url, href)

            if not result:
                driver.close()
                return False

            driver.close()
            return True
    except TimeoutException as e:
        print("Timed out loading. Try setting a longer time using --time")
        driver.close()
        return False
    except Exception as e:
        print(e)
        print("Error for URL " + url)
        driver.close()
        return False


def main():
    try:
        url, filetype, useragent, headless_mode, logs, all_resource, alert, wait_time, txt, statuscode, proxy, proxycred, login, href = check_args()

        if txt:
            url_txt = []
            url_txt = read_txt(url)
            #If reading URLs from a file, perform the scraping for each URL
            for urll in url_txt:
                success = grim(urll, filetype, useragent, headless_mode, logs, all_resource, alert, wait_time, txt, statuscode, proxy, proxycred, login, href)
                if success:
                    print("Success for " + urll)
                else:
                    print("Fail for " + urll)

        else:
            #If only a single URL is provided, perform scraping once
            success = grim(url, filetype, useragent, headless_mode, logs, all_resource, alert, wait_time, txt, statuscode, proxy, proxycred, login, href)
            if success:
                print("Success for " + url)
            else:
                print("Fail for " + url)

    except Exception as e:
        print(e)
        print("Error... exiting")
        sys.exit()

main()