from flask import Flask
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
    <head>
        <meta charset="utf-8">
        <title>Vercel 電影查詢</title>
    </head>
    <body style="font-family: sans-serif; padding: 20px;">
        <h1>我的 Vercel 電影網</h1>
        <a href="/search" style="color: blue; text-decoration: underline; font-size: 1.2rem; font-weight: bold;">
            [查詢即將上映電影]
        </a>
    </body>
    </html>
    """
@app.route('/search')
def search_movies():
    # 執行爬蟲
    url = "http://www.atmovies.com.tw/movie/next/"
    Data = requests.get(url)
    Data.encoding = "utf-8"
    sp = BeautifulSoup(Data.text, "html.parser")
    result = sp.select(".filmListAllX li")
    
    html_info = """
    <html>
    <head><meta charset="utf-8"><title>即將上映電影</title></head>
    <body style="font-family: sans-serif; padding: 20px;">
        <h2>🎥 即將上映電影清單</h2>
        <ul style="line-height: 1.8;">
    """
    
    for item in result:
        a_tag = item.find("a")
        if a_tag and a_tag.text:
            title = a_tag.text.strip()
            href = "http://www.atmovies.com.tw" + a_tag.get("href")
            html_info += f'<li><a href="{href}" target="_blank">{title}</a></li>'
            
    html_info += """
        </ul>
        <br>
        <a href="/" style="color: gray;">返回首頁</a>
    </body>
    </html>
    """
    return html_info

if __name__ == '__main__':
    app.run()