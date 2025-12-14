# coding: UTF-8

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import requests
import urllib.parse

# Reference URL
target_url = "http://www.cerij.or.jp/evaluation_document/hazard_assessment_report_03.html"
base_url = "http://www.cerij.or.jp"

# Ensure the 'chem22-1' directory exists
os.makedirs("chem22-1", exist_ok=True)

try:
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(target_url)
except Exception as e:
    print('WEBアクセスに失敗しました:', e)
else:
    print('WEBアクセスに成功しました')
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")
    pdf_links = soup.select("table a")

    for pdf_link in pdf_links:
        download_url = pdf_link.get("href")
        print("Raw href:", download_url)

        if not download_url:
            continue

        # Build the full URL
        if download_url.startswith("http"):
            full_url = download_url
        elif download_url.startswith("/"):
            full_url = base_url + download_url
        else:
            full_url = urllib.parse.urljoin(target_url, download_url)

        file_name = "chem22-1/" + full_url.split("/")[-1]
        print("Saving as:", file_name)

        # Only download PDF files
        if not file_name.lower().endswith(".pdf"):
            continue

        try:
            response = requests.get(full_url)
            print("Status code:", response.status_code)
            if 200 <= response.status_code < 300:
                with open(file_name, mode="wb") as f:
                    f.write(response.content)
                print("保存しました")
            else:
                print("Failed to download:", full_url, "Status:", response.status_code)
        except Exception as err:
            print("Error downloading", full_url, ":", err)
    driver.quit()
