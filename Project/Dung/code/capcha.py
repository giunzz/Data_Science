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

print("Page title:", page.title())
page.screenshot(path="C:\\Users\\ASUS\\Documents\\GitHub\\Data_sceince_ute\\Data_Science\\Project\\Dung\\img\\walmart.png")


browser.close()
