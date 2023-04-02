# scraping
Auto scraping program.

適当に作ったChromeのスクレイピング用プログラム。というかAI作るための虹ヱ口画像をpixivから自動で集めたかっただけ。
python 3.9.16
selenium 3.141.0
fake-useragent 1.1.3

↓directory
なんか適当なファイル--google_search.py
.                   ト-webdriver-chromedriver.exe
.                   ト-accounts-0から始まる番号(数字のみ)のファイル達-dir.txt (chromeのurlにchrome://versionって打ち込んで出てきた画面のプロフィールパスの最後の部分のみ記述。技術力がないだけ)
.                                                                  ト-download (無かったとしても自動生成できるようにする予定)-pixiv(自動生成してくれる)-"絵師の名前" (対象の絵師の画像保存するためのファイル。自動でHTMLから生成してくれる)-画像
