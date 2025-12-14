# coding: UTF-8

import os
import urllib.parse
from selenium import webdriver
from bs4 import BeautifulSoup
import requests

# Ensure 'pdf' directory exists
os.makedirs("chem22-2", exist_ok=True)

target_url = "http://www.cerij.or.jp/evaluation_document/Chemical_hazard_data_list_04.html"
target_url2 = "http://www.cerij.or.jp/evaluation_document/"

try:
    driver = webdriver.Chrome()
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
        print(download_url)
        
        if not download_url:
            continue

        file_name = "chem22-2/" + download_url.split("/")[-1]
        print(file_name)

        # Build the full URL safely
        full_url = urllib.parse.urljoin(target_url2, download_url)
        print("Downloading from:", full_url)

        # Download and save the file
        try:
            response = requests.get(full_url)
            print(response.status_code)
            if 200 <= response.status_code < 300:
                with open(file_name, mode="wb") as f:
                    f.write(response.content)
                print("保存しました")
            else:
                print("Download failed:", response.status_code)
        except Exception as err:
            print("Error downloading:", err)
    driver.quit()
