import urllib.robotparser

# def check_robots(robots_url, test_url, user_agent="*"):
#     rp = urllib.robotparser.RobotFileParser()
#     rp.set_url(robots_url)
#     rp.read()
#     return rp.can_fetch(user_agent, test_url)


# BASE_URL = "https://www.linkedin.com"
# ROBOTS_URL = BASE_URL + "/robots.txt"

# paths = [
#     "/",                      
#     "/jobs",                 
#     "/search/results/people/", 
#     "/feed/"                  
# ]

# print("Robots.txt URL:", ROBOTS_URL)

# for path in paths:
#     test_url = BASE_URL + path
#     allowed = check_robots(ROBOTS_URL, test_url)
#     print(f"Check: {test_url}")
#     print(f"  → scraping allowed? {allowed}")

# # xem toàn bộ
import requests

robots_url = "https://www.linkedin.com/robots.txt"
res = requests.get(robots_url, timeout=10)

print("=== LinkedIn robots.txt ===")
print(res.text)