from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
from urllib.parse import urljoin
import csv
import time
import random

BASE = "http://books.toscrape.com/"

def extract_books_from_page(page):
    """Trả về list of dicts: [{'title':..., 'price':..., 'link':...}, ...]"""
    books = []
    page.wait_for_selector(".product_pod", timeout=10000)
    pods = page.query_selector_all(".product_pod")
    for pod in pods:
        a = pod.query_selector("h3 a")
        title = a.get_attribute("title").strip() if a else ""
        href = a.get_attribute("href") if a else ""
        link = urljoin(BASE, href)
        price_el = pod.query_selector(".price_color")
        price = price_el.inner_text().strip() if price_el else ""
        avail_el = pod.query_selector(".availability")
        availability = avail_el.inner_text().strip() if avail_el else ""
        books.append({
            "title": title,
            "price": price,
            "link": link,
            "availability": " ".join(availability.split())
        })
    return books

def save_csv(rows, path="books.csv"):
    keys = ["title", "price", "link", "availability"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

def scrape_all_pages(
    max_pages=None,
    headless=True,
    slow_mo=0,
    browser_name="chromium"  
):
    all_books = []
    with sync_playwright() as p:
        # Chọn engine
        if browser_name == "firefox":
            browser = p.firefox.launch(headless=headless, slow_mo=slow_mo)
        elif browser_name == "webkit":
            browser = p.webkit.launch(headless=headless, slow_mo=slow_mo)
        else:
            browser = p.chromium.launch(headless=headless, slow_mo=slow_mo)

        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )
        page = context.new_page()
        page.goto(BASE, wait_until="domcontentloaded")
        page_number = 1

        while True:
            try:
                print(f"[INFO] Đang xử lý trang #{page_number}: {page.url}")
                books = extract_books_from_page(page)
                print(f"[INFO] Tìm thấy {len(books)} sản phẩm trên trang này.")
                all_books.extend(books)

                if max_pages is not None and page_number >= max_pages:
                    print("[INFO] Đã đạt max_pages, dừng lại.")
                    break

                next_a = page.query_selector(".next a")
                if not next_a:
                    print("[INFO] Không có trang tiếp theo — kết thúc.")
                    break

                time.sleep(random.uniform(0.6, 1.8))
                next_a.click()
                page.wait_for_load_state("domcontentloaded", timeout=10000)
                time.sleep(random.uniform(0.2, 0.8))
                page_number += 1

            except PWTimeout as e:
                print(f"[WARN] Timeout trên trang {page.url}: {e}. Thử reload.")
                try:
                    page.reload(wait_until="domcontentloaded", timeout=10000)
                except Exception:
                    break
            except Exception as e:
                print(f"[ERROR] Lỗi không mong muốn: {e}")
                break

        browser.close()
    return all_books

if __name__ == "__main__":
        rows = scrape_all_pages(max_pages=None, headless=False, slow_mo=3000, browser_name="firefox")
        print(f"[DONE] Tổng sản phẩm thu thập: {len(rows)}")
        save_csv(rows, "C:\\Users\\ASUS\\Documents\\GitHub\\Data_sceince_ute\\Data_Science\\Project\\Dung\\store.csv")
        print("[DONE] Lưu file store.csv")
