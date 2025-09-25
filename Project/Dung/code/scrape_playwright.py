from playwright.sync_api import sync_playwright #API đồng bộ, cho phép điều khiển trình duyệt như người dùng thật.
from urllib.request import urlretrieve #tải tệp từ URL về máy
import os #Xử lý đường dẫn, tạo thư mụ


pw = sync_playwright().start() #Tạo ra một instance điều khiển trình duyệt.

browser = pw.firefox.launch(
    headless=False, # run GUI
    slow_mo=5000 # 1 step = 5s
)

page = browser.new_page()
page.goto("http://arxiv.org/search")

page.get_by_placeholder("Search term...").fill("neural network")

page.get_by_role("button").get_by_text("Search").nth(1).click() # nhấn tìm kiếm gửi truy vấn | label theo level

page.wait_for_selector("xpath=//a[contains(@href, '/pdf/')]")
links = page.locator("xpath=//a[contains(@href, '/pdf/')]").all()

print(f"Found {len(links)} PDF links.")
download_dir = "C:\\Users\\ASUS\\Documents\\GitHub\\Data_sceince_ute\\Data_Science\\Project\\Dung\\data\\paper_arxiv"

for link in links:
    url = link.get_attribute("href")
    urlretrieve(url, os.path.join(download_dir, url.split("/")[-1] + ".pdf")) #lưu vào thư mục với file được ghép 

print("Page title:", page.title())

page.screenshot(path="C:\\Users\\ASUS\\Documents\\GitHub\\Data_sceince_ute\\Data_Science\\Project\\Dung\\img\\arxiv.png")
browser.close()


