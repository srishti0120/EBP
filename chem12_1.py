import os
import time
import requests
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Settings
project_name = 'chem12'
main_url = 'http://apps.who.int/pesticide-residues-jmpr-database/Home/Range/All'
pdf_folder = r'C:\Users\srish\OneDrive\Desktop\internship\chem12\pdf'
download_timeout = 15

def print_line():
    print('--------------------------------')

def get_domain(url):
    return '{uri.scheme}://{uri.netloc}'.format(uri=urllib.parse.urlparse(url))

def make_url_absolute(link, current_url):
    href = link.get('href')
    if href is None:
        return None
    if href.startswith('http'):
        return href
    else:
        return urllib.parse.urljoin(get_domain(current_url), href)

def get_links(html, selector):
    soup = BeautifulSoup(html, 'lxml')
    return soup.select(selector)

def safe_filename(name):
    # Remove illegal characters from filename
    keep = (' ', '_', '.', '-')
    return ''.join(c for c in name if c.isalnum() or c in keep).strip()

def download_file(url, folder, link_text=None):
    try:
        # Get the file name from the URL
        file_name = os.path.basename(urllib.parse.urlparse(url).path)
        if not file_name:
            file_name = "document"
        file_name = safe_filename(file_name)
        # If the file name has no extension, use the link text as a hint
        if '.' not in file_name and link_text:
            link_text = safe_filename(link_text)
            file_name = f"{file_name}_{link_text}"
        # Download the file
        response = requests.get(url, timeout=download_timeout, stream=True)
        response.raise_for_status()
        # Determine the file extension based on Content-Type or URL
        content_type = response.headers.get('content-type', '').lower()
        if 'pdf' in content_type or url.lower().endswith('.pdf'):
            ext = '.pdf'
        elif 'html' in content_type or url.lower().endswith(('.htm', '.html')):
            ext = '.html'
        else:
            ext = '.bin'  # Unknown type
        # Ensure the file name has the correct extension
        if not file_name.lower().endswith(ext):
            file_name += ext
        file_path = os.path.join(folder, file_name)
        # Save the file
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Downloaded: {file_path}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def get_pesticide_links(driver):
    driver.get(main_url)
    time.sleep(5)  # Wait for dynamic content
    source = driver.page_source
    # Try multiple selectors to find pesticide links
    for selector in ['.multicolumn3 a', '.multicolumn3 li a', '.list-group a', 'ul li a', 'a[href*="/Chemical/"]']:
        links = get_links(source, selector)
        if links:
            return links
    return []

def download_files_for_pesticide(driver, pesticide_link):
    pesticide_name = pesticide_link.text.strip().replace('/', '').replace('\\', '')
    pesticide_url = make_url_absolute(pesticide_link, driver.current_url)
    if not pesticide_url:
        print(f"Invalid URL for {pesticide_name}")
        return
    folder = os.path.join(pdf_folder, safe_filename(pesticide_name))
    os.makedirs(folder, exist_ok=True)
    driver.get(pesticide_url)
    time.sleep(3)  # Wait for page to load
    source = driver.page_source
    # Find all relevant links (PDF and HTML)
    file_links = get_links(source, 'a[href$=".pdf"], a[href$=".htm"], a[href$=".html"], table a, .table a')
    if not file_links:
        print(f"No files found for {pesticide_name}")
        return
    print(f"Found {len(file_links)} files for {pesticide_name}")
    for link in file_links:
        file_url = make_url_absolute(link, driver.current_url)
        if file_url:
            download_file(file_url, folder, link.text)

def main():
    os.makedirs(pdf_folder, exist_ok=True)
    driver = webdriver.Chrome()
    try:
        pesticide_links = get_pesticide_links(driver)
        if not pesticide_links:
            print("No pesticide links found. Check the page structure.")
            return
        print(f"Found {len(pesticide_links)} pesticides.")
        for link in pesticide_links:
            print_line()
            print(f"\nProcessing: {link.text.strip()}")
            download_files_for_pesticide(driver, link)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print_line()
    print(f"\nTotal time: {round(end_time-start_time,1)} seconds")