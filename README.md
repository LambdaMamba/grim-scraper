#　The Grim Scraper

A Selenium Python Scraper for Scraping websites, and downloading their resources.

##　Example usage:

`python3 grim-scraper.py --url https://github.com/login`

-First, it will visit `https://github.com/login` using Selenium, and a screenshot of the site will be saved in `github.com/screenshot.png`.

-Second, it will check the HTTP requests and responses, and will save the `URL HTTP-Status-Code Content-Type` information in `github.com/http_responses.csv`.

-Third, it will visit the URLs found in the HTTP requests and responses. The source codes will be saved in their respective folders and file names.


##　Running in headless mode (`-headless` flag):

`python3 grim-scraper.py --url https://github.com/login -headless`


##　Output the logs (`-log` flag):

`python3 grim-scraper.py --url https://github.com/login -log`


##　Specify resource filetype to save (Use `--filetype` to specify):

`python3 grim-scraper.py --url https://github.com/login --filetype html`

##　Download all resources found in HTTP response/request (`-all` flag):

`python3 grim-scraper.py --url https://github.com/login -all`

(Without `-all` flag, it will only save resources found under `github.com`)


##　Specify the user agent (Use `--usergent` to specify):

`python3 grim-scraper.py --url https://github.com/login --useragent "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36"`

##　Bypass Javascript pop up alerts (`-alert` flag):

`python3 grim-scraper.py --url https://github.com/login -alert"`



##　Example output with `-log` option enabled:

```
URL HTTP-Status-Code Content-Type
('https://accounts.google.com/ListAccounts?gpsia=1&source=ChromiumBrowser&json=standard', 200, 'application/json; charset=utf-8')
('https://github.com/login', 200, 'text/html; charset=utf-8')
('https://github.githubassets.com/assets/light-0946cdc16f15.css', 200, 'text/css')
('https://github.githubassets.com/assets/global-0d04dfcdc794.css', 200, 'text/css')
('https://github.githubassets.com/assets/dark-3946c959759a.css', 200, 'text/css')
('https://github.githubassets.com/assets/github-c7a3a0ac71d4.css', 200, 'text/css')
('https://github.githubassets.com/assets/primer-0e3420bbec16.css', 200, 'text/css')
...
```

```
Saving the resources...
Saved https://accounts.google.com/ListAccounts?gpsia=1&source=ChromiumBrowser&json=standard in github.com/google.com/ListAccounts
Saved https://github.com/login in github.com/github.com/login
Saved https://github.githubassets.com/assets/light-0946cdc16f15.css in github.com/githubassets.com/assets/light-0946cdc16f15.css
Saved https://github.githubassets.com/assets/global-0d04dfcdc794.css in github.com/githubassets.com/assets/global-0d04dfcdc794.css
Saved https://github.githubassets.com/assets/dark-3946c959759a.css in github.com/githubassets.com/assets/dark-3946c959759a.css
Saved https://github.githubassets.com/assets/github-c7a3a0ac71d4.css in github.com/githubassets.com/assets/github-c7a3a0ac71d4.css
Saved https://github.githubassets.com/assets/primer-0e3420bbec16.css in github.com/githubassets.com/assets/primer-0e3420bbec16.css
...
```