from bs4 import BeautifulSoup
from selenium import webdriver
from seleniumwire import webdriver
import urllib.request
import re
import base64
import argparse
import html

import urllib

def href(file_name, page_string):
    soup = BeautifulSoup(page_string, "html.parser")
    print("Links found inside " +file_name+" from 'href':")
    for link in soup.findAll('a'):
        links = link.get('href')
        print(links)
    return links

def doublequote(file_name, page_string):
    dq_list = []
    #Find all string inside double quote
    dq = re.findall(r'(?i)"(.*?)"', page_string)

    if dq:
        for word in dq:
            dq_list.append(word.strip('"'))
    return dq_list

def singlequote(file_name, page_string):
    sq_list = []
    #Find all string inside single quote
    sq = re.findall(r"(?i)'(.*?)'", page_string)
    if sq:
        for word in sq:
            sq_list.append(word.strip("'"))
    return sq_list

def php(file_name, page_string, words):
    if words:
        for word in words:
            #Put character length limit to speed up
            if (len(word) > 3) and (len(word) < 500):
                #Match .php inside single or double quote
                match = re.findall(r'(?i)\S+\.php', word)
                if match:
                    for wor in match:
                        print("PHP endpoint found inside " +file_name+": " + wor)
    

def apk(file_name, page_string, words):
    if words:
        for word in words:
            #Put character length limit to speed up
            if (len(word) > 3) and (len(word) < 500):
                #Match .apk inside single or double quote
                match = re.findall(r'(?i)\S+\.apk', word)
                if match:
                    for wor in match:
                        print("APK found inside " +file_name+": " + wor)

def email_addr(file_name, page_string, words):
    #This takes time to match, so only do if --email option is enabled
    match = re.findall(r"(?i)[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", page_string)
    if match:
        for wor in match:
            print("Email found inside " +file_name+": " + wor)


def b64(file_name, page_string, words):
    #Use regex to search for Base64 encoded strings
    if words:
        for word in words:
            if len(word) > 10:
                match = re.findall(r'^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$', word)
                if match:
                    for wor in match:
                        res = verify_b64(wor)
                        dec_64 = base64.b64decode(wor)
                        decoded = str(dec_64).strip("b")
                        decoded = decoded.strip("'")
                        decoded = decoded.strip('"')
                        res = verify_b64(decoded)
                        if res:
                            print("Found a possible Base 64 string: "+ wor)
                            print("Decoded from Base64: "+ decoded)

def verify_b64(decoded):
    #Verify if base64 encoded, by checking if decoded word contains "\x"
    if "\\x" in decoded:
        return False
    else:
        return True

def unesc(file_name, page_string):
    unescc = re.findall(r'(?i)unescape\(([^)]+)\)', page_string)
    if unescc:
        print("unescape() detected inside "+file_name)
        for word in unescc:
            string = word.strip("unescape(")
            string = string.strip(")")
            string = string.strip("'")
            string = string.strip('"')
            unescaped = html.unescape(string)
            percentdec = urllib.parse.unquote(unescaped)
            print("The unescaped and percent decoded text: \n"+percentdec)

def seek(file_name, email):
    try:
        #print("********* Running grim-seeker *********")
        dq_list = []
        sq_list = []
        words = []
        html_page = open(file_name, 'r')
        page_string = html_page.read()
        #Search for words enclosed in single or double quotes
        dq_list = doublequote(file_name, page_string)
        sq_list = singlequote(file_name, page_string)
        words = dq_list + sq_list
        links = href(file_name, page_string)
        print()
        php(file_name, page_string, words)
        print()
        apk(file_name, page_string, words)
        print()
        if email:
            email_addr(file_name, page_string, words)
            print()
        b64(file_name, page_string, words)
        print()
        unesc(file_name, page_string)

    except Exception as e:
        print(e)

    #print("********* End grim-seeker *********")
 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True, help="Specify the filename")
    parser.add_argument('-email', action='store_true', help="To find email addresses inside file")
    args = parser.parse_args()
    seek(args.file, args.email)


main()