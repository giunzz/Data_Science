from playwright.sync_api import sync_playwright
from pathlib import Path
from collections import namedtuple
from bs4 import BeautifulSoup
import pandas as pd

# Cấu trúc dữ liệu Anime
Anime = namedtuple("Anime", ["title", "url", "view", "extra", "eps"])

def download_file(query, page_from, page_to, export_loc):
    # Tạo thư mục lưu file nếu chưa có
    Path(export_loc).mkdir(exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()

        for page_num in range(page_from, page_to + 1):
            # Trang đầu tiên có format khác
            if page_num == 1:
                url = f"https://animevietsub.show/the-loai/{query}/"
            else:
                url = f"https://animevietsub.show/the-loai/{query}/trang-{page_num}.html"

            print("Process:", url)
            page.goto(url)
            page.wait_for_load_state("domcontentloaded")

            # Lưu file HTML
            filename = Path(export_loc) / f"{query}_page{page_num}.html"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(page.content())

            print(f"✅ Saved file: {filename}")

        browser.close()

def extract_anime_summary(article_element):
    title = article_element.find("h2", class_="Title").text.strip()
    url = article_element.a["href"]
    view = article_element.find("span", class_="Year").text.strip() if article_element.find("span", class_="Year") else None
    extra = article_element.find("div", class_="anime-extras").text.strip() if article_element.find("div", class_="anime-extras") else None
    eps = article_element.find("span", class_="mli-eps").text.strip() if article_element.find("span", class_="mli-eps") else None

    return Anime(title=title, url=url, view=view, extra=extra, eps=eps)

# def get_last_page(query, base_url="https://animevietsub.show"):          # tu dong lay so trang cuoi cung
#     with sync_playwright() as playwright:
#         browser = playwright.chromium.launch(headless=False)
#         page = browser.new_page()
#         url = f"{base_url}/the-loai/{query}/"
#         page.goto(url)
#         page.wait_for_load_state("domcontentloaded")

#         soup = BeautifulSoup(page.content(), "html.parser")
#         browser.close()

#     # Tìm các số trang trong phân trang
#     pagination = soup.select("ul.pagination a")
#     pages = []
#     for p in pagination:
#         try:
#             pages.append(int(p.text.strip()))
#         except:
#             pass

#     return max(pages) if pages else 1

if __name__ == "__main__":
    query = "hanh-dong"
    source_dir = Path("C:/Users/ASUS/Documents/GitHub/Data_sceince_ute/Data_Science/Project/Bình/export")
    source_dir.mkdir(exist_ok=True)
    source_csv = Path("C:/Users/ASUS/Documents/GitHub/Data_sceince_ute/Data_Science/Project/Bình/Data")
    source_csv.mkdir(exist_ok=True)

    #last_page = get_last_page(query)
    #print(f"Sẽ quét tới trang cuối cùng: {last_page}")

    # 👉 Cho người dùng nhập số trang muốn cào
    page_to = int(input("Nhập số trang muốn cào: "))
    download_file(query=query, page_from=1, page_to=page_to, export_loc=source_dir)

    record = []

    # Đọc tất cả file html đã tải
    for html_file in source_dir.glob(f"{query}_page*.html"):
        print(f"Processing file {html_file}")
        with open(html_file, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        # Tìm tất cả anime trong trang
        articles = soup.find_all("article", class_="TPost")
        for article in articles:
            anime_summary = extract_anime_summary(article)
            record.append(anime_summary)

    # Xuất ra CSV
    df = pd.DataFrame(record)
    df.to_csv(source_csv /f"danh_sach_phim_{query}.csv", index=False, encoding="utf-8-sig")
    print(f"✅ File saved: danh_sach_phim_{query}.csv")
