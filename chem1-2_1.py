import os
import requests
import openpyxl
import urllib
import time
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

project_name = 'chem1-2'
target_url = 'http://www.env.go.jp/chemi/communication/factsheet.html'
download_url = 'http://www2.env.go.jp/chemi/prtr/factsheet/factsheet'
driver_wait_time = 30.0
current_path = os.path.abspath('.')
pdf_folder_path = os.path.join(current_path, project_name, 'pdf')
log_path = os.path.join(current_path, project_name, 'log')
html_parser = 'lxml'
sheet_area = 'A2:A34'

def print_line():
    print('--------------------------------')

def get_domain(target_url):
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=urllib.parse.urlparse(target_url))
    return domain

def form_domain(classification_link, current_url):
    classification_url = classification_link.get('href')
    
    if not classification_url:
        print("⚠ Skipping link without href.")
        return None
    
    if classification_url.startswith('http'):
        return classification_url
    
    global_url = download_url + classification_url.lstrip('.')
    return global_url

def get_links(source, selector):
    soup = BeautifulSoup(source, html_parser)
    return soup.select(selector)

def get_target_xls_data():
    try:
        wb = openpyxl.load_workbook('casno for test.xlsx')
        sheet = wb['Sheet1']
        cells = []
        for row in sheet[sheet_area]:
            for cell in row:
                if cell.value:
                    cells.append(str(cell.value).strip())
        return cells
    except FileNotFoundError as err:
        print(f'Excel processing failed ({err})')
        write_log(f'Excel processing failed ({err})')
        return []

def write_log(log_text=''):
    current_date = datetime.datetime.now()
    log_date = current_date.strftime('%Y_%m_%d %H_%M_%S')
    file_name = f'{project_name}_{current_date.strftime("%Y_%m_%d")}.log'
    os.makedirs(log_path, exist_ok=True)
    with open(os.path.join(log_path, file_name), 'a', encoding='utf-8') as f:
        f.write(f'{log_date} : {log_text}\n')

def download_pdf(driver, pdf_link, cas_no):
    os.makedirs(pdf_folder_path, exist_ok=True)
    pdf_url = form_domain(pdf_link, driver.current_url)
    if not pdf_url:
        return
    
    print("PDF URL:", pdf_url)
    pdf_name = os.path.join(pdf_folder_path, pdf_url.split("/")[-1])
    try:
        response = requests.get(pdf_url)
        print("Status code:", response.status_code)
        if 200 <= response.status_code < 300:
            with open(pdf_name, "wb") as f:
                f.write(response.content)
            print("○ File saved:", pdf_name)
        else:
            print("× Download failed:", pdf_url)
            write_log(f'× File download failed - {cas_no}: {pdf_name}, {response.status_code}')
    except Exception as e:
        print("× Exception during PDF download:", e)
        write_log(f'× Exception during PDF download - {cas_no}: {pdf_name}, {e}')

def download_site(driver, site_link, cas_no):
    print_line()
    site_url = form_domain(site_link, driver.current_url)
    if not site_url:
        return
    
    print("Site URL:", site_url)
    driver.get(site_url)
    time.sleep(2)
    source = driver.page_source
    with open(f"debug_{cas_no}.html", "w", encoding="utf-8") as f:
        f.write(source)
    pdf_links = get_links(source, 'a[href$=".pdf"]')
    print(f"Found {len(pdf_links)} PDF links.")
    if not pdf_links:
        print(f"No PDF links found for {cas_no}. Check debug_{cas_no}.html for details.")
        write_log(f'No PDF links found - {cas_no}')
    for pdf_link in pdf_links:
        download_pdf(driver, pdf_link, cas_no)

def material_parsing(driver, cas_no):
    print_line()
    print('\n■ Parsing chemical substance page\n')
    driver.switch_to.default_content()
    driver.switch_to.frame('main')
    source = driver.page_source
    time.sleep(2)
    site_links = get_links(source, 'td.datas a')
    print(f"Found {len(site_links)} site links.")
    if not site_links:
        print('× No data found')
        write_log(f'× No file - {cas_no}')
    else:
        for site_link in site_links:
            download_site(driver, site_link, cas_no)

def search_parsing(driver, cas_no):
    print_line()
    print(f'\n■ Parsing page for {cas_no}\n')
    if cas_no and cas_no.strip():
        cas_no = cas_no.strip()
        try:
            driver.get(target_url)
            time.sleep(2)
            os.makedirs(pdf_folder_path, exist_ok=True)

            driver.switch_to.frame('menu')
            WebDriverWait(driver, driver_wait_time).until(EC.presence_of_element_located((By.ID, 'CAS1')))
            driver.find_element(By.ID, 'CAS1').clear()
            driver.find_element(By.ID, 'CAS1').send_keys(cas_no)
            print('Text input complete')
            time.sleep(1)
            driver.find_element(By.NAME, 'f_submit').click()
            time.sleep(2)

        except TimeoutException:
            print(f'Search timeout - {cas_no}')
            write_log(f'Search timeout - {cas_no}')
            return
        except Exception as err:
            print(f'No search result - {cas_no} ({err})')
            write_log(f'No search result - {cas_no} ({err})')
            return

        material_parsing(driver, cas_no)

def start_parsing(driver):
    print_line()
    print('\n[Parsing chemical substance search page]\n')
    cas_no_list = get_target_xls_data()
    for cas_no in cas_no_list:
        search_parsing(driver, cas_no)

if __name__ == "__main__":
    start_time = time.time()
    try:
        os.makedirs(pdf_folder_path, exist_ok=True)
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        prefs = {'download.default_directory': pdf_folder_path}
        chrome_options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(target_url)
        start_parsing(driver)
    except KeyboardInterrupt:
        print('\nProcess interrupted\n')
    finally:
        driver.quit()
        end_time = time.time()
        print_line()
        print(f'\nProcessing time: {round(end_time - start_time, 1)} seconds')
