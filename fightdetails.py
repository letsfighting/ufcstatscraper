import requests
from bs4 import BeautifulSoup
import re
import pymongoarrow as pma
from pymongoarrow.monkey import patch_all
from pymongo import MongoClient

patch_all()

URL = "http://ufcstats.com/fight-details/3c98739eb42f96bf"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

fighter_links = []
fighter_names = []
stats = []
ref = []
details = []
labels = []
data = []
outcome_array = []
fight = []
winner_loser = []



for link in soup.find_all('i', {"class": "b-fight-details__person-status"}):
  text = str(link.get_text())
  text = text.strip()
  # href = str(link.get('href'))
  # match = re.search("(?P<url>https?://ufcstats.com/fighter-details/.+)", href)
  # if match is not None:
  outcome_array.append(text)

# # for x in range(0, len(eventlinks)):
# #   event = {'_id': len(eventlinks)-x, 'name': eventnames[x], 'url': eventlinks[x]}
# #   eventdata.append(event)


print(f"outcome_array: {outcome_array}")

for link in soup.find_all('a'):
  text = str(link.get_text())
  text = text.strip()
  href = str(link.get('href'))
  match = re.search("(?P<url>https?://ufcstats.com/fighter-details/.+)", href)
  if match is not None:
    fighter_links.append((match.group("url")))
    fighter_names.append(text)

# # for x in range(0, len(eventlinks)):
# #   event = {'_id': len(eventlinks)-x, 'name': eventnames[x], 'url': eventlinks[x]}
# #   eventdata.append(event)


fighter_links = list(dict.fromkeys(fighter_links))
fighter_names = list(dict.fromkeys(fighter_names))

print(f"Fighter Links: {fighter_links}")
print(f"Fighter Names: {fighter_names}")

for link in soup.find_all('p', {"class": "b-fight-details__table-text"}):
  text = str(link.get_text())
  text = text.strip()
  if (text != fighter_names[0] and text != fighter_names[1]):
    stats.append((text))

print(f"stats: {stats}")

for link in soup.find_all('i', {"class": "b-fight-details__text-item"}):
  text = str(link.get_text())
  text = text.strip()
  cleanText = text.replace('\n        \n        ','')
  cleanText = cleanText.replace(' Rnd (5-5-5)','')
  cleanText = cleanText.replace(' Rnd (5-5-5-5-5)','')
  cleanText = cleanText.replace('\n        \n\n                                ','')
  cleanText = cleanText.replace(' \n\n            \n            \n            ',':')
  cleanText = cleanText.replace('.','')
  details.append((cleanText))

print(f"details: {details}")

for link in soup.find_all('i', {"class": "b-fight-details__fight-title"}):
  text = str(link.get_text())
  text = text.strip()
  text = f"Fight_Type:{text}"
  details.append((text))

print(f"details: {details}")

for item in details:
  match = re.search("(.+?(?=:))", item)
  
  labels.append(match.group(1))
  
for item in details:
  match = re.search(":([\s\S]*)$", item)
  
  data.append(match.group(1))

print(f"labels: {labels}")
print(f"data: {data}")



for link in soup.find_all('a'):
  text = str(link.get_text())
  text = text.strip()
  href = str(link.get('href'))
  match = re.search("(?P<url>https?://ufcstats.com/event-details/.+)", href)
  if match is not None:
    fight.append(text)


print(f"fight: {fight}")

trimmed = re.search(":([\s\S]*)$", fight[0])

print(f"trimmed fight: {trimmed.group(1)[1:]}")

if outcome_array[0] == "W":
 winner_loser.append(fighter_names[0])
 winner_loser.append(fighter_names[1])
elif outcome_array[0] == "L":
 winner_loser.append(fighter_names[1])
 winner_loser.append(fighter_names[0])
elif outcome_array[0] == "D":
 winner_loser.append(fighter_names[0])
 winner_loser.append(fighter_names[1])

print(f"winner_loser: {winner_loser}")

# fightid = {'event': trimmed.group(1)[1:], "fighter1": winner_loser[0], "fighter2": winner_loser[1]}

# fight details organization

#
#




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
#


# for x in range(0, len(fightlinks)):


#   fight = {'_id': len(fightlinks)-x, 'url': fightlinks[x]}
#   fightdata.append(fight)
#

# # print(fightdata)

# # client.ufcstats.fights.drop()
# client.ufcstats.fights.insert_many(fightdata)

