# # scrape_ivolunteer_realtime_csv.py
# import os, csv, re, time, datetime
# from urllib.parse import urljoin
# from playwright.sync_api import sync_playwright

# START_URL = "https://ivolunteervietnam.com/"
# OUT_CSV   = "Projectivolunteer_posts.csv"
# MAX_POSTS = 60
# MAX_SCROLLS = 12

# def main(): 
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()
#         page.goto('https://ivolunteervietnam.com/hoc-bong/', wait_until="networkidle")
#         print("Page loaded successfully:", page.title())
#         html = page.content()  # toàn bộ DOM hiện tại
#         print("Page HTML length:", len(html))
#     # Dynamic elemnt and extract data
#         page.wait_for_selector("article h2 a") #

#         rows = []
#         cards = page.locator("article")
#         for i in range(cards.count()):
#             c = cards.nth(i)
#             a = c.locator("h2 a")
#             title = (a.inner_text() or "").strip()
#             url   = a.get_attribute("href")
#             date  = c.locator("time").first.get_attribute("datetime") 
#             rows.append({"title": title, "url": url, "date": date})
#             print(f"  - {title} ({date}) [{url}]")
            
#         browser.close()
        
# if __name__ == "__main__":
#     main()

