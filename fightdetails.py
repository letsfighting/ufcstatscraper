from operator import truediv
import requests
from bs4 import BeautifulSoup
import re
import pymongoarrow as pma
from pymongoarrow.monkey import patch_all
from pymongo import MongoClient


from modules.statsparser import statsparser

patch_all()


def fightdetails(url):
  # URL = "http://ufcstats.com/fight-details/a7eaf7b101166d3e"
  URL = url
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
  method_array = []
  method_array2 = []



  for link in soup.find_all('i', {"class": "b-fight-details__person-status"}):
    text = str(link.get_text())
    text = text.strip()
    # href = str(link.get('href'))

    outcome_array.append(text)

  # # for x in range(0, len(eventlinks)):
  # #   event = {'_id': len(eventlinks)-x, 'name': eventnames[x], 'url': eventlinks[x]}
  # #   eventdata.append(event)

  print(f"outcome_array: {outcome_array}")

  for link in soup.find_all('i', {"class": "b-fight-details__text-item_first"}):
    text = str(link.get_text())
    text = text.strip()
    # href = str(link.get('href'))

    method_array.append(text)

  # # for x in range(0, len(eventlinks)):
  # #   event = {'_id': len(eventlinks)-x, 'name': eventnames[x], 'url': eventlinks[x]}
  # #   eventdata.append(event)

  # to return everything after "Method:
  trimmed1 = re.search(r'Method:\s*([^\r\n]+)', method_array[0])

  print(f"trimmed method: {trimmed1.group(1)}")


  for link in soup.find_all('p', {"class": "b-fight-details__text"}):
    text = str(link.get_text())
    text = text.strip()
    # href = str(link.get('href'))

    method_array2.append(text)

  # # for x in range(0, len(eventlinks)):
  # #   event = {'_id': len(eventlinks)-x, 'name': eventnames[x], 'url': eventlinks[x]}
  # #   eventdata.append(event)


  # to return everything after "Details:"
  # trimmed2 = re.search(r'Details:\s*([^\r\n]+)', method_array2[1])

  # print(f"trimmed method2: {trimmed2.group(1)}")




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

  

  if len(details) < 6:
    weight_class = (re.search("(?s).*?Fight_Type:(.*)", details[4]).group(1))
    referee = (re.search("(?s).*?Referee:(.*)", details[3]).group(1))
    judge1 = "judge1"
    judge2 = "judge2"
    judge3 = "judge3"
    judge1score = "--"
    judge2score = "--"
    judge3score = "--"
    round_format = int(re.search("(?s).*?Time format:(.*)", details[2]).group(1))
    rounds_total = int(re.search("(?s).*?Round:(.*)", details[0]).group(1))
    if data[4].find("Title") > -1:
      championship = True
    else:
      championship = False

  else:
    weight_class = (re.search("(?s).*?Fight_Type:(.*)", details[7]).group(1))
    referee = (re.search("(?s).*?Referee:(.*)", details[3]).group(1))
    judge1 = (re.search("^(.*)(?=:)", details[4]).group(1))
    judge2 = (re.search("^(.*)(?=:)", details[5]).group(1))
    judge3 = (re.search("^(.*)(?=:)", details[6]).group(1))
    judge1score = (re.search("^(?s).*?:(.*)", details[4]).group(1))
    judge2score = (re.search("^(?s).*?:(.*)", details[5]).group(1))
    judge3score = (re.search("^(?s).*?:(.*)", details[6]).group(1))
    round_format = int(re.search("(?s).*?Time format:(.*)", details[2]).group(1))
    rounds_total = int(re.search("(?s).*?Round:(.*)", details[0]).group(1))
    if data[7].find("Title") > -1:
      championship = True
    else:
      championship = False

  print(f"labels: {labels}")
  print(f"data: {data}")

  minutes = int(re.search("^(.*)(?=:)", data[1]).group(1))
  seconds = int(re.search("^(?s).*?:(.*)", data[1]).group(1))
  
  duration = int(data[0]) * 5 * 60 + minutes * 60 + seconds


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
    outcome = 1

  elif outcome_array[0] == "L":
    winner_loser.append(fighter_names[1])
    winner_loser.append(fighter_names[0])
    outcome = 2
  elif outcome_array[0] == "D":
    winner_loser.append("D")
    outcome = 3
  elif outcome_array[0] == "NC":
    winner_loser.append("NC")
    outcome = 0

  print(f"winner_loser: {winner_loser}")

# fightid = {'event': trimmed.group(1)[1:], "fighter1": winner_loser[0], "fighter2": winner_loser[1]}

  

  

  fight_details = { 'fight_id': (re.search("(?s).*?fight-details/(.*)", url)).group(1), 'fighter1_id': (re.search("(?s).*?fighter-details/(.*)",fighter_links[0])).group(1), 'fighter2_id': (re.search("(?s).*?fighter-details/(.*)",fighter_links[1])).group(1), 'outcome': outcome, 'method': trimmed1.group(1), 'referee': referee, 'weight_class': weight_class, f'{judge1}': judge1score, f'{judge2}': judge2score, f'{judge3}': judge3score, 'format': round_format, 'round_finish': rounds_total, 'duration': duration, 'championship': championship}

  statsparser(int(data[0]), stats)

  print(fight_details)




fightdetails("http://ufcstats.com/fight-details/03aec9073946907f")

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




