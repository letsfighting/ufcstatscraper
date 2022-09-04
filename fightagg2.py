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
    totalmatches = 0
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
    wdq = 0
    uxoutcome = 0
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



    for entry in client.ufcstats.allfightstats.find({ "fighter_id": fighterid, "year": { "$lt": year }, "stats_available": True }):
        print('entry: ', entry)
        totalmatches += 1

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
        elif entry['outcome'] == 'L':
            losses += 1
            if entry['method'] == 'KO/TKO':
                lko += 1
            elif entry['method'] == 'Submission':
                lsub += 1
            elif entry['method'] == 'DQ':
                ldq += 1
            else:
                ldec += 1
        elif entry['outcome'] == 'D':
            draws += 1
        elif entry['outcome'] == 'NC':
            ncs += 1
        else:
            uxoutcome += 1

        rounds_fought += entry['rounds_fought']
        duration += entry['duration']
        KD += entry['KD']
        SS += entry['SS']
        SSA += entry['SSA']
        TD += entry['TD']
        TDA += entry['TDA']
        SUBATT += entry['SUBATT']
        REV += entry['REV']
        CTRL += entry['CTRL']
        HS += entry['HS']
        HSA += entry['HSA']
        BS += entry['BS']
        BSA += entry['BSA']
        LS += entry['LS']
        LSA += entry['LSA']
        DS += entry['DS']
        DSA += entry['DSA']
        CS += entry['CS']
        CSA += entry['CSA']
        GS += entry['GS']
        GSA += entry['GSA']
        Downed += entry['Downed']
        SSD += entry['SSD']
        SSR += entry['SSR']
        TDD += entry['TDD']
        TDR += entry['TDR']
        SUBATTR += entry['SUBATTR']
        REVED += entry['REVED']
        CTRLED += entry['CTRLED']
        HSD += entry['HSD']
        HSR += entry['HSR']
        BSD += entry['BSD']
        BSR += entry['BSR']
        LSD += entry['LSD']
        LSR += entry['LSR']
        DSD += entry['DSD']
        DSR += entry['DSR']
        CSD += entry['CSD']
        CSR += entry['CSR']
        GSD += entry['GSD']
        GSR += entry['GSR']

    x = client.ufcstats.fighters.find_one({ "_id": fighterid })
    fightername = x['name']
    # print('fightername: ', fighterid+str(year))
    
    # y = client.ufcstats.fightstats.find_one({ "fighter_id": fighterid, "year": year, "stats_available": True })

    # print('y: ', y)

    if client.ufcstats.allfightstats.find_one({ "fighter_id": fighterid, "year": { "$lt": year }, "stats_available": True }) is not None:

        finalentry = {'_id': fighterid + str(year-1), 'name': fightername, 'year': year-1, 'totalmatches': totalmatches, 'wins': wins, 'losses': losses, 'draws': draws, 'ncs': ncs, 'wko': wko, 'wdq': wdq, 'wdec': wdec, 'ldq': ldq, 'ldec': ldec, 'lko': lko, 'wsub': wsub, 'lsub': lsub, 'wdq': wdq, 'uxoutcome': uxoutcome, 'rounds_fought': rounds_fought, 'duration': duration, 'KD': KD, 'SS': SS, 'SSA': SSA, 'TD': TD, 'TDA': TDA, 'SUBATT': SUBATT, 'REV': REV, 'CTRL': CTRL, 'HS': HS, 'HSA': HSA, 'BS': BS, 'BSA': BSA, 'LS': LS, 'LSA': LSA, 'DS': DS, 'DSA': DSA, 'CS': CS, 'CSA': CSA, 'GS': GS, 'GSA': GSA, 'Downed': Downed, 'SSD': SSD, 'SSR': SSR, 'TDD': TDD, 'TDR': TDR, 'SUBATT': SUBATT, 'REVED': REVED, 'CTRLED': CTRLED, 'HSD': HSD, 'HSR': HSR, 'BSD': BSD, 'BSR': BSR, 'LSD': LSD, 'LSR': LSR, 'DSD': DSD, 'DSR': DSR, 'CSD': CSD, 'CSR': CSR, 'GSD': GSD, 'GSR': GSR}    
        client.ufcstats.allcumulativefightstatsbyyear.insert_one(finalentry)
        print('Entry Inserted for ', fightername, ' in ', year-1)
    else:
        print('No Entry Found for ', fightername, ' in ', year-1)
            
            



mclient = MongoClient()

timestart = time.time()
print("Started at: ", timestart)

mclient.ufcstats.allcumulativefightstatsbyyear.drop()

for fighter in mclient.ufcstats.fighters.find():
    year = 1993
    while year < 2024:
        print("Processing: ", fighter['name'], ", Year: ", year-1)
        fightstatsquery(fighter['_id'], year)
        year += 1

# fightstatsquery('babc6b5745335f18', 2011)


timefinish = time.time()
timecomplete = timefinish - timestart
print(f"It took {timecomplete} seconds to complete")
