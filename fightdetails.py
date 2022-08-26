from operator import truediv
import requests
from bs4 import BeautifulSoup
import re
import pymongoarrow as pma
from pymongoarrow.monkey import patch_all
from pymongo import MongoClient

import time


from modules.statsparser import statsparser

patch_all()


def fightstatsfighter(fighturl, fighterlinksArr, fighternamesArr, method, referee, detailedmethod, rounds_fought, duration, outcome, statsArrObj, stats_available, years):

  fight_id = (re.search("(?s).*?fight-details/(.*)", fighturl)).group(1)
  fighter1_id = (re.search("(?s).*?fighter-details/(.*)", fighterlinksArr[0])).group(1)
  fighter2_id = (re.search("(?s).*?fighter-details/(.*)", fighterlinksArr[1])).group(1)
  fighter1_name = fighternamesArr[0]
  fighter2_name = fighternamesArr[1]
  uid1 = fight_id + '_' + fighter1_id
  uid2 = fight_id + '_' + fighter2_id
  fighter1_stats = statsArrObj['fighter1']
  fighter2_stats = statsArrObj['fighter2']
  
  if outcome == 0:
    result1 = "NC"
    result2 = "NC"
  elif outcome == 1:
    result1 = "W"
    result2 = "L"
  elif outcome == 2:
    result1 = "L"
    result2 = "W"
  elif outcome == 3:
    result1 = "D"
    result2 = "D"

  
  fighter1_complete = {'_id': uid1, 'fight_id': fight_id, 'fighter_id': fighter1_id, 'fighter_name': fighter1_name, 'opponent_id': fighter2_id, 'opponent_name': fighter2_name, 'method': method, 'referee': referee, 'detailed_method': detailedmethod, 'rounds_fought': rounds_fought, 'duration': duration, 'outcome': result1, 
  'KD': fighter1_stats[0], 'SS': fighter1_stats[1], 'SSA':  fighter1_stats[2], 'TD':  fighter1_stats[3], 'TDA':  fighter1_stats[4], 'SUBATT':  fighter1_stats[5], 'REV':  fighter1_stats[6], 'CTRL': fighter1_stats[7], 'HS': fighter1_stats[8], 'HSA': fighter1_stats[9], 
  'BS': fighter1_stats[10], 'BSA': fighter1_stats[11], 'LS': fighter1_stats[12], 'LSA': fighter1_stats[13], 'DS': fighter1_stats[14], 'DSA': fighter1_stats[15], 'CS': fighter1_stats[16], 'CSA': fighter1_stats[17], 'GS': fighter1_stats[18], 'GSA': fighter1_stats[19], 'Downed': fighter1_stats[20], 'SSD': fighter1_stats[21], 'SSR': fighter1_stats[22], 'TDD': fighter1_stats[23], 'TDR': fighter1_stats[24], 'REVED': fighter1_stats[25], 'CTRLED': fighter1_stats[26], 'HSD': fighter1_stats[27], 'HSR': fighter1_stats[28],
  'BSD': fighter1_stats[29], 'BSR': fighter1_stats[30], 'LSD': fighter1_stats[31], 'LSR': fighter1_stats[32], 'DSD': fighter1_stats[33], 'DSR': fighter1_stats[34], 'CSD': fighter1_stats[35], 'CSR': fighter1_stats[36], 'GSD': fighter1_stats[37], 'GSR': fighter1_stats[38], 'stats_available': stats_available, 'year': years}

  fighter2_complete = {'_id': uid2, 'fight_id': fight_id, 'fighter_id': fighter2_id, 'fighter_name': fighter2_name, 'opponent_id': fighter1_id, 'opponent_name': fighter1_name, 'method': method, 'referee': referee, 'detailed_method': detailedmethod, 'rounds_fought': rounds_fought, 'duration': duration, 'outcome': result2, 
  'KD': fighter2_stats[0], 'SS': fighter2_stats[1], 'SSA':  fighter2_stats[2], 'TD':  fighter2_stats[3], 'TDA':  fighter2_stats[4], 'SUBATT':  fighter2_stats[5], 'REV':  fighter2_stats[6], 'CTRL': fighter2_stats[7], 'HS': fighter2_stats[8], 'HSA': fighter2_stats[9], 
  'BS': fighter2_stats[10], 'BSA': fighter2_stats[11], 'LS': fighter2_stats[12], 'LSA': fighter2_stats[13], 'DS': fighter2_stats[14], 'DSA': fighter2_stats[15], 'CS': fighter2_stats[16], 'CSA': fighter2_stats[17], 'GS': fighter2_stats[18], 'GSA': fighter2_stats[19], 'Downed': fighter2_stats[20], 'SSD': fighter2_stats[21], 'SSR': fighter2_stats[22], 'TDD': fighter2_stats[23], 'TDR': fighter2_stats[24], 'REVED': fighter2_stats[25], 'CTRLED': fighter2_stats[26], 'HSD': fighter2_stats[27], 'HSR': fighter2_stats[28],
  'BSD': fighter2_stats[29], 'BSR': fighter2_stats[30], 'LSD': fighter2_stats[31], 'LSR': fighter2_stats[32], 'DSD': fighter2_stats[33], 'DSR': fighter2_stats[34], 'CSD': fighter2_stats[35], 'CSR': fighter2_stats[36], 'GSD': fighter2_stats[37], 'GSR': fighter2_stats[38], 'stats_available': stats_available, 'year': years}

  answer = [fighter1_complete, fighter2_complete]
  # print('answer: ', answer)

  return answer 





def fightdetails(url, years):

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

  # print(f"outcome_array: {outcome_array}")

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

  # print(f"trimmed method: {trimmed1.group(1)}")
  method = trimmed1.group(1)


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

  # print(f"Fighter Links: {fighter_links}")
  # print(f"Fighter Names: {fighter_names}")

  for link in soup.find_all('p', {"class": "b-fight-details__table-text"}):
    text = str(link.get_text())
    text = text.strip()
    if (text != fighter_names[0] and text != fighter_names[1]):
      stats.append((text))

  # print(f"stats: {stats}")

  for link in soup.find_all('i', {"class": "b-fight-details__text-item"}):
    text = str(link.get_text())
    text = text.strip()
    cleanText = text.replace('\n        \n        ','')
    cleanText = cleanText.replace(' Rnd (5)','')
    cleanText = cleanText.replace(' Rnd (5-5)','')
    cleanText = cleanText.replace(' Rnd (5-5-5)','')
    cleanText = cleanText.replace(' Rnd (5-5-5-5-5)','')
    cleanText = cleanText.replace(' Rnd + OT (5-5-5-5)','')
    cleanText = cleanText.replace(' Rnd + OT (5-5-5-5-5-5)','')
    cleanText = cleanText.replace(' Rnd + 2OT (15-3-3)','')
    cleanText = cleanText.replace(' Rnd + OT (12-3)','')
    cleanText = cleanText.replace('\n        \n\n                                ','')
    cleanText = cleanText.replace(' \n\n            \n            \n            ',':')
    cleanText = cleanText.replace('.','')
    # if cleanText == 'No Time Limit'
    #   cleanText =   
    # print(f"cleanText: {cleanText}")
    details.append((cleanText))

  

  for link in soup.find_all('i', {"class": "b-fight-details__fight-title"}):
    text = str(link.get_text())
    text = text.strip()
    text = f"Fight_Type:{text}"
    details.append((text))

  # print(f"details: {details}")

  

  # for item in details:
  #   match = re.search("(.+?(?=:))", item)
    
  #   labels.append(match.group(1))
    
  for item in details:
    match = re.search(":([\s\S]*)$", item)
    if match != None:
      data.append(match.group(1))

  # print('details: ', details)
  # print('data: ', data)


  if len(details) < 6:
    weight_class = (re.search("(?s).*?Fight_Type:(.*)", details[4]).group(1))
    referee = (re.search("(?s).*?Referee:(.*)", details[3]).group(1))
    judge1 = "judge1"
    judge2 = "judge2"
    judge3 = "judge3"
    judge1score = "--"
    judge2score = "--"
    judge3score = "--"
    if re.search("(?s).*?Time format:(.*)", details[2]).group(1).isnumeric():
      round_format = int(re.search("(?s).*?Time format:(.*)", details[2]).group(1))
    else:
      round_format = (re.search("(?s).*?Time format:(.*)", details[2]).group(1))
    rounds_total = int(re.search("(?s).*?Round:(.*)", details[0]).group(1))
    # print(method_array2)
    if re.search(r'Details:\s*([^\r\n]+)', method_array2[1]) != None:
      detailedmethod = re.search(r'Details:\s*([^\r\n]+)', method_array2[1]).group(1)
    else:
      detailedmethod = "Not Applicable"
      
    if data[4].find("Title") > -1:
      championship = True
    else:
      championship = False

  else:
    weight_class = (re.search("(?s).*?Fight_Type:(.*)", details[7]).group(1))
    referee = (re.search("(?s).*?Referee:(.*)", details[3]).group(1))
    if re.search("^(.*)(?=:)", details[4]) != None:
      judge1 = (re.search("^(.*)(?=:)", details[4]).group(1))
    else:
      judge1 = 'judge1'
    if re.search("^(.*)(?=:)", details[5]) != None:      
      judge2 = (re.search("^(.*)(?=:)", details[5]).group(1))
    else:
      judge2 = 'judge2'
    if re.search("^(.*)(?=:)", details[6]) != None:
      judge3 = (re.search("^(.*)(?=:)", details[6]).group(1))
    else:
      judge3 = 'judge3'
    if re.search("(?s).*?:(.*)", details[4]) != None:
      judge1score = (re.search("(?s).*?:(.*)", details[4]).group(1))
    else:
      judge1score = details[4]
    if re.search("(?s).*?:(.*)", details[5]) != None:
      judge2score = (re.search("(?s).*?:(.*)", details[5]).group(1))
    else:
      judge2score = details[5]
    if re.search("(?s).*?:(.*)", details[6]) != None:
      judge3score = (re.search("(?s).*?:(.*)", details[6]).group(1))
    else:
      judge3score = details[6]
    round_format = int(re.search("(?s).*?Time format:(.*)", details[2]).group(1))
  
    rounds_total = int(re.search("(?s).*?Round:(.*)", details[0]).group(1))
    detailedmethod = "Judge's Decision"

    if data[len(data)-1].find("Title") > -1:
      championship = True
    else:
      championship = False

    # print("championship: " + str(championship))

  # print(f"labels: {labels}")
  # print(f"data: {data}")

  minutes = int(re.search("^(.*)(?=:)", data[1]).group(1))
  seconds = int(re.search("(?s).*?:(.*)", data[1]).group(1))
  
  duration = int(data[0]) * 5 * 60 + minutes * 60 + seconds


  for link in soup.find_all('a'):
    text = str(link.get_text())
    text = text.strip()
    href = str(link.get('href'))
    match = re.search("(?P<url>https?://ufcstats.com/event-details/.+)", href)
    if match is not None:
      fight.append(text)


  # print(f"fight: {fight}")

  trimmed = re.search(":([\s\S]*)$", fight[0])

  # print(f"trimmed fight: {trimmed.group(1)[1:]}")





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

  # print(f"winner_loser: {winner_loser}")

# fightid = {'event': trimmed.group(1)[1:], "fighter1": winner_loser[0], "fighter2": winner_loser[1]}

  
  
  

  fight_details = { '_id': (re.search("(?s).*?fight-details/(.*)", url)).group(1), 'fighter1_id': (re.search("(?s).*?fighter-details/(.*)",fighter_links[0])).group(1), 'fighter2_id': (re.search("(?s).*?fighter-details/(.*)",fighter_links[1])).group(1), 'outcome': outcome, 'method': trimmed1.group(1), 'detailed_method': detailedmethod, 'referee': referee, 'weight_class': weight_class, f'{judge1}': judge1score, f'{judge2}': judge2score, f'{judge3}': judge3score, 'format': round_format, 'round_finish': rounds_total, 'duration': duration, 'championship': championship}

  print("fight_details: ", fight_details)
  print("stats: ", stats)

  stats_available = True

  print("length: ", len(stats))

  if len(stats) == 0:
    stats_available = False
    fight_stats = {'fighter1': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 'fighter2': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}
  else:
    fight_stats = statsparser(int(data[0]), stats)



  # print("fight_details: ", fight_details)
  # print("fight_stats: ", fight_stats)



  fight_stats_fighter = fightstatsfighter(url, fighter_links, fighter_names, method, referee, detailedmethod, rounds_total, duration, outcome, fight_stats, stats_available, years)
  
  print("fight_stats_fighter: ", fight_stats_fighter)

  client = MongoClient()



  client.ufcstats.fightdetails.insert_one(fight_details)
  client.ufcstats.fightstats.insert_many(fight_stats_fighter)

# end of fightdetails function

# fightdetails("http://ufcstats.com/fight-details/635fbf57001897c7")






mclient = MongoClient()
mclient.ufcstats.fightdetails.drop()
mclient.ufcstats.fightstats.drop()
timestart = time.time()
print("Started at: ", timestart)

for fight in mclient.ufcstats.fights.find():
  print("Captured fight: ", fight['url'], fight['year'])
  fightdetails(fight['url'], fight['year'])
  

timefinish = time.time()
timecomplete = timefinish - timestart
print(f"It took {timecomplete} seconds to complete")






