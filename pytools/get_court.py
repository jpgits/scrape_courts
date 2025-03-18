from time import sleep
from pprint import pprint

from requests import Session
from bs4 import BeautifulSoup


# 最高裁判所 判例集 検索結果
# https://www.courts.go.jp/app/hanrei_jp/recentlist2
# 下級裁判所 裁判例速報 検索結果
# https://www.courts.go.jp/app/hanrei_jp/recentlist4
# 知的財産 裁判例集 検索結果
# https://www.courts.go.jp/app/hanrei_jp/recentlist4

session = Session()

session.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
})


def recent_court():
    # debug
    # with open("index.html", "r") as file:
    #     r = file.read()

    courts = []

    for page in range(1, 3):

        r = session.get(
            "https://www.courts.go.jp/app/hanrei_jp/recentlist2?page=1&filter%5Brecent%5D=true",
            params={
                "page": page,
                "filter[recent": True
            }
        )

        soup = BeautifulSoup(r.text, "html.parser")

        _ = soup.find("div", class_="module-sub-page-parts-table module-search-page-table-parts-result").find_all("tr")

        courts.extend([__.find("a")["href"] for __ in _])

    return courts


def detail(url): 
# {'裁判例集': '最高裁判所判例集',
#  '事件名': '損害賠償請求事件',
#  '事件番号': '令和5(受)961',
#  '全文': [{'全文': 'https://www.courts.go.jp/app/files/hanrei_jp/869/093869_hanrei.pdf'}],
#  '判例集等巻・号・頁': '',
#  '判示事項': '都道府県警察所属の警部補が自殺した場合において、当該都道府県警察を置く都道府県が安全配慮義務違反に基づく損害賠償責任を負うとされた事例',
#  '原審事件番号': '令和4(ネ)264',
#  '原審裁判年月日': '令和5年2月17日',
#  '原審裁判所名': '広島高等裁判所',
#  '参照法条': '',
#  '法廷名': '最高裁判所第二小法廷',
#  '結果': '棄却',
#  '裁判年月日': '令和7年3月7日',
#  '裁判種別': '判決',
#  '裁判要旨': ''
# }


    # debug
    # with open("detail.html", "r") as file:
    #     r = file.read()

    r = session.get(f"https://www.courts.go.jp/{url}")

    court_data = {}
        
    soup = BeautifulSoup(r.text, "html.parser")

    court_data["裁判例集"] = soup.find("div", "module-sub-page-parts-default-2").find("h4").text

    _ = soup.find_all("div", class_="module-search-page-table-parts-result module-search-page-table-parts-result-detail")

    for a in _:
        for b in a.find_all("dl"):
            name = b.find("dt").text
            if "全文" in name:
                value = [{__.find("a").text: "https://www.courts.go.jp" + __.find("a")["href"]} for __ in b.find_all("li")]
            else:
                value = "".join(b.find("p").text.split())

            court_data[name] = value

    return court_data

if __name__ == "__main__":
    for _ in recent_court():
        pprint(detail(_))
        sleep(5)
        
