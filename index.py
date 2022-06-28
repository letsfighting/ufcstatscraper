import requests
from bs4 import BeautifulSoup
import re

URL = "http://ufcstats.com/statistics/events/completed?page=all"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
data = []
eventlinks = []
fightlinks = []


# print(soup)

for link in soup.find_all('a'):
  href = str(link.get('href'))
  match = re.search("(?P<url>https?://ufcstats.com/event-details/.+)", href)
  if match is not None:
    eventlinks.append((match.group("url")))


# print(links)

for event in eventlinks:
  eventpage = requests.get(event)
  soup = BeautifulSoup(eventpage.content, "html.parser")
  for fightlink in soup.find_all('a'):
    href = str(fightlink.get('href'))
    match = re.search("(?P<url>https?://ufcstats.com/fight-details/.+)", href)
    if match is not None:
      fightlinks.append((match.group("url")))


# print(fightlinks)