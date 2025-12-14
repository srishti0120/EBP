# coding: UTF-8

import os
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time

# Ensure 'chem15' directory exists
os.makedirs("chem15", exist_ok=True)

target_urls = ["https://www.sanei.or.jp/?mode=view&cid=290#1"]

# Set Chrome options to keep the browser open after script ends
options = Options()
options.add_experimental_option('detach', True)  # Keeps browser open

# Initialize Chrome driver
service = Service()  # Specify chromedriver path if needed
driver = webdriver.Chrome(service=service, options=options)

for target_url in target_urls:
    try:
        driver.get(target_url)
        print(f"Accessed: {target_url}")
        time.sleep(3)  # Wait for JS to load content if needed
    except Exception as e:
        print('WEBアクセスに失敗しました:', e)
        continue

    source = driver.page_source
    soup = BeautifulSoup(source, "lxml")
    pdf_links = soup.select("a[href$='.pdf']")  # Find all <a> tags with href ending in .pdf

    print(f"Found {len(pdf_links)} PDF links.")

    if not pdf_links:
        # Try printing all links for debugging
        all_links = soup.find_all('a')
        print("No PDF links found. Here are all hrefs on the page:")
        for link in all_links:
            print(link.get('href'))
        continue

    for pdf_link in pdf_links:
        download_frag = pdf_link.get("href")
        if download_frag:
            file_name = os.path.join("chem15", download_frag.split("/")[-1])
            download_url = urllib.parse.urljoin(target_url, download_frag.replace(' ', '%20'))
            print(f"Attempting to download: {download_url}")
            time.sleep(1)
            try:
                response = requests.get(download_url)
                print(f"HTTP status: {response.status_code}")
                content_type = response.headers.get('Content-Type', '')
                print(f"Content-Type: {content_type}")

                # Check if the response is a PDF
                if 200 <= response.status_code < 300 and 'application/pdf' in content_type:
                    with open(file_name, mode="wb") as f:
                        f.write(response.content)
                    print(f"Saved: {file_name}")
                else:
                    print(f"Download failed or not a PDF for {download_url}:")
                    # Print the first 200 characters of the response for debugging
                    print(response.text[:200])
            except Exception as e:
                print(f"Request error for {download_url}: {e}")

# driver.quit()  # Not called, browser stays open


