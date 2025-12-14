import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import requests
import urllib.parse

# Ensure 'pdf' folder exists
os.makedirs("chem9", exist_ok=True)

target_url = "https://unit.aist.go.jp/riss/crm/mainmenu/1-1-3.html"

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
    soup = BeautifulSoup(source, "lxml")
    pdf_links = soup.select("table a")

    for pdf_link in pdf_links:
        href = pdf_link.get("href")
        if not href:
            continue

        # Properly join base and relative URLs
        download_url = urllib.parse.urljoin(target_url, href)
        print(download_url)

        file_name = "chem9/" + download_url.split("/")[-1]
        print(file_name)

        # Only download PDF files
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

