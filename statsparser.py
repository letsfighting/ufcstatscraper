import re

stat = ['0', '0', '26 of 41', '25 of 47', '63%', '53%', '26 of 41', '25 of 47', '0 of 0', '0 of 0', '---', '---', '0', '0', '0', '0', '0:00', '0:00', '0', '0', '19 of 25', '15 of 26', '76%', '57%', '19 of 25', '15 of 26', '0 of 0', '0 of 0', '---', '---', '0', '0', '0', '0', '0:00', '0:00', '0', '0', '7 of 16', '10 of 21', '43%', '47%', '7 of 16', '10 of 21', '0 of 0', '0 of 0', '---', '---', '0', '0', '0', '0', '0:00', '0:00', '26 of 41', '25 of 47', '63%', '53%', '0 of 9', '14 of 30', '0 of 2', '8 of 14', '26 of 30', '3 of 3', '26 of 41', '25 of 47', '0 of 0', '0 of 0', '0 of 0', '0 of 0', '19 of 25', '15 of 26', '76%', '57%', '0 of 3', '7 of 13', '0 of 0', '5 of 10', '19 of 22', '3 of 3', '19 of 25', '15 of 26', '0 of 0', '0 of 0', '0 of 0', '0 of 0', '7 of 16', '10 of 21', '43%', '47%', '0 of 6', '7 of 17', '0 of 2', '3 of 4', '7 of 8', '0 of 0', '7 of 16', '10 of 21', '0 of 0', '0 of 0', '0 of 0', '0 of 0']

def statsparser1(rounds, stats):
 
  fighterone = []
  fightertwo = []
  
  if rounds == 2:
    fighterone.append(stats[0]) # KD
    fightertwo.append(stats[1]) # KD

     # take only everything before of
    trimmed = re.search("^(.*)(?=of)", stats[2])
    fighterone.append(trimmed.group(1)) # SS
    trimmed2 = re.search("^(.*)(?=of)", stats[3])
    fightertwo.append(trimmed2.group(1)) # SS

    # take only everything after of
    trimmed = re.search("(?s).*?of(.*)", stats[2])
    # shave off first character
    fighterone.append(trimmed.group(1)[1:]) # SSA
    # take only everything after of
    trimmed2 = re.search("(?s).*?of(.*)", stats[3])
    # shave off first character
    fightertwo.append(trimmed2.group(1)[1:]) # SSA

    # take only everything before of
    trimmed = re.search("^(.*)(?=of)", stats[8])
    fighterone.append(trimmed.group(1)) # TD
     # take only everything before of
    trimmed2 = re.search("^(.*)(?=of)", stats[9])
    fightertwo.append(trimmed2.group(1)) # TD

     # take only everything after of
    trimmed = re.search("(?s).*?of(.*)", stats[8])
    # shave off first character
    fighterone.append(trimmed.group(1)[1:]) # TDA
     # take only everything after of
    trimmed2 = re.search("(?s).*?of(.*)", stats[9])
    # shave off first character
    fightertwo.append(trimmed2.group(1)[1:]) # TDA

    fighterone.append(stats[12]) # SUBATT
    fightertwo.append(stats[13]) # SUBATT

    fighterone.append(stats[14]) # REV
    fightertwo.append(stats[15]) # REV

    # take only everything before :
    trimmed = re.search("^(.*)(?=:)", stats[16])
    fighterone.append(trimmed.group(1)) # CTRL in minutes
    # take only everything before :
    trimmed2 = re.search("^(.*)(?=:)", stats[17])
    fightertwo.append(trimmed2.group(1)) # CTRL in minutes
    

     # take only everything before :
    trimmed = re.search("^(.*)(?=:)", stats[17])
    fighterone.append(trimmed.group(1)) # BTM in minutes
    trimmed2 = re.search("^(.*)(?=:)", stats[16])
    fightertwo.append(trimmed2.group(1)) # CTRL in minutes

    x = 18 + 18 * rounds + 4
    y = 19 + 18 * rounds + 5

    print(stats[x])

    

    print(fighterone)
    print(fightertwo)

statsparser1(2, stat)