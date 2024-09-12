import os
import sqlite3
import psycopg2
from psycopg2 import OperationalError

def remove_null_bytes(text):
    """NULL文字を削除する関数"""
    if isinstance(text, str):
        return text.replace('\x00', '')
    return text

def get_heroku_database_url():
    """HerokuのデータベースURLを環境変数から取得"""
    return os.getenv('DATABASE_URL', 'postgres://udqo9u95b9ver2:p818daad9176bfa7f5c5cdd3e15d0993517d981a6cbbfa671f8399ccd3e80a2be@c3gtj1dt5vh48j.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d7qbcmbmrj0c0b')

def migrate_data():
    try:
        # ローカルのSQLiteデータベースに接続
        sqlite_conn = sqlite3.connect(os.path.expanduser('~/.onwut/onwut_data.db'))
        sqlite_cursor = sqlite_conn.cursor()

        # SQLiteデータベースに `reports` テーブルと `time_series_data` テーブルが存在しない場合は作成
        sqlite_cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                date TEXT,
                url TEXT,
                content TEXT,
                source TEXT
            );
        ''')

        sqlite_cursor.execute('''
            CREATE TABLE IF NOT EXISTS time_series_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                value REAL,
                title TEXT,
                source TEXT
            );
        ''')

        # SQLiteから `reports` のデータを取得
        sqlite_cursor.execute("SELECT title, date, url, content, source FROM reports")
        report_rows = sqlite_cursor.fetchall()

        # SQLiteから `time_series_data` のデータを取得
        sqlite_cursor.execute("SELECT date, value, title, source FROM time_series_data")
        time_series_rows = sqlite_cursor.fetchall()

        # HerokuのPostgreSQLデータベースに接続
        heroku_conn = psycopg2.connect(get_heroku_database_url())
        heroku_cursor = heroku_conn.cursor()

        # Heroku上の `reports` テーブルを作成（既に作成済みならスキップ）
        heroku_cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id SERIAL PRIMARY KEY,
                title TEXT,
                date TEXT,
                url TEXT,
                content TEXT,
                source TEXT
            );
        ''')

        # Heroku上の `time_series_data` テーブルを作成（既に作成済みならスキップ）
        heroku_cursor.execute('''
            CREATE TABLE IF NOT EXISTS time_series_data (
                id SERIAL PRIMARY KEY,
                date TEXT,
                value REAL,
                title TEXT,
                source TEXT
            );
        ''')

        # HerokuのPostgreSQLに `reports` データを挿入
        for row in report_rows:
            cleaned_row = tuple(remove_null_bytes(value) for value in row)
            heroku_cursor.execute(
                "INSERT INTO reports (title, date, url, content, source) VALUES (%s, %s, %s, %s, %s)",
                cleaned_row
            )

        # HerokuのPostgreSQLに `time_series_data` データを挿入
        for row in time_series_rows:
            cleaned_row = tuple(remove_null_bytes(value) for value in row)
            heroku_cursor.execute(
                "INSERT INTO time_series_data (date, value, title, source) VALUES (%s, %s, %s, %s)",
                cleaned_row
            )

        heroku_conn.commit()

        print(f"{len(report_rows)} 件の `reports` データがHerokuに移行されました。")
        print(f"{len(time_series_rows)} 件の `time_series_data` データがHerokuに移行されました。")

    except (sqlite3.OperationalError, OperationalError) as e:
        print(f"データベースエラーが発生しました: {e}")

    finally:
        # 接続を閉じる
        if 'heroku_conn' in locals():
            heroku_conn.close()
        if 'sqlite_conn' in locals():
            sqlite_conn.close()

if __name__ == "__main__":
    migrate_data()
