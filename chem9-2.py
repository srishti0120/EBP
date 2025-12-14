# coding: UTF-8

import os
import urllib.parse
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# All your URLs
target_urls = [
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-2.html",
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-3.html",
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-4.html",
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-5.html",
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-6.html",
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-7.html",
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-8.html",
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-9.html",
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-10.html",
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-11.html",
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-12.html",
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-13.html",
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-14.html",
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-15.html",
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-16.html",
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-17.html",
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-18.html",
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-19.html",
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-20.html",
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-21.html",
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-22.html",
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-23.html",
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-24.html",
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-25.html",
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-26.html",
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-27.html",
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-28.html",
    "https://unit.aist.go.jp/riss/crm/mainmenu/1-29.html"
]

# Ensure output directory exists
os.makedirs("chem9-2", exist_ok=True)

with open("title9.txt", "a", encoding="utf-8") as f_out:
    options = Options()
    options.add_experimental_option('detach', True)
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)

    for target_url in target_urls:
        try:
            driver.get(target_url)
            time.sleep(2)  # Wait for page to load
        except Exception as e:
            print('WEBアクセスに失敗しました:', e)
            continue

        print('WEBアクセスに成功しました:', target_url)
        source = driver.page_source
        soup = BeautifulSoup(source, "lxml")
        # Find all links to zip and pdf files
        file_links = soup.select("a[href$='.zip'], a[href$='.pdf']")

        print(f"Found {len(file_links)} downloadable files on {target_url}")

        for link in file_links:
            href = link.get("href")
            if not href:
                continue
            download_url = urllib.parse.urljoin(target_url, href)
            file_name = os.path.join("chem9-2", download_url.split("/")[-1])

            print(f"Downloading: {download_url}")
            print(download_url, file=f_out)  # Save URL to title9.txt

            try:
                response = requests.get(download_url)
                if response.status_code == 200 and (response.headers.get("Content-Type", "").startswith("application/zip") or response.headers.get("Content-Type", "").startswith("application/pdf")):
                    with open(file_name, "wb") as f:
                        f.write(response.content)
                    print(f"Saved: {file_name}")
                else:
                    print(f"Failed to download {download_url}: HTTP {response.status_code}, Content-Type: {response.headers.get('Content-Type')}")
            except Exception as e:
                print(f"Error downloading {download_url}: {e}")

    driver.quit()



