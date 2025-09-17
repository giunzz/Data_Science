from playwright.sync_api import sync_playwright

proxies = {
    "server": "brd.superproxy.io:33335",
    "username": "brd-customer-hl_f46f9e68-zone-dung_zone1",
    "password": "2wumzv594s80"
}

# Start Playwright and launch browser
pw = sync_playwright().start()
browser = pw.firefox.launch(headless=False, slow_mo=3000)
page = browser.new_page()

page.goto("http://www.walmart.com")

page.locator("input[aria-label='Search']").fill("clothes")
page.locator("button[type='submit']").click()  

# page.wait_for_load_state("networkidle")

# total_pages = 1

# for page_num in range(1, total_pages + 1):
#     print(f"Scraping page {page_num}")
    
#     # Ensure the page has finished loading before proceeding
#     page.wait_for_load_state("networkidle")
    
#     # Select product links and click them
#     product_links = page.locator("a[href*='/ip/']")
    
#     for i in range(len(product_links)):
#         product_links.nth(i).click()
        
#         # Wait for the product page to load
#         page.wait_for_load_state("networkidle")
        
#         # Take a screenshot of each product page
#         page.screenshot(path=f"product_page_{page_num}_{i+1}.png")
#         print(f"Page title for product {i+1} on page {page_num}:", page.title())
        
#         # Go back to the previous page (the list of products)
#         page.go_back()
        
#     # Move to the next page if available (pagination handling)
#     if page_num < total_pages:
#         next_page_button = page.locator("a[aria-label='Next Page']")
#         next_page_button.click()
#         page.wait_for_load_state("networkidle")

# # Take a final screenshot of the current page (after scraping)
page.screenshot(path="example.png")
print("Page title:", page.title())

browser.close()
