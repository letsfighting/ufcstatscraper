import requests
from bs4 import BeautifulSoup
import re

URL = "http://ufcstats.com/statistics/events/completed?page=all"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
data = []
links = []


# print(soup)

for link in soup.find_all('a'):
  href = str(link.get('href'))
  match = re.search("(?P<url>https?://ufcstats.com/event-details/.+)", href)
  if match is not None:
    links.append((match.group("url")))


print(links)

