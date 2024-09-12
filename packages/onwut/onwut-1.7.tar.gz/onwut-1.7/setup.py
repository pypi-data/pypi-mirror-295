# setup.py
from setuptools import setup, find_packages

setup(
    name="onwut",
    version="1.7",  # バージョンを更新
    packages=find_packages(),
    include_package_data=True,  # データファイルを含めるために必要
    package_data={
        'onwut': ['onwut_data.db'],  # パッケージに含めるデータファイルを指定
    },
    install_requires=[
        "requests",
        "beautifulsoup4",
        "PyPDF2",
        "lxml",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="onwut は、経済産業省のウェブサイトからPDFレポートをスクレイピングして処理するためのPythonライブラリです。",
    url="https://github.com/yourusername/onwut",
)
