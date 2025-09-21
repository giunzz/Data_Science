from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
from urllib.parse import urljoin
import csv, time, random
from sub_work import RealtimeCsvWriter,load_existing_urls_quick

HOME_URL   = "https://www.topcv.vn/"
OUTPUT_CSV = r"C:\Users\ASUS\Documents\GitHub\Data_sceince_ute\Data_Science\Project\Dung\job.csv"

HEADLESS     = False          
SLOW_MO_MS   = 400
BROWSER_NAME = "firefox"      # "firefox" | "chromium" | "webkit"
MAX_PAGES    = 1              
SEARCH_KEY   = "Lập trình nhúng"

def save_csv(rows, path=OUTPUT_CSV):
    keys = ["job_title","company","salary","location","posted","job_url","company_url","source_page","summary"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow(r)

def human_delay(a=0.25, b=0.8):
    time.sleep(random.uniform(a, b))

def accept_cookies_if_any(page):
    for sel in [
        "text=Đồng ý", "text=Chấp nhận", "text=Cho phép", "text=Đồng ý tất cả",
        "text=Accept", "text=I agree", "text=Allow all"
    ]:
        try:
            btn = page.locator(sel)
            if btn.count() and btn.first.is_visible():
                btn.first.click()
                page.wait_for_timeout(300)
                break
        except:
            pass

def do_search(page, keyword: str) -> str:
    """Vào trang chủ → nhập keyword → click nút tìm → trả về URL trang kết quả."""
    page.goto(HOME_URL, wait_until="domcontentloaded")
    accept_cookies_if_any(page)
    # nhập từ khóa
    page.locator("input#keyword").fill(keyword)
    # click nút tìm
    page.locator("button.btn-search-job").click()
    page.wait_for_load_state("domcontentloaded")
    # đôi khi trang tải thêm — đợi nhẹ
    page.wait_for_timeout(500)
    return page.url

def collect_job_anchors(page):
    page.wait_for_load_state("domcontentloaded")
    candidate_selectors = [
        "[data-testid='job-item'] a[href*='/viec-lam/']",
        "[data-testid='job-card'] a[href*='/viec-lam/']",
        "a[href*='/viec-lam/'][target='_blank']",
        "a[href*='/viec-lam/']:not([href$='#'])"
    ]
    hrefs = []
    for sel in candidate_selectors:
        for a in page.locator(sel).all():
            href = a.get_attribute("href") or ""
            if "/viec-lam/" in href:
                if href.startswith("/"):
                    href = urljoin("https://www.topcv.vn/", href)
                if href.startswith("https://www.topcv.vn/") and href not in hrefs:
                    hrefs.append(href)
        if hrefs:
            break
    if not hrefs:
        page.mouse.wheel(0, 4000)
        page.wait_for_timeout(600)
        for sel in candidate_selectors:
            for a in page.locator(sel).all():
                href = a.get_attribute("href") or ""
                if "/viec-lam/" in href:
                    if href.startswith("/"):
                        href = urljoin("https://www.topcv.vn/", href)
                    if href.startswith("https://www.topcv.vn/") and href not in hrefs:
                        hrefs.append(href)
            if hrefs:
                break
    return hrefs

def extract_job_detail(detail_page):
    def safe_text(selectors):
        for sel in selectors:
            loc = detail_page.locator(sel)
            if loc.count() and loc.first.is_visible():
                t = loc.first.inner_text().strip()
                if t:
                    return " ".join(t.split())
        return ""

    title = safe_text(["h1", "h1.job-title", "[data-testid='job-title']"])
    company = safe_text(["a[href*='/cong-ty/']", ".company a", "[data-testid='company-name']"])
    salary = safe_text([
        "li:has(span:has-text('Mức lương')) span:not(:has-text('Mức lương'))",
        "span:has-text('Mức lương') + *",
        "[data-testid='job-salary']"
    ])
    location = safe_text([
        "li:has(span:has-text('Địa điểm')) span:not(:has-text('Địa điểm'))",
        "span:has-text('Địa điểm') + *",
        "[data-testid='job-location']"
    ])
    posted = safe_text([
        "li:has(span:has-text('Cập nhật'))",
        "li:has(span:has-text('Hạn nộp'))",
        "[data-testid='job-deadline']"
    ])
    company_url = ""
    comp_a = detail_page.locator("a[href*='/cong-ty/']").first
    if comp_a.count():
        href = comp_a.get_attribute("href") or ""
        company_url = urljoin("https://www.topcv.vn/", href) if href.startswith("/") else href

    summary = safe_text([
        "[data-testid='job-description']",
        ".job-description",
        "section:has(h2:has-text('Mô tả công việc'))",
        "section:has(h2:has-text('Chi tiết công việc'))",
        "article"
    ])[:1000]

    return {
        "job_title": title,
        "company": company,
        "salary": salary,
        "location": location,
        "posted": posted,
        "company_url": company_url,
        "summary": summary
    }

def click_open_popup_and_scrape(page, href):
    # tìm anchor khớp href (TopCV thêm query theo dõi → dùng starts-with để bền hơn)
    anchor = page.locator(f"a[href='{href}']").first
    if not anchor.count():
        anchor = page.locator(f"a[href^='{href.split('.html')[0]}']").first
    anchor.scroll_into_view_if_needed()
    human_delay()

    with page.expect_popup() as pop_info:
        anchor.click()  # click thường; target=_blank sẽ mở tab mới
    detail_page = pop_info.value

    detail_page.wait_for_load_state("domcontentloaded")
    detail_page.wait_for_timeout(300)

    info = extract_job_detail(detail_page)
    info["job_url"] = detail_page.url

    detail_page.close()
    human_delay()
    return info

def go_next_results_page(page):
    for sel in [
        "a[rel='next']",
        "a.pagination-next",
        "li.next a",
        "a:has-text('Sau')",
        "a:has-text('Tiếp')",
        "button:has-text('Sau')",
    ]:
        el = page.locator(sel)
        if el.count() and el.first.is_visible():
            try:
                el.first.scroll_into_view_if_needed()
            except:
                pass
            el.first.click()
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(500)
            return True
    return False

def run():
    writer = RealtimeCsvWriter(OUTPUT_CSV)
    seen_urls = load_existing_urls_quick(OUTPUT_CSV)

    try:
        with sync_playwright() as p:
            browser = getattr(p, BROWSER_NAME).launch(headless=HEADLESS, slow_mo=SLOW_MO_MS)
            ctx = browser.new_context(
                user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/120.0.0.0 Safari/537.36")
            )
            page = ctx.new_page()

            # 2) Search như trước
            result_url = do_search(page, SEARCH_KEY)
            print("Kết quả tìm kiếm URL:", result_url)

            page_no = 1
            while True:
                print(f"[LIST] Trang #{page_no}: {page.url}")
                hrefs = collect_job_anchors(page)
                print(f"  - Tìm thấy {len(hrefs)} job links.")

                list_url = page.url
                for i, href in enumerate(hrefs, 1):
                    try:
                        info = click_open_popup_and_scrape(page, href)
                        real_url = info["job_url"].strip()
                        if real_url in seen_urls:
                            print(f"    • BỎ QUA (đã có): {real_url}")
                            continue

                        row = {
                            "job_title": info["job_title"],
                            "company": info["company"],
                            "salary": info["salary"],
                            "location": info["location"],
                            "posted": info["posted"],
                            "job_url": real_url,
                            "company_url": info["company_url"],
                            "source_page": list_url,
                            "summary": info["summary"]
                        }

                        # 3) GHI NGAY (REALTIME)
                        writer.write_row(row)
                        seen_urls.add(real_url)
                        print(f"    ✓ GHI CSV: {row['job_title']} | {row['company']}")

                    except Exception as e:
                        print(f"    [ERR] {e} — bỏ qua job này.")

                if MAX_PAGES is not None and page_no >= MAX_PAGES:
                    print("[INFO] Đã đạt MAX_PAGES → dừng.")
                    break
                if not go_next_results_page(page):
                    print("[INFO] Hết trang kết quả.")
                    break
                page_no += 1

            browser.close()

    finally:
        writer.close()
        print(f"[DONE] CSV được cập nhật realtime tại: {OUTPUT_CSV}")

if __name__ == "__main__":
    run()
