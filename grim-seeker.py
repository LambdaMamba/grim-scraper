from bs4 import BeautifulSoup
from selenium import webdriver
from seleniumwire import webdriver
import urllib.request
import re
import base64
import argparse

def seek(file_name):
    #print("********* Running grim-seeker *********")
    html_page = open(file_name, 'r')
    page_string = html_page.read()
    soup = BeautifulSoup(page_string, "html.parser")
    print("Links found inside " +file_name+" from 'href':")
    for link in soup.findAll('a'):
        links = link.get('href')
        print(links)

    php = re.findall(r'(?i)http\S+php', page_string)

    if php:
        print("PHP endpoint found inside " +file_name+":")
        for url in php:
            print(url)

    #Use regex to search for Base64 encoded strings
    b_64 = re.findall(r'["](?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4})["]', page_string)
    b_64_2 = re.findall(r"['](?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4})[']", page_string)

    if b_64:
        for word in b_64:
            if len(word) > 10:
                stripped = word.strip('"')
                print("Found a possible Base 64 string: "+ stripped)
                dec_64 = base64.b64decode(stripped).decode()
                print("Decoded from Base64: "+ str(dec_64))
    if b_64_2:
        for word in b_64_2:
            if len(word) > 10:
                stripped = word.strip("'")
                print("Found a possible Base 64 string: "+ stripped)
                dec_64 = base64.b64decode(stripped).decode()
                print("Decoded from Base64: "+ str(dec_64))

    #print("********* End grim-seeker *********")
 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', required=True, help="Specify the filename")
    args = parser.parse_args()
    seek(args.filename)


main()