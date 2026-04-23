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
    
    try:
        Data = requests.get(url, headers=headers)
        Data.encoding = "utf-8"
        sp = BeautifulSoup(Data.text, "html.parser")
        
        html_info = """
        <html>
        <head><meta charset="utf-8"><title>即將上映電影</title></head>
        <body style="font-family: sans-serif; padding: 20px;">
            <h2>🎥 即將上映電影清單</h2>
            <ul style="line-height: 1.8;">
        """
        
        movie_links = sp.find_all("a")
        
        seen_movies = set() # 用來記錄已經抓過的電影，避免重複
        movie_count = 0
        
        for a_tag in movie_links:
            href = a_tag.get("href", "")
            title = a_tag.text.strip()
            
            if title and href.startswith("/movie/") and len(href) > 15:
                # 確保不重複抓取，且排除抓到隱藏圖片的狀況
                if title not in seen_movies and "<img" not in str(a_tag):
                    seen_movies.add(title)
                    full_url = "http://www.atmovies.com.tw" + href
                    html_info += f'<li><a href="{full_url}" target="_blank">{title}</a></li>\n'
                    movie_count += 1
                    
        # 防呆提示
        if movie_count == 0:
            html_info += '<li style="color:red;">哎呀！沒有抓到電影，開眼電影網可能阻擋了連線。</li>'
            
        html_info += """
            </ul>
            <br>
            <a href="/" style="color: gray;">返回首頁</a>
        </body>
        </html>
        """
        return html_info
        
    except Exception as e:
        return f"發生錯誤：{str(e)}"

if __name__ == '__main__':
    app.run()
