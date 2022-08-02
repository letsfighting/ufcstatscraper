import requests
from bs4 import BeautifulSoup
import re
import pymongoarrow as pma
from pymongoarrow.monkey import patch_all
from pymongo import MongoClient

patch_all()

x = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
y = 0
URL = f"http://ufcstats.com/statistics/fighters?char={x[y]}&page=all"



fighterlinks = []
fighterdata = []


# print(soup)

for letter in x:
  URL = f"http://ufcstats.com/statistics/fighters?char={x[y]}&page=all"
  print(URL)
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, "html.parser")
  for link in soup.find_all('a'):
    text = str(link.get_text())
    text = text.strip()
    href = str(link.get('href'))
    match = re.search("(?P<url>https?://ufcstats.com/fighter-details/.+)", href)
    if match is not None:
      if match.group("url") in fighterlinks:
        continue
      else:
        fighterlinks.append((match.group("url")))
  
  y = y + 1



for z in range(0, len(fighterlinks)):
  fighter = {'_id': (re.search("(?s).*?fighter-details/(.*)", fighterlinks[z])).group(1), 'url': fighterlinks[z]}
  fighterdata.append(fighter)


print(fighterdata)


client = MongoClient()

# client.ufcstats.events.delete_one( {"_id": 610})


#  START
# for event in client.ufcstats.events.find():
#   eventpage = requests.get(event['url'])
#   soup = BeautifulSoup(eventpage.content, "html.parser")
#   for fightlink in soup.find_all('a'):
#     text = str(fightlink.get_text())
#     text = text.strip()
#     href = str(fightlink.get('href'))
#     match = re.search("(?P<url>https?://ufcstats.com/fight-details/.+)", href)
#     # nameMatch = re.search("(?P<url>https?://ufcstats.com/fighter-details/.+)", href)
#     if match is not None:
#       fightlinks.append((match.group("url")))
#     # if nameMatch is not None:
#     #   fighters.append((text))

# END


#  format and insert into mongo
# for x in range(0, len(fightlinks)):

#   # if x == 0:
#   #   y = x
#   # else:
#   #   y += 1

#   fight = {'_id': len(fightlinks)-x, 'url': fightlinks[x]}
#   fightdata.append(fight)


# print(fightdata)

client.ufcstats.fighterlinks.drop()
client.ufcstats.fighterlinks.insert_many(fighterdata)


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