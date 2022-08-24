# this script scrapes event pages example: http://ufcstats.com/event-details/4f853e98886283cf


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


fightlinks = []
fightyears = []
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
#
# # delete the last event as it has no fights yet
client.ufcstats.events.delete_one( {"human_id": 618})

for event in client.ufcstats.events.find():
  eventpage = requests.get(event['url'])
  soup = BeautifulSoup(eventpage.content, "html.parser")
  for fightlink in soup.find_all('a'):
    text = str(fightlink.get_text())
    text = text.strip()
    href = str(fightlink.get('href'))
    match = re.search("(?P<url>https?://ufcstats.com/fight-details/.+)", href)
    # nameMatch = re.search("(?P<url>https?://ufcstats.com/fighter-details/.+)", href)
    if match is not None:
      if match.group("url") in fightlinks:
        continue
      else:
        print("Appended: ", match.group("url"))
        fightlinks.append((match.group("url")))

        date = soup.find('li', {"class": "b-list__box-list-item"})
        text2 = str(date.get_text())

        text2 = text2.strip()
        text2 = re.search("(?s).*?:(.*)", text2)
        text2 = text2.group(1)[1:]
        text3 = text2[-4:]
        fightyears.append(int(text3))

for x in range(0, len(fightlinks)):

  # if x == 0:
  #   y = x
  # else:
  #   y += 1

  fightid = (re.search("(?s).*?fight-details/(.*)", fightlinks[x])).group(1)
  fight = {'_id': fightid, 'human_id': len(fightlinks)-x, 'url': fightlinks[x], 'year': fightyears[x]}
  print("Inserted: ", fight)
  fightdata.append(fight)


# print(fightdata)

client.ufcstats.fights.drop()
client.ufcstats.fights.insert_many(fightdata)


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