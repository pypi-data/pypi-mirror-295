import os
import psycopg2

def get_database_url():
    # 環境変数 ONWUT_DB_URL を使用。設定されていない場合はデフォルトの Heroku データベースURLを使用
    default_db_url = "postgres://udqo9u95b9ver2:p818daad9176bfa7f5c5cdd3e15d0993517d981a6cbbfa671f8399ccd3e80a2be@c3gtj1dt5vh48j.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d7qbcmbmrj0c0b"
    return os.getenv("ONWUT_DB_URL", default_db_url)

def fetch_reports(search_string=None, start_date=None, end_date=None, source=None, limit=10):
    db_url = get_database_url()

    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()

    query = "SELECT title, date, url, content, source FROM reports WHERE 1=1"
    params = []

    if search_string:
        query += " AND content LIKE %s"
        params.append(f"%{search_string}%")

    if start_date:
        query += " AND date >= %s"
        params.append(start_date)

    if end_date:
        query += " AND date <= %s"
        params.append(end_date)

    if source:
        query += " AND source = %s"
        params.append(source)

    query += " LIMIT %s"
    params.append(limit)

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    # フィールドごとの結果を辞書のリストとして返す
    return [
        {
            'title': row[0],
            'date': row[1],
            'url': row[2],
            'content': row[3][:30],  # 最初の30文字のみを含める
            'source': row[4]
        }
        for row in results
    ]

def fetch_time_series_data(title=None, start_date=None, end_date=None, source=None, limit=10):
    db_url = get_database_url()

    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()

    query = "SELECT date, value, title, source FROM time_series_data WHERE 1=1"
    params = []

    if title:
        query += " AND title LIKE %s"
        params.append(f"%{title}%")

    if start_date:
        query += " AND date >= %s"
        params.append(start_date)

    if end_date:
        query += " AND date <= %s"
        params.append(end_date)

    if source:
        query += " AND source = %s"
        params.append(source)

    query += " LIMIT %s"
    params.append(limit)

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    # フィールドごとの結果を辞書のリストとして返す
    return [
        {
            'date': row[0],
            'value': row[1],
            'title': row[2],
            'source': row[3]
        }
        for row in results
    ]

if __name__ == "__main__":
    # レポートデータを取得
    articles = fetch_reports(source="総務省")
    for article in articles:
        print(f"レポートタイトル: {article['title']}\n日付: {article['date']}\nURL: {article['url']}\nソース: {article['source']}\n内容: {article['content']}...\n")

    # 時系列データを取得
    time_series = fetch_time_series_data(title="株価", limit=5)
    for data in time_series:
        print(f"時系列データ - タイトル: {data['title']}\n日付: {data['date']}\n値: {data['value']}\nソース: {data['source']}\n")
