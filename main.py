from typing import List, Optional, Dict
from dataclasses import dataclass, field
import requests
from bs4 import BeautifulSoup

@dataclass
class Judgment:
    裁判例集: str
    裁判種別: Optional[str] = None
    法廷名: Optional[str] = None
    裁判年月日: Optional[str] = None
    事件名: Optional[str] = None
    事件番号: Optional[str] = None
    判示事項: Optional[str] = None
    裁判要旨: Optional[str] = None
    結果: Optional[str] = None
    原審裁判所名: Optional[str] = None
    原審裁判年月日: Optional[str] = None
    原審事件番号: Optional[str] = None
    判例集等巻号頁: Optional[str] = None
    参照法条: Optional[str] = None
    全文: List[Dict[str, str]] = field(default_factory=list)

class CourtScraper:
    BASE_URL = "https://www.courts.go.jp"

    def __init__(self, court_type: str = "recentlist2", max_pages: int = 2):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/134.0.0.0 Safari/537.36"
            )
        })
        self.court_type = court_type
        self.max_pages = max_pages

    def get_recent_judgment_urls(self) -> List[str]:
        urls = []
        for page in range(1, self.max_pages + 1):
            response = self.session.get(
                f"{self.BASE_URL}/app/hanrei_jp/{self.court_type}",
                params={"page": page, "filter[recent]": True}
            )
            soup = BeautifulSoup(response.text, "html.parser")
            rows = soup.select("div.module-sub-page-parts-table tr")
            urls.extend([
                row.find("a")["href"]
                for row in rows
                if row.find("a")
            ])
        return urls

    def get_judgment_detail(self, url: str) -> Judgment:
        response = self.session.get(f"{self.BASE_URL}{url}")
        soup = BeautifulSoup(response.text, "html.parser")
        court_data = {}

        title_block = soup.find("div", class_="module-sub-page-parts-default-2")
        if title_block:
            court_data["裁判例集"] = title_block.find("h4").text.strip()

        detail_blocks = soup.select("div.module-search-page-table-parts-result-detail")
        for block in detail_blocks:
            for dl in block.find_all("dl"):
                name = dl.find("dt").text.strip()
                if name == "判例集等巻・号・頁":
                    name = "判例集等巻号頁"
                if "全文" in name:
                    value = [
                        {
                            a_tag.text.strip(): f"{self.BASE_URL}{a_tag['href']}"
                        }
                        for a_tag in dl.find_all("a")
                    ]
                else:
                    value = "".join(dl.find("p").text.split())
                court_data[name] = value
        return Judgment(**court_data)

def extract_text_from_xml(file_path="output.xml") -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    soup = BeautifulSoup(content, "xml")
    return soup.get_text(separator="\n")

def main():
    judgment_fields = list(Judgment.__annotations__.keys())
    print("Judgmentのフィールド:", judgment_fields)

    取得器 = CourtScraper()
    判例群 = []

    for 判例url in 取得器.get_recent_judgment_urls():
        判例 = 取得器.get_judgment_detail(判例url)
        判例群.append(判例)

    for 判例 in 判例群:
        print("-" * 50)
        for 項目 in judgment_fields:
            if hasattr(判例, 項目):
                print(f"{項目}: {getattr(判例, 項目)}")

if __name__ == "__main__":
    main()
