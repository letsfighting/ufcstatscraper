import requests
from bs4 import BeautifulSoup

URL = "http://ufcstats.com/statistics/events/completed?page=all"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

# print(soup)

for link in soup.find_all('a'):
  print(link.get('href'))

