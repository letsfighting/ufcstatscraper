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



mclient = MongoClient()
# mclient.ufcstats.fightdetails.drop()
# mclient.ufcstats.fightstats.drop()
timestart = time.time()
print("Started at: ", timestart)

for fighter in mclient.ufcstats.fighters.find():
    print("fightername: ", fighter['name'], ", fighterid: ", fighter['_id'])


timefinish = time.time()
timecomplete = timefinish - timestart
print(f"It took {timecomplete} seconds to complete")
