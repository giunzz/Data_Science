import os, re, csv, time, datetime
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

BASE = "https://viasm.edu.vn/hoat-dong-khoa-hoc/hoat-dong-trong-nam"
COLUMNS = ["title", "time", "location", "speaker", "url", "scraped_at"]
out = "C:\\Users\\ASUS\\Documents\\GitHub\\Data_sceince_ute\\Data_Science\\Project\\Dung\\viasm_events.xlsx"

def pick(label, text):
    m = re.search(rf"{label}\s*:\s*(.+)", text)
    return m.group(1).strip() if m else ""

def scrape_viasm(output=out, year_text=None, max_pages=None):
    existing = set()
    if os.path.exists(output):
        with open(output, newline="", encoding="utf-8") as rf:
            for r in csv.DictReader(rf):
                u = (r.get("url") or "").strip()
                if u: existing.add(u)

    with sync_playwright() as p, \
         open(output, "a", newline="", encoding="utf-8") as f:   
        writer = csv.writer(f)

        if f.tell() == 0:
            writer.writerow(COLUMNS)
            f.flush()

        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context()
        list_page = ctx.new_page()
        detail = ctx.new_page()

        print("Mở trang danh sách…")
        list_page.goto(BASE, wait_until="networkidle")
        time.sleep(0.3)

        # (tuỳ chọn) lọc theo năm, ví dụ: "Năm 2025"
        if year_text:
            y = list_page.get_by_text(year_text, exact=True)
            if y.count():
                y.first.click()
                list_page.wait_for_load_state("networkidle")

        page_idx = 1
        saved = 0

        while True:
            # lấy link sự kiện ở trang hiện tại
            anchors = list_page.locator('a[href^="/hdkh/"]').all()
            links, seen = [], set()
            for a in anchors:
                href = a.get_attribute("href")
                title = (a.text_content() or "").strip()
                if not href or not title or href in seen:
                    continue
                seen.add(href)
                links.append((urljoin(BASE, href), title))
                print(f"  - found: {title}")

            # duyệt từng trang chi tiết và GHI NGAY VÀO CSV
            for url, fallback_title in links:
                if url in existing:
                    continue
                try:
                    detail.goto(url, wait_until="networkidle")

                    # tiêu đề
                    d_title = ""
                    for sel in ("h1", "h2", "h3"):
                        loc = detail.locator(sel)
                        if loc.count():
                            d_title = (loc.first.text_content() or "").strip()
                            if d_title: break
                    title = d_title or fallback_title

                    body = detail.locator("body").inner_text()
                    time_range = pick("Thời gian", body)
                    location   = pick("Địa điểm", body)
                    speaker    = pick("Báo cáo viên", body)

                    row = [title, time_range, location, speaker, url,
                           datetime.datetime.now().isoformat(timespec="seconds")]

                    writer.writerow(row)   # ghi NGAY
                    f.flush()              # ĐẨY RA ĐĨA LIỀN (tránh phải đợi)
                    # Nếu muốn chắc chắn hơn nữa (chậm hơn): os.fsync(f.fileno())

                    existing.add(url)
                    saved += 1
                    print("    saved:", title)
                    time.sleep(0.15)
                except Exception as e:
                    print("    ! lỗi:", url, "-", e)

            # sang trang kế tiếp ("Sau")
            next_btn = list_page.locator('a:has-text("Sau")').first
            if not next_btn.is_visible() or (max_pages and page_idx >= max_pages):
                break
            curr = list_page.url
            next_btn.click()
            list_page.wait_for_load_state("networkidle")
            page_idx += 1
            if list_page.url == curr:
                break

        browser.close()
        print(f"Done. Appended {saved} rows to {output}")

if __name__ == "__main__":
    scrape_viasm()
