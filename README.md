# The Grim Scraper

A Selenium Python Scraper for Scraping websites, and downloading their resources.

## Example usage:
```
python3 grim-scraper.py --url https://github.com/login
```

- First, it will visit `https://github.com/login` using Selenium, and a screenshot of the site will be saved in `github.com/screenshot.png`.

- Second, it will check the HTTP requests and responses, and will save the `URL HTTP-Status-Code Content-Type` information in `github.com/http_responses.csv`.

- Third, it will visit the URLs found in the HTTP requests and responses. The source codes will be saved in their respective folders and file names.

## Arguments, options and flags:

```
usage: grim-scraper.py [-h] --url URL [--filetype FILETYPE] [--useragent USERAGENT] [--time TIME]
                       [--status STATUS] [--proxy PROXY] [--proxycred PROXYCRED] [-headless] [-log]
                       [-all] [-alert]

optional arguments:
  -h, --help            show this help message and exit
  --url URL             Specify the URL
  --filetype FILETYPE   Specify the resource filetype to save
  --useragent USERAGENT
                        Specify the user agent. Default is 'Mozilla/5.0 (X11; Linux x86_64)
                        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
  --time TIME           Seconds to wait for page to load. Default is 10 seconds
  --status STATUS       Specify status code of main page. Do not scrape if main page does not match
                        this status code.
  --proxy PROXY         Specify proxy PROXY:PORT
  --proxycred PROXYCRED
                        Specify proxy credentials USER:PASS
  -headless             Run in headless mode
  -log                  Output logs
  -all                  Save all resources found in HTTP request/response
  -alert                Accept pop up alert
```

**Use URLs from a file (Use `--url` option, and specify the list file name)**
```
python3 grim-scraper.py --url urls.txt
```

**Specify resource filetype to save (Use `--filetype` to specify):**
```
python3 grim-scraper.py --url https://github.com/login --filetype html
```

**Specify the user agent (Use `--usergent` to specify):**
```
python3 grim-scraper.py --url https://github.com/login --useragent "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36"
```

**Specify wait time (Use `--time` to specify):**
```
python3 grim-scraper.py --url https://github.com/login --time 1
```
**Specify HTTP status code (Use `--status` to specify, will only scrape if main page matches this status code):**
```
python3 grim-scraper.py --url https://github.com/login --status 200
```
**Specify proxy (Use `--proxy` to specify, format: `PROXY:PORT`):**
```
python3 grim-scraper.py --url https://github.com/login --proxy 123.123.123.123:8080
```
**Specify proxy username and password (Use `--proxycred` to specify, format: `USER:PASS`):**
```
python3 grim-scraper.py --url https://github.com/login --proxy 123.123.123.123:8080 --proxycred admin:admin
```
**Running in headless mode (`-headless` flag):**
```
python3 grim-scraper.py --url https://github.com/login -headless
```
**Output the logs (`-log` flag):**
```
python3 grim-scraper.py --url https://github.com/login -log
```

**Download all resources found in HTTP response/request (`-all` flag):**
```
python3 grim-scraper.py --url https://github.com/login -all
```

(Without `-all` flag, it will only save resources found under `github.com`)

**Bypass Javascript pop up alerts (`-alert` flag):**
```
python3 grim-scraper.py --url https://github.com/login -alert
```


## Example output with `-log` option enabled:

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