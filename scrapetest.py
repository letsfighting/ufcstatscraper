# this script scrapes event pages example: http://ufcstats.com/event-details/4f853e98886283cf


import requests
from bs4 import BeautifulSoup
import re
import pymongoarrow as pma
from pymongoarrow.monkey import patch_all
from pymongo import MongoClient

patch_all()

URL = "http://ufcstats.com/event-details/4f853e98886283cf"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")


fightlinks = []
fightdata = []
fighters = []




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
print("text2: ", text3)




