from playwright.sync_api import sync_playwright
from urllib.request import urlretrieve
import requests
import os


pw = sync_playwright().start()
browser = pw.firefox.launch(
    headless=False,
    slow_mo=5000
)

page = browser.new_page()
# page.goto("https://www.traveloka.com/en-vn/hotel")
page.goto("http://arxiv.org/search")

page.get_by_placeholder("Search term...").fill("neural network")

page.get_by_role("button").get_by_text("Search").nth(1).click()

page.wait_for_selector("xpath=//a[contains(@href, '/pdf/')]")
links = page.locator("xpath=//a[contains(@href, '/pdf/')]").all()

print(f"Found {len(links)} PDF links.")

download_dir = "C:\\Users\\ASUS\\Documents\\GitHub\\Data_sceince_ute\\Data_Science\\Project\\Dung\\data"

for link in links:
    url = link.get_attribute("href")
    urlretrieve(url, os.path.join(download_dir, url.split("/")[-1] + ".pdf"))

# print(page.content())
print("Page title:", page.title())

page.screenshot(path="C:\\Users\\ASUS\\Documents\\GitHub\\Data_sceince_ute\\Data_Science\\Project\\Dung\\example.png")


browser.close()