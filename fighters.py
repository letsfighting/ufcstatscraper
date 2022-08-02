import requests
from bs4 import BeautifulSoup
import re
import pymongoarrow as pma
from pymongoarrow.monkey import patch_all
from pymongo import MongoClient

patch_all()


fightername = []
fighterstat = []


# print(soup)




client = MongoClient()

#  START
# for fighterlink in client.ufcstats.fighterlinks.find():
#   fighterpage = requests.get(fighterlink['url'])
#   soup = BeautifulSoup(fighterpage.content, "html.parser")

#   for name in soup.find_all('span', {"class": "b-content__title-highlight"}):
#     text = str(name.get_text())
#     text = text.strip()
#     fightername.append(text)


#   for attribute in soup.find_all('li', {"class": "b-list__box-list-item_type_block"}):
#     text = str(attribute.get_text())
#     text = text.strip()
#     fighterstat.append((text))


# for fighterlink in client.ufcstats.fighterlinks.find():
#   fighterpage = requests.get(fighterlink['url'])
#   soup = BeautifulSoup(fighterpage.content, "html.parser")

# fighterpage = requests.get('http://ufcstats.com/fighter-details/93fe7332d16c6ad9')
fighterpage = requests.get('http://ufcstats.com/fighter-details/3329d692aea4dc28')
soup = BeautifulSoup(fighterpage.content, "html.parser")


for name in soup.find_all('span', {"class": "b-content__title-highlight"}):
  text = str(name.get_text())
  text = text.strip()
  fightername.append(text)
for attribute in soup.find_all('li', {"class": "b-list__box-list-item_type_block"}):
  text = str(attribute.get_text())
  text = text.strip()
  trimmed = re.search("(?s).*?Height:(.*)", text)
  if trimmed is not None:
    feet = ((trimmed.group(1)[:-4].strip()))
    inches = ((trimmed.group(1)[-2].strip()))
    if feet.isnumeric() and inches.isnumeric():
      totalheight = (int(feet) * 12 + int(inches))
      fighterstat.append(totalheight)
    else:
      fighterstat.append(trimmed.group(1).strip())

  trimmed = re.search("(?s).*Weight:(.*)", text)
  if trimmed is not None:
    if trimmed.group(1)[:-4].strip().isnumeric():
      fighterstat.append(int(trimmed.group(1)[:-4].strip()))
    else:
      fighterstat.append(trimmed.group(1).strip())
  trimmed = re.search("(?s).*Reach:(.*)", text)
  if trimmed is not None:
    if  trimmed.group(1)[:-1].strip().isnumeric():
      fighterstat.append(int(trimmed.group(1)[:-1].strip()))
    else:
      fighterstat.append('--')
  trimmed = re.search("(?s).*STANCE:(.*)", text)
  if trimmed is not None:
    if trimmed.group(1).strip():
      fighterstat.append((trimmed.group(1).strip()))
    else:
      fighterstat.append('--')

  trimmed = re.search("(?s).*DOB:(.*)", text)
  if trimmed is not None:
    if trimmed.group(1)[-4:].strip().isnumeric():
      fighterstat.append(int(trimmed.group(1)[-4:].strip()))
    else:
      fighterstat.append('--')



print(fightername)
print(fighterstat)
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

# client.ufcstats.fighterlinks.drop()
# client.ufcstats.fighterlinks.insert_many(fighterdata)


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