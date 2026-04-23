from flask import Flask
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# --- 首頁 ---
@app.route('/')
def home():
    return """
    <html>
    <head><meta charset="utf-8"><title>Vercel 電影查詢</title></head>
    <body style="font-family: sans-serif; padding: 20px;">
        <h1>我的 Vercel 電影網</h1>
        <a href="/search" style="color: blue; text-decoration: underline; font-size: 1.2rem; font-weight: bold;">
            [查詢即將上映電影]
        </a>
    </body>
    </html>
    """

# --- 查詢頁面 ---
@app.route('/search')
def search_movies():
    url = "http://www.atmovies.com.tw/movie/next/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    Data = requests.get(url, headers=headers)
    Data.encoding = "utf-8"
    sp = BeautifulSoup(Data.text, "html.parser")
    
    result = sp.select(".filmListAllX li")
    if len(result) == 0:
        result = sp.select(".filmListAll li")
        
    html_info = """
    <html>
    <head><meta charset="utf-8"><title>即將上映電影</title></head>
    <body style="font-family: sans-serif; padding: 20px;">
        <h2>🎥 即將上映電影清單</h2>
        <ul style="line-height: 1.8;">
    """
    
    if len(result) == 0:
        html_info += '<li style="color:red;">哎呀！沒有抓到電影，可能是網站原始碼改版了。</li>'
        
    for item in result:
        a_tag = item.find("a")
        if a_tag and a_tag.text.strip():
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
