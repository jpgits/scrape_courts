from scraper import CourtScraper
from models import Judgment

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
