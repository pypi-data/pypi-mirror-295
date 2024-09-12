import requests
from bs4 import BeautifulSoup
import PyPDF2
import io
import sqlite3
import calendar
from datetime import datetime
import os
import re
import yfinance as yf

# データベースのパスを取得する関数
def get_database_path():
    home_dir = os.path.expanduser("~")
    db_dir = os.path.join(home_dir, ".onwut")
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, "onwut_data.db")
    return db_path

# PDFから内容を抽出する関数
def extract_pdf_content(pdf_url):
    response = requests.get(pdf_url)
    response.raise_for_status()
    pdf_data = io.BytesIO(response.content)
    reader = PyPDF2.PdfReader(pdf_data)
    content = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        content += page.extract_text()
    return content

# テーブルを作成する関数
def create_tables(cursor):
    # reportsテーブル
    cursor.execute('''CREATE TABLE IF NOT EXISTS reports
                      (title TEXT, date TEXT, url TEXT, content TEXT, source TEXT)''')

    # time_series_dataテーブル
    cursor.execute('''CREATE TABLE IF NOT EXISTS time_series_data
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      date TEXT, 
                      value REAL, 
                      title TEXT, 
                      source TEXT)''')

# データソース1をスクレイピングする関数（総務省: 消費者物価指数）
def scrape_data_source1(cursor):
    print("データソース1の取得を開始します。")
    main_url = 'https://www.e-stat.go.jp/stat-search/files?page=1&layout=datalist&toukei=00200573&tstat=000001150147&cycle=1&tclass1=000001150149&tclass2val=0'
    source1 = '総務省'
    response = requests.get(main_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'lxml')
    month_links = soup.select('a.stat-item_child')
    base_url = 'https://www.e-stat.go.jp'

    for link in month_links:
        month_url = base_url + link['href']
        month_response = requests.get(month_url)
        month_response.raise_for_status()
        month_soup = BeautifulSoup(month_response.content, 'lxml')

        publish_date_tag = month_soup.find('span', class_='stat-sp', string='公開（更新）日  ')
        if publish_date_tag:
            publish_date = publish_date_tag.find_next_sibling(string=True).strip()
        else:
            publish_date = "公開日が見つかりませんでした"

        pdf_link_tag = month_soup.find('a', class_='stat-dl_icon stat-icon_2 stat-icon_format js-dl stat-download_icon_left')
        if pdf_link_tag:
            pdf_url = base_url + pdf_link_tag['href']
            pdf_text = extract_pdf_content(pdf_url)
            title = f"{publish_date} 消費者物価指数"
            cursor.execute('''INSERT INTO reports (title, date, url, content, source)
                              VALUES (?, ?, ?, ?, ?)''', 
                              (title, publish_date, pdf_url, pdf_text, source1))
            print(f"データソース1のレポート取得: {title}, URL: {pdf_url}")
        else:
            print(f"日付: {publish_date}, No PDF found")

# データソース2をスクレイピングする関数（経済産業省: 鉱工業指数）
def scrape_data_source2(cursor):
    print("データソース2の取得を開始します。")
    main_url = 'https://www.meti.go.jp/statistics/tyo/iip/kako_press.html'
    source2 = '経済産業省'
    response = requests.get(main_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'lxml')

    reference_links = soup.find_all('a', href=lambda href: href and '/reference/' in href)
    base_url = 'https://www.meti.go.jp/statistics/tyo/iip/'

    for link in reference_links:
        pdf_url = base_url + link['href']
        match = re.search(r'b\d{4}_(\d{6})', link['href'])  # YYYYMM形式の6桁をキャプチャ
        if match:
            year_month = match.group(1)
            year = year_month[:4]
            month = year_month[4:]
            last_day = calendar.monthrange(int(year), int(month))[1]
            formatted_date = f"{year}-{month}-{last_day:02d}"
            pdf_text = extract_pdf_content(pdf_url)
            title = f"{formatted_date} 鉱工業指数"
            cursor.execute('''INSERT INTO reports (title, date, url, content, source)
                              VALUES (?, ?, ?, ?, ?)''', 
                              (title, formatted_date, pdf_url, pdf_text, source2))
            print(f"データソース2のレポート取得: {title}, URL: {pdf_url}")

# 株価データをスクレイピングする関数
def scrape_stock_data(cursor, ticker, source):
    print(f"{ticker}の株価データを取得中です。")
    stock = yf.Ticker(ticker)
    data = stock.history(period="1y")  # 過去1年のデータを取得

    for index, row in data.iterrows():
        date = str(index.date())
        value = row['Close']
        title = f"{ticker} 株価データ"
        cursor.execute('''INSERT INTO time_series_data (date, value, title, source) 
                          VALUES (?, ?, ?, ?)''', (date, value, title, source))
    print(f"{ticker}の株価データが保存されました。")

# データの全体取得を行う関数
def scrape_all_data():
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # テーブル作成
    create_tables(cursor)

    # データソース1の取得
    scrape_data_source1(cursor)

    # データソース2の取得
    scrape_data_source2(cursor)

    # 株価データの取得 (例: Apple)
    scrape_stock_data(cursor, "AAPL", "Yahoo Finance")

    conn.commit()
    conn.close()
    print(f"すべてのデータが取得され、データベースに保存されました: {db_path}")

if __name__ == "__main__":
    scrape_all_data()
