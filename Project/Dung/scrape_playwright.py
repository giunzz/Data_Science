import re, csv, time
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

BASE = "https://viasm.edu.vn/hoat-dong-khoa-hoc/hoat-dong-trong-nam"

def pick(label, text): # lấy giá trị theo nhãn
    m = re.search(rf"{label}\s*:\s*(.+)", text)
    return m.group(1).strip() if m else ""


def scrape_viasm(output_csv="viasm_events.csv", year_text=None, max_pages=None):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context()
        list_page = ctx.new_page()
        detail = ctx.new_page()
        print("Mở trang danh sách...")
        with open(output_csv, "w", newline="", encoding="utf-8") as f:
            list_page.goto(BASE, wait_until="networkidle")
            time.sleep(1)
            if year_text:
                y = list_page.get_by_text(year_text, exact=True)
                if y.count():
                    y.first.click()
                    list_page.wait_for_load_state("networkidle")

            page_idx = 1
            while True:
                anchors = list_page.locator('a[href^="/hdkh/"]').all()
                links, seen = [], set()
                for a in anchors:
                    href = a.get_attribute("href")
                    title = (a.text_content() or "").strip()
                    print(f"  - {title} ({href})")
                    if not href or href in seen or not title:
                        continue
                    seen.add(href)
                    links.append((urljoin(BASE, href), title))

                # Mở từng trang chi tiết để lấy trường cấu trúc
                for url, fallback_title in links:
                    detail.goto(url, wait_until="networkidle")

                    # tiêu đề
                    d_title = ""
                    for sel in ("h1", "h2", "h3"):
                        loc = detail.locator(sel)
                        if loc.count():
                            d_title = (loc.first.text_content() or "").strip()
                            if d_title:
                                break
                    title = d_title or fallback_title

                    body = detail.locator("body").inner_text()
                    time_range = pick("Thời gian", body)
                    location   = pick("Địa điểm", body)
                    speaker    = pick("Báo cáo viên", body)

                    a = [title, time_range, location, speaker, url]
                    w = csv.writer(f)
                    w.writerow(a)
                curr = list_page.url
                next_btn = list_page.locator('a:has-text("Sau")').first
                if not next_btn.is_visible() or (max_pages and page_idx >= max_pages):
                    break
                next_btn.click()
                list_page.wait_for_load_state("networkidle")
                page_idx += 1
                if list_page.url == curr:  
                    break

        browser.close()

    
if __name__ == "__main__":
    scrape_viasm()
