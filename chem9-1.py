# coding: UTF-8

import os
import urllib.parse
from selenium import webdriver
from bs4 import BeautifulSoup
import requests

# Ensure 'pdf' directory exists
os.makedirs("chem9-1", exist_ok=True)

target_url = "https://unit.aist.go.jp/riss/crm/mainmenu/1-1-3.html"
base_url = "https://unit.aist.go.jp/riss/crm/mainmenu/"

try:
    driver = webdriver.Chrome()
    driver.get(target_url)
except Exception as e:
    print('WEBアクセスに失敗しました:', e)
else:
    print('WEBアクセスに成功しました')
    source = driver.page_source
    soup = BeautifulSoup(source, "lxml")
    pdf_links = soup.select("table a")
    
    for pdf_link in pdf_links:
        href = pdf_link.get("href")
        if not href:
            continue
        # Proper URL join
        download_url = urllib.parse.urljoin(base_url, href)
        print(download_url)
        
        file_name = "chem9-1/" + download_url.split("/")[-1]
        print(file_name)
        
        if file_name.endswith(".pdf"):
            try:
                response = requests.get(download_url)
                response.raise_for_status()
                with open(file_name, mode="wb") as f:
                    f.write(response.content)
                print("保存しました")
            except Exception as err:
                print(err)
    driver.quit()

