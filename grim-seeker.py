from bs4 import BeautifulSoup
from selenium import webdriver
from seleniumwire import webdriver
import urllib.request
import re
import base64
import argparse

def href(file_name, page_string):
    soup = BeautifulSoup(page_string, "html.parser")
    print("Links found inside " +file_name+" from 'href':")
    for link in soup.findAll('a'):
        links = link.get('href')
        print(links)

def php(file_name, page_string):
    php = re.findall(r'(?i)"\S+\.php"', page_string)
    php2 = re.findall(r"(?i)'\S+\.php'", page_string)

    if php:
        print("PHP endpoint found inside " +file_name+":")
        for url in php:
            print(url.strip('"'))

    if php2:
        print("PHP endpoint found inside " +file_name+":")
        for url in php2:
            print(url.strip("'"))


def apk(file_name, page_string):
    apk = re.findall(r'(?i)"\S+\.apk"', page_string)
    apk2 = re.findall(r"(?i)'\S+\.apk'", page_string)

    if apk:
        print("APK found inside " +file_name+":")
        for url in apk:
            print(url.strip('"'))

    if apk2:
        print("APK found inside " +file_name+":")
        for url in apk:
            print(url.strip("'"))

def b64(file_name, page_string):
    #Use regex to search for Base64 encoded strings
    b_64 = re.findall(r'["](?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4})["]', page_string)
    b_64_2 = re.findall(r"['](?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4})[']", page_string)

    if b_64:
        for word in b_64:
            if len(word) > 10:
                stripped = word.strip('"')
                print("Found a possible Base 64 string: "+ stripped)
                dec_64 = base64.b64decode(stripped)
                decoded = str(dec_64).strip("b")
                decoded = decoded.strip("'")
                decoded = decoded.strip('"')
                print("Decoded from Base64: "+ decoded)
    if b_64_2:
        for word in b_64_2:
            if len(word) > 10:
                stripped = word.strip("'")
                print("Found a possible Base 64 string: "+ stripped)
                dec_64 = base64.b64decode(stripped)
                decoded = str(dec_64).strip("b")
                decoded = decoded.strip("'")
                decoded = decoded.strip('"')
                print("Decoded from Base64: "+ decoded)


def seek(file_name):
    try:
        #print("********* Running grim-seeker *********")
        html_page = open(file_name, 'r')
        page_string = html_page.read()
        href(file_name, page_string)
        php(file_name, page_string)
        apk(file_name, page_string)
        b64(file_name, page_string)

    except Exception as e:
        print(e)

    #print("********* End grim-seeker *********")
 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True, help="Specify the filename")
    args = parser.parse_args()
    seek(args.file)


main()