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
data = []
eventlinks = []
eventnames = []
eventdata = []

fightlinks = []




for link in soup.find_all('a'):
  text = str(link.get_text())
  text = text.strip()
  href = str(link.get('href'))
  match = re.search("(?P<url>https?://ufcstats.com/event-details/.+)", href)
  if match is not None:
    eventlinks.append((match.group("url")))
    eventnames.append(text)

for x in range(0, len(eventlinks)):
  eventid = (re.search("(?s).*?event-details/(.*)", eventlinks[x])).group(1)
  event = {'_id': eventid, 'human_id': len(eventlinks)-x, 'name': eventnames[x], 'url': eventlinks[x]}
  eventdata.append(event)


print(eventdata)


client = MongoClient()
client.ufcstats.events.drop()
client.ufcstats.events.insert_many(eventdata)

print("Event Data Inserted")

