from playwright.sync_api import sync_playwright

proxies = {
    "server": "brd.superproxy.io:33335",
    "username": "brd-customer-hl_f46f9e68-zone-dung_zone1",
    "password": "2wumzv594s80"
    
}
pw = sync_playwright().start()
browser = pw.firefox.launch(headless=False, slow_mo=5000, proxy=proxies)
page = browser.new_page()
page.goto("http://www.geektime.co.il/") #use cloudflare
#page.goto("http://www.walmart.com") #captcha

page.locator("xpath=//input[@type='search']").fill("testing")
page.keyboard.press("Enter")
page.screenshot(path="example.png")
print("Page title:", page.title())