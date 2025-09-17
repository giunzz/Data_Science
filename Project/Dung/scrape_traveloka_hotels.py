from playwright.sync_api import sync_playwright
from urllib.request import urlretrieve
import requests
import os


download_dir = "C:\\Users\\ASUS\\Documents\\GitHub\\Data_sceince_ute\\Data_Science\\Project\\Dung\\data"


pw = sync_playwright().start()
browser = pw.firefox.launch(
    headless=False,
    # slow_mo=2000
)

page = browser.new_page()
# page.goto("https://www.traveloka.com/en-vn/hotel")
page.goto("http://arxiv.org/search")

page.get_by_placeholder("Search term...").fill("neural network")

page.get_by_role("button").get_by_text("Search").nth(1).click()

# Cập nhật lại XPath để chỉ lấy các liên kết PDF
links = page.locator("xpath=//a[contains(@href, '/pdf/')]").all()

# Lặp qua các liên kết và tải PDF về
for link in links:
    url = link.evaluate("element => element.href")
    print("Downloading:", url)

    # Tải file PDF sử dụng requests
    try:
        response = requests.get(url)

        # Kiểm tra nếu yêu cầu thành công (status code 200)
        if response.status_code == 200:
            # Sử dụng phần cuối của URL làm tên file (ví dụ: "2509.12202.pdf")
            file_name = url.split("/")[-1] + ".pdf"
            file_path = os.path.join(download_dir, file_name)

            # Lưu nội dung vào file
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"Downloaded: {file_name}")
        else:
            print(f"Failed to download: {url}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")


# print(page.content())
print("Page title:", page.title())

page.screenshot(path="C:\\Users\\ASUS\\Documents\\GitHub\\Data_sceince_ute\\Data_Science\\Project\\Dung\\example.png")


browser.close()