import requests
from bs4 import BeautifulSoup

URL = "http://ufcstats.com/statistics/fighters"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

print(soup)