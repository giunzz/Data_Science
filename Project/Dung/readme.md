## Báo cáo Web scraping using python 

### Dữ liệu 
1. Một số cuộc thi, hoạt động ngoại khóa 
2. Một số công ty đang tuyển dụng

### Kỹ thuật scraping data 
- Trang web có định dạnh (có cấu trúc hay phi cấu trúc)
- Web scraping yêu cầu 2 parts: crawler & scraper. 
    - Trình thu thập thông tin (crawler) là một thuật toán trí tuệ nhân tạo duyệt web để tìm kiếm dữ liệu cụ thể cần thiết bằng cách theo các liên kết trên internet. 
    - Scaper là một công cụ cụ thể được tạo ra để trích xuất dữ liệu từ trang web.
- Types of Web Scrapers: **Self-built** or Pre-built Web Scrapers, Browser extension or Software Web Scrapers, and Cloud or Local Web Scrapers.

1. Định danh (DOM (Document Object Model))


### Triển khai web 
| Tiêu chí                            | **Requests + BeautifulSoup**  | **Selenium / Playwright**                |
| ----------------------------------- | ----------------------------- | ---------------------------------------- |
| **Cách lấy dữ liệu**                | Gửi request lấy HTML thô      | Mở trình duyệt → render → lấy DOM sau JS |
| **Tốc độ**                          |  Rất nhanh (vài ms/request) | Chậm (vài giây/trang)                 |
| **Tài nguyên**                      | Nhẹ, tốn ít CPU/RAM           | Nặng, cần nhiều CPU/RAM                  |
| **Khả năng chạy JS**                |  Không hỗ trợ                |  Hỗ trợ đầy đủ                          |
| **Khả năng login / scroll / click** |  Không làm được              | Làm được như người dùng                |
| **Khả năng scale lớn**              | Dễ (crawl 100k+ URL)        | Khó (chậm, dễ block)                   |
| **Ứng dụng phù hợp**                | Web tĩnh, API JSON, blog, báo | Web động, e-commerce, mạng xã hội        |

- Một số tình hướng 

| Loại trang | Công cụ                  | Khó khăn chính           |
| ---------- | ------------------------ | ------------------------ |
| HTML tĩnh  | Requests + BeautifulSoup | Dễ gãy khi đổi HTML      |
| Bảng HTML  | Pandas `read_html`       | Bảng lồng nhau, encoding |
| JS động    | Selenium / Playwright    | Chậm, anti-bot           |
| API ẩn     | Requests                 | Cần tìm endpoint, token  |
| PDF/Excel  | Pandas, Camelot          | PDF khó xử lý            |


### Nguồn tham khảo
1. [Defination: Scraping](https://www.geeksforgeeks.org/blogs/what-is-web-scraping-and-how-to-use-it/)

2. [Tutorial](https://www.geeksforgeeks.org/python/python-web-scraping-tutorial/)

3.[How To Legally Extract Web Content](https://kinsta.com/knowledgebase/what-is-web-scraping/)