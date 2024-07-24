#!/usr/bin/env python3

import argparse
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse
import threading
import time

# Banner
BANNER = """
====================================
          JS Keeper Script
====================================
Usage:
    -u, --url      : Single URL to parse for javascript files
    -l, --list     : File containing list of URLs to parse
    -t, --threads  : Number of threads to use (default: 1)
    -h, --headers  : HTTP headers to be used with requests in JSON format
    -n, --rate     : Number of requests per second (default: no limit)
    -help, --help  : Display help information
====================================
"""


def download_js(session, url, save_dir, headers, rate_limit):
    try:
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            file_name = os.path.basename(urlparse(url).path)
            file_path = os.path.join(save_dir, file_name)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {file_name}")
        else:
            print(f"Failed to download: {url}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")


def parse_and_download(session, url, save_dir, headers, rate_limit):
    try:
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            js_files = [urljoin(url, script['src']) for script in soup.find_all('script') if script.get('src')]
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            for js_url in js_files:
                download_js(session, js_url, save_dir, headers, rate_limit)
                if rate_limit:
                    time.sleep(1 / rate_limit)
        else:
            print(f"Failed to access {url}")
    except Exception as e:
        print(f"Error parsing {url}: {e}")


def main():
    parser = argparse.ArgumentParser(description='JS Keeper Script', add_help=False)
    parser.add_argument('-u', '--url', type=str, help='Single URL to parse')
    parser.add_argument('-l', '--list', type=str, help='File containing list of URLs to parse')
    parser.add_argument('-t', '--threads', type=int, default=1, help='Number of threads to use (default: 1)')
    parser.add_argument('-h', '--headers', type=str, help='HTTP headers in JSON format')
    parser.add_argument('-n', '--rate', type=int, help='Number of requests per second (default: no limit)')
    parser.add_argument('-help', '--help', action='store_true', help='Display help information')

    args = parser.parse_args()

    if args.help:
        print(BANNER)
        parser.print_help()
        return

    headers = {}
    if args.headers:
        import json
        headers = json.loads(args.headers)

    session = requests.Session()

    if args.url:
        urls = [args.url]
    elif args.list:
        with open(args.list, 'r') as file:
            urls = [line.strip() for line in file]
    else:
        print(BANNER)
        parser.print_help()
        return

    threads = []
    for url in urls:
        thread = threading.Thread(target=parse_and_download, args=(session, url, 'downloaded_js', headers, args.rate))
        threads.append(thread)
        thread.start()

        if len(threads) >= args.threads:
            for t in threads:
                t.join()
            threads = []

    for t in threads:
        t.join()

if __name__ == '__main__':
    main()
