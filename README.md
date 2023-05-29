**The Grim Scraper**
A Selenium Python Scraper for Scraping websites, specifically phishing websites.

Input a URL when prompted.

`Enter the URL: https://github.com/login`

The screenshot of the page will be saved in `screenshot.png`.

It will output the URL HTTP-Status-Code Content-Type in the following format.
```
URL HTTP-Status-Code Content-Type
https://accounts.google.com/ListAccounts?gpsia=1&source=ChromiumBrowser&json=standard 200 application/json; charset=utf-8
https://github.com/login 200 text/html; charset=utf-8
https://github.githubassets.com/assets/light-0946cdc16f15.css 200 text/css
https://github.githubassets.com/assets/dark-3946c959759a.css 200 text/css
https://github.githubassets.com/assets/primer-0e3420bbec16.css 200 text/css
...
```
It will then save all the resources.
```
Saved https://accounts.google.com/ListAccounts?gpsia=1&source=ChromiumBrowser&json=standard in ListAccounts
Saved https://github.com/login in login
Saved https://github.githubassets.com/assets/light-0946cdc16f15.css in light-0946cdc16f15.css
Saved https://github.githubassets.com/assets/dark-3946c959759a.css in dark-3946c959759a.css
Saved https://github.githubassets.com/assets/primer-0e3420bbec16.css in primer-0e3420bbec16.css
Saved https://github.githubassets.com/assets/github-c7a3a0ac71d4.css in github-c7a3a0ac71d4.css
Saved https://github.githubassets.com/assets/global-0d04dfcdc794.css in global-0d04dfcdc794.css
...
```