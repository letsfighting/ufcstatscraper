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

client = MongoClient()

def entrymaker(fightid, year, fighter1, fighter2):
  
  queryf1 = fighter1+str(year)
  queryf2 = fighter2+str(year)

  print('queryf1: '+queryf1)
  print('queryf2: '+queryf2)
  

  profilef1 = client.ufcstats.allcumulativefightstatsbyyear.find_one({"_id":queryf1})
  profilef2 = client.ufcstats.allcumulativefightstatsbyyear.find_one({"_id":queryf2})

  print('profilef1: ',profilef1)
  print('profilef2: ',profilef2)


entrymaker('b96c8fef6c9f92db', 2010, 'abc6b5745335f18', '757c06bbdba61d2')