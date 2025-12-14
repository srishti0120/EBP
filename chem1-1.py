# coding: UTF-8

from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import urllib

#ダウンロード先ドメイン
main_domain='chem1'

#参照URL
#target_urls= [{"http://www.env.go.jp/chemi/report/"+q+"/profile.html"} for q in
              #["h29-01","h28-01","h27-01","h26-01","h24-02","h24-01",\
               #"h23-01","h22-01","h21-01","h19-03","h18-12","h17-21"]]
target_urls=["http://www.env.go.jp/chemi/report/h29-01/profile.html",
             "http://www.env.go.jp/chemi/report/h28-01/profile.html",
             "http://www.env.go.jp/chemi/report/h27-01/profile.html",
             "http://www.env.go.jp/chemi/report/h26-01/profile.html",
             "http://www.env.go.jp/chemi/report/h24-02/profile.html",
             "http://www.env.go.jp/chemi/report/h24-01/profile.html",
             "http://www.env.go.jp/chemi/report/h23-01/profile.html",
             "http://www.env.go.jp/chemi/report/h22-01/profile.html",
             "http://www.env.go.jp/chemi/report/h21-01/profile.html",
             "http://www.env.go.jp/chemi/report/h19-03/profile.html",
             "http://www.env.go.jp/chemi/report/h18-12/profile.html",
             "http://www.env.go.jp/chemi/report/h17-21/profile.html"]

#URLの参照、データの出力
for target_url in target_urls:
    try:
        driver = webdriver.Chrome()
        driver.get(target_url)

    except:
        print('WEBアクセスに失敗しました')

    else:
        print('WEBアクセスに成功しました')
        source = driver.page_source
        soup = BeautifulSoup(source, "lxml")
        #抽出するPDFのクラス（属性）に注意！！
        #tableクラスのaに属している
        pdf_links = soup.select("ol a")

    for pdf_link in pdf_links:
        download_url = pdf_link.get("href")
        print(download_url)
        if download_url is not None:
            #ファイル名にはCAS番号を入れる
            file_name = main_domain+"/pdf/"+target_url.split('/')[-2]+'_'+download_url.split("/" or "-")[-1]
            print(file_name)

            #HTTPからのステータスコードを記録して、レスポンスの詳細を検知
            file = requests.get(target_url.split(".html")[0]+"/"+download_url.split("/" or "-")[-1])
            print(file.status_code)
            print(target_url.split(".html")[0]+"/"+download_url.split("/" or "-")[-1])

            if file.status_code>=200 and file.status_code<=299:
                file = urllib.request.urlopen(target_url.split(".html")[0]+"/"+download_url.split("/" or "-")[-1]).read()
                with open(file_name, mode="wb") as f:
                    f.write(file)
                    print("保存しました")
            else:
                err=requests.exceptions.RequestException
                print(err)
                continue
                driver.close()  