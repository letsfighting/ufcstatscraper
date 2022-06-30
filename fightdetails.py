import requests
from bs4 import BeautifulSoup
import re
import pymongoarrow as pma
from pymongoarrow.monkey import patch_all
from pymongo import MongoClient

patch_all()

URL = "http://ufcstats.com/fight-details/1f5f59924b59408b"
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

# client.ufcstats.events.delete_one( {"_id": 610})

# for fight in client.ufcstats.fights.find():
#   fightpage = requests.get(fight['url'])
#   soup = BeautifulSoup(fightpage.content, "html.parser")
#   for fightlink in soup.find_all('a'):
#     text = str(fightlink.get_text())
#     text = text.strip()
#     href = str(fightlink.get('href'))
#     match = re.search("(?P<url>https?://ufcstats.com/fight-details/.+)", href)
#     if match is not None:
#       fightlinks.append((match.group("url")))



# for x in range(0, len(fightlinks)):


#   fight = {'_id': len(fightlinks)-x, 'url': fightlinks[x]}
#   fightdata.append(fight)


# # print(fightdata)

# # client.ufcstats.fights.drop()
# client.ufcstats.fights.insert_many(fightdata)

