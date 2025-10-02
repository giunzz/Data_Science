import urllib.robotparser

import requests

robots_url = "https://www.linkedin.com/robots.txt"
res = requests.get(robots_url, timeout=10)

print("=== LinkedIn robots.txt ===")
print(res.text)