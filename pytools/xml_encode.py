from bs4 import BeautifulSoup

with open("output.xml", "r", encoding="utf-8") as file:
    content = file.read()

soup = BeautifulSoup(content, "xml")
text_data = soup.get_text(separator="\n")
