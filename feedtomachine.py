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

def entrymaker(fightid, year):
  
  method = 'pending'

  # allfightsquery = client.ufcstats.allfights.find({"_id": fightid})
  allfightdetailsquery = client.ufcstats.allfightdetails.find_one({"_id":fightid})
  fighter1 = allfightdetailsquery['fighter1_id']
  fighter2 = allfightdetailsquery['fighter2_id']
  queryf1 = fighter1+str(year)
  queryf2 = fighter2+str(year)

  # print('queryf1: '+queryf1)
  # print('queryf2: '+queryf2)
  

  profilef1 = client.ufcstats.allcumulativefightstatsbyyear.find_one({"_id":queryf1})
  profilef2 = client.ufcstats.allcumulativefightstatsbyyear.find_one({"_id":queryf2})

  bio1 = client.ufcstats.fighters.find_one({"_id":fighter1})
  bio2 = client.ufcstats.fighters.find_one({"_id":fighter2})
  winner = allfightdetailsquery['outcome']
  

  if allfightdetailsquery['method'] == 'KO' or allfightdetailsquery['method'] == 'TKO' or allfightdetailsquery['method'] == 'KO/TKO':
    method = 'KO/TKO'
  elif allfightdetailsquery['method'] == 'Submission':
    method = 'SUB'
  elif allfightdetailsquery['method'] == 'Overturned':
    method = 'OT'
  elif allfightdetailsquery['method'] == 'DQ':
    method = 'DQ'
  elif allfightdetailsquery['method'] == 'Decision - Split':
    method = 'SDEC'
  elif allfightdetailsquery['method'] == 'Decision - Unanimous':
    method = 'UDEC'
  elif allfightdetailsquery['method'] == 'Decision - Majority':
    method = 'MDEC'
  

  print('profilef1: ',profilef1)
  print('profilef2: ',profilef2)
  print('bio1: ',bio1)
  print('bio2: ',bio2)

  if profilef1 is None or profilef2 is None:
    print('No profile found for '+fighter1+' or '+fighter2)
    print('Investigate: ', fightid, ', ', fighter1, ', ', fighter2)
    client.ufcstats.taleofthetapeerrors.insert_one({"_id":fightid, "fighter1":fighter1, "fighter2":fighter2})
  else:
    entry = {'_id': fightid, 'year': year, 'fighter1_id': profilef1['_id'], 'fighter1_name': profilef1['name'], 'fighter2_id': profilef2['_id'], 'fighter2_name': profilef2['name'], 'winner': winner, 'weight_class': allfightdetailsquery['weight_class'], 'method': method, 'end_round': allfightdetailsquery['round_finish'], 'fighter1_wins': profilef1['wins'], 'fighter1_losses': profilef1['losses'], 'fighter1_draws': profilef1['draws'], 'fighter1_ncs': profilef1['ncs'], 'fighter1_wko': profilef1['wko'], 'fighter1_wsub': profilef1['wsub'], 'fighter1_wdec': profilef1['wdec'], 'fighter1_wdq': profilef1['wdq'], 'fighter1_lko': profilef1['lko'], 'fighter1_lko': profilef1['lsub'], 'fighter1_ldec': profilef1['ldec'], 'fighter1_ldq': profilef1['ldq'], 'fighter1_rounds_fought': profilef1['rounds_fought'], 'fighter1_total_time_fought': profilef1['duration'], 'fighter1_height': bio1['height'], 'fighter1_weight': bio1['weight'], 'fighter1_height': bio1['reach'], 'fighter1_reach': bio1['reach'], 'fighter1_stance': bio1['stance'], 'fighter1_birthyear': bio1['dob'], 'fighter1_KD': profilef1['KD'], 'fighter1_SS': profilef1['SS'], 'fighter1_SSA': profilef1['SSA'], 'fighter1_TD': profilef1['TD'], 'fighter1_TDA': profilef1['TDA'], 'fighter1_SUBATT': profilef1['SUBATT'], 'fighter1_REV': profilef1['REV'], 'fighter1_CTRL': profilef1['CTRL'], 'fighter1_HS': profilef1['HS'], 'fighter1_HSA': profilef1['HSA'], 'fighter1_BS': profilef1['BS'], 'fighter1_BSA': profilef1['BSA'], 'fighter1_LS': profilef1['LS'], 'fighter1_LSA': profilef1['LSA'], 'fighter1_DS': profilef1['DS'], 'fighter1_DSA': profilef1['DSA'], 'fighter1_CS': profilef1['CS'], 'fighter1_CSA': profilef1['CSA'], 'fighter1_GS': profilef1['GS'], 'fighter1_GSA': profilef1['GSA'], 'fighter1_DOWNED': profilef1['Downed'], 'fighter1_SSD': profilef1['SSD'], 'fighter1_SSR': profilef1['SSR'], 'fighter1_TDD': profilef1['TDD'], 'fighter1_TDR': profilef1['TDR'], 'fighter1_REVED': profilef1['REVED'], 'fighter1_CTRLED': profilef1['CTRLED'], 'fighter1_HSD': profilef1['HSD'], 'fighter1_HSR': profilef1['HSR'], 'fighter1_BSD': profilef1['BSD'], 'fighter1_BSR': profilef1['BSR'], 'fighter1_LSD': profilef1['LSD'], 'fighter1_LSR': profilef1['LSR'], 'fighter1_DSD': profilef1['DSD'], 'fighter1_DSR': profilef1['DSR'], 'fighter1_CSD': profilef1['CSD'], 'fighter1_CSR': profilef1['CSR'], 'fighter1_GSD': profilef1['GSD'], 'fighter1_GSR': profilef1['GSR'],
    'fighter2_wins': profilef2['wins'], 'fighter2_losses': profilef2['losses'], 'fighter2_draws': profilef2['draws'], 'fighter2_ncs': profilef2['ncs'], 'fighter2_wko': profilef2['wko'], 'fighter2_wsub': profilef2['wsub'], 'fighter2_wdec': profilef2['wdec'], 'fighter2_wdq': profilef2['wdq'], 'fighter2_lko': profilef2['lko'], 'fighter2_lko': profilef2['lsub'], 'fighter2_ldec': profilef2['ldec'], 'fighter2_ldq': profilef2['ldq'], 'fighter2_rounds_fought': profilef2['rounds_fought'], 'fighter2_total_time_fought': profilef2['duration'], 'fighter2_height': bio2['height'], 'fighter2_weight': bio2['weight'], 'fighter2_height': bio2['reach'], 'fighter2_reach': bio2['reach'], 'fighter2_stance': bio2['stance'], 'fighter2_birthyear': bio2['dob'], 'fighter2_KD': profilef2['KD'], 'fighter2_SS': profilef2['SS'], 'fighter2_SSA': profilef2['SSA'], 'fighter2_TD': profilef2['TD'], 'fighter2_TDA': profilef2['TDA'], 'fighter2_SUBATT': profilef2['SUBATT'], 'fighter2_REV': profilef2['REV'], 'fighter2_CTRL': profilef2['CTRL'], 'fighter2_HS': profilef2['HS'], 'fighter2_HSA': profilef2['HSA'], 'fighter2_BS': profilef2['BS'], 'fighter2_BSA': profilef2['BSA'], 'fighter2_LS': profilef2['LS'], 'fighter2_LSA': profilef2['LSA'], 'fighter2_DS': profilef2['DS'], 'fighter2_DSA': profilef2['DSA'], 'fighter2_CS': profilef2['CS'], 'fighter2_CSA': profilef2['CSA'], 'fighter2_GS': profilef2['GS'], 'fighter2_GSA': profilef2['GSA'], 'fighter2_DOWNED': profilef2['Downed'], 'fighter2_SSD': profilef2['SSD'], 'fighter2_SSR': profilef2['SSR'], 'fighter2_TDD': profilef2['TDD'], 'fighter2_TDR': profilef2['TDR'], 'fighter2_REVED': profilef2['REVED'], 'fighter2_CTRLED': profilef2['CTRLED'], 'fighter2_HSD': profilef2['HSD'], 'fighter2_HSR': profilef2['HSR'], 'fighter2_BSD': profilef2['BSD'], 'fighter2_BSR': profilef2['BSR'], 'fighter2_LSD': profilef2['LSD'], 'fighter2_LSR': profilef2['LSR'], 'fighter2_DSD': profilef2['DSD'], 'fighter2_DSR': profilef2['DSR'], 'fighter2_CSD': profilef2['CSD'], 'fighter2_CSR': profilef2['CSR'], 'fighter2_GSD': profilef2['GSD'], 'fighter2_GSR': profilef2['GSR']}
    
    client.ufcstats.taleofthetape.insert_one(entry)
    print("Entry Inserted: ", entry)


timestart = time.time()
print("Started at: ", timestart)


client.ufcstats.taleofthetape.drop()
client.ufcstats.taleofthetapeerrors.drop()

for fight in client.ufcstats.allfights.find():
  print('Processing:', fight['url'], ', Year: ', fight['year'])
  entrymaker(fight['_id'], fight['year'])


timefinish = time.time()
timecomplete = timefinish - timestart
print(f"It took {timecomplete} seconds to complete")