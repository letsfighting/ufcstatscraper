from curses import ncurses_version
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


def fightstatsquery(fighterid, year):
    client = MongoClient()
    wins = 0
    losses = 0
    draws = 0
    ncs = 0
    wko = 0
    wdq = 0
    wdec = 0
    ldq = 0
    ldec = 0
    lko = 0
    wsub = 0 
    lsub = 0
    dq = 0
    rounds_fought = 0
    duration = 0
    KD = 0
    SS = 0
    SSA = 0
    TD = 0
    TDA = 0
    SUBATT = 0
    REV = 0
    CTRL = 0
    HS = 0
    HSA = 0
    BS = 0
    BSA = 0
    LS = 0
    LSA = 0
    DS = 0
    DSA = 0
    CS = 0
    CSA = 0
    GS = 0
    GSA = 0
    Downed = 0
    SSD = 0
    SSR = 0
    TDD = 0
    TDR = 0
    REVED = 0
    CTRLED = 0
    HSD = 0
    HSR = 0
    BSD = 0
    BSR = 0
    LSD = 0
    LSR = 0
    DSD = 0
    DSR = 0
    CSD = 0
    CSR = 0
    GSD = 0
    GSR = 0



    for entry in client.ufcstats.fightstats.find({ "fighter_id": fighterid, "year": { "$lt": year }, "stats_available": True }):
        print('entry: ', entry)
        if entry['outcome'] == 'W':
            wins += 1
            if entry['method'] == 'KO/TKO':
                wko += 1
            elif entry['method'] == 'Submission':
                wsub += 1
            elif entry['method'] == 'DQ':
                wdq += 1
            else:
                wdec += 1
            
            



mclient = MongoClient()
# mclient.ufcstats.fightdetails.drop()
# mclient.ufcstats.fightstats.drop()
timestart = time.time()
print("Started at: ", timestart)

# for fighter in mclient.ufcstats.fighters.find():
#     print("fightername: ", fighter['name'], ", fighterid: ", fighter['_id'])

fightstatsquery("cd2c4d30c6e13b47", 2023)


timefinish = time.time()
timecomplete = timefinish - timestart
print(f"It took {timecomplete} seconds to complete")
