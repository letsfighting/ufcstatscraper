import requests
from bs4 import BeautifulSoup
import re
import pymongoarrow as pma
from pymongoarrow.monkey import patch_all
from pymongo import MongoClient

patch_all()

URL = "http://ufcstats.com/statistics/events/completed?page=all"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
# data = []
# eventlinks = []
# eventnames = []
# eventdata = []

fightlinks = []
fightdata = []
fighters = []


# print(soup)

# for link in soup.find_all('a'):
#   text = str(link.get_text())
#   text = text.strip()
#   href = str(link.get('href'))
#   match = re.search("(?P<url>https?://ufcstats.com/event-details/.+)", href)
#   if match is not None:
#     eventlinks.append((match.group("url")))
#     eventnames.append(text)

# for x in range(0, len(eventlinks)):
#   event = {'_id': len(eventlinks)-x, 'name': eventnames[x], 'url': eventlinks[x]}
#   eventdata.append(event)


# print(eventdata)


client = MongoClient()

for event in client.ufcstats.events.find():
  eventpage = requests.get(event['url'])
  soup = BeautifulSoup(eventpage.content, "html.parser")
  for fightlink in soup.find_all('a'):
    text = str(fightlink.get_text())
    text = text.strip()
    href = str(fightlink.get('href'))
    match = re.search("(?P<url>https?://ufcstats.com/fight-details/.+)", href)
    nameMatch = re.search("(?P<url>https?://ufcstats.com/fighter-details/.+)", href)
    if match is not None:
      fightlinks.append((match.group("url")))
    if nameMatch is not None:
      fighters.append((text))

print(fighters)
 #
# for event in eventlinks:
#   eventpage = requests.get(event)
#   soup = BeautifulSoup(eventpage.content, "html.parser")
#   for fightlink in soup.find_all('a'):
#     href = str(fightlink.get('href'))
#     match = re.search("(?P<url>https?://ufcstats.com/fight-details/.+)", href)
#     if match is not None:
#       fightlinks.append((match.group("url")))


# print(fightlinks)