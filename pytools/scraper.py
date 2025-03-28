from typing import List
import requests
from bs4 import BeautifulSoup
from models import Judgment

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
