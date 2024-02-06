import requests
import re
import time
from bs4 import BeautifulSoup

num = int(input("请输入要爬取的页数："))

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
with open("game_price.txt", "w", encoding='utf-8') as f:
    for page_number in range(1, num):
        time.sleep(1)# 防止爬虫被拦截
        url = f"https://store.steampowered.com/search/?specials=1&page={page_number}"
        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError:
            print("[Error] 403 Retrying...")
            continue
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        # 获取游戏列表
        games_info = soup.find(id="search_resultsRows")
        games_a = games_info.find_all("a")
        for i in range(len(games_a)):
            try:
                game_name = games_a[i].find("span", attrs={"class": "title"}).text
                game_price = games_a[i].find("div", attrs={"class": "discount_final_price"}).text
                game_sale = games_a[i].find("div", attrs={"class": "discount_pct"}).text
            except AttributeError:
                print("[Error] 未爬取到信息.Retrying...")
                continue
            else:
                f.write(f"{game_name},{game_sale},{game_price}\n")
        print(f"Successfully saved the Page {page_number} games price")
print("All done!")