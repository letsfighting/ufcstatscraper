import requests
from bs4 import BeautifulSoup
import re
import pymongoarrow as pma
from pymongoarrow.monkey import patch_all
from pymongo import MongoClient
import time


patch_all()



eventslist = []
eventnames = []
eventdata = []




client = MongoClient()

timestart = time.time()
print("Started at: ", timestart)


#  START
for fighterlink in client.ufcstats.fighterlinks.find():
  fighterpage = requests.get(fighterlink['url'])
  soup = BeautifulSoup(fighterpage.content, "html.parser")

  

  for event in soup.find_all('a', {"class": "b-link_style_black"}):
    link = str(event.get('href'))
    text = str(event.get_text())
    text = text.strip()
    match = re.search("(?P<url>https?://ufcstats.com/event-details/.+)", link)
    if match is not None and match.group('url') not in eventslist:
      eventslist.append(match.group('url'))
      eventnames.append(text)
      print("Appended event: ", text)
    else:
      print("Event already in list: ", text)


for x in range(0, len(eventslist)):
  eventid = (re.search("(?s).*?event-details/(.*)", eventslist[x])).group(1)
  event = {'_id': eventid, 'human_id': len(eventslist)-x, 'name': eventnames[x], 'url': eventslist[x]}
  eventdata.append(event)
  print('Generated entry for event: ', eventnames[x]) 

print(eventdata)


# END
client = MongoClient()
# client.ufcstats.completeevents.drop()
client.ufcstats.completeevents.insert_many(eventdata)



print("Event Data Inserted")

timefinish = time.time()
timecomplete = timefinish - timestart
print(f"It took {timecomplete} seconds to complete")