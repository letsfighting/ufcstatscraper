import re

stat = ['0', '0', '26 of 41', '25 of 47', '63%', '53%', '26 of 41', '25 of 47', '0 of 0', '0 of 0', '---', '---', '0', '0', '0', '0', '0:00', '0:00', '0', '0', '19 of 25', '15 of 26', '76%', '57%', '19 of 25', '15 of 26', '0 of 0', '0 of 0', '---', '---', '0', '0', '0', '0', '0:00', '0:00', '0', '0', '7 of 16', '10 of 21', '43%', '47%', '7 of 16', '10 of 21', '0 of 0', '0 of 0', '---', '---', '0', '0', '0', '0', '0:00', '0:00', '26 of 41', '25 of 47', '63%', '53%', '0 of 9', '14 of 30', '0 of 2', '8 of 14', '26 of 30', '3 of 3', '26 of 41', '25 of 47', '0 of 0', '0 of 0', '0 of 0', '0 of 0', '19 of 25', '15 of 26', '76%', '57%', '0 of 3', '7 of 13', '0 of 0', '5 of 10', '19 of 22', '3 of 3', '19 of 25', '15 of 26', '0 of 0', '0 of 0', '0 of 0', '0 of 0', '7 of 16', '10 of 21', '43%', '47%', '0 of 6', '7 of 17', '0 of 2', '3 of 4', '7 of 8', '0 of 0', '7 of 16', '10 of 21', '0 of 0', '0 of 0', '0 of 0', '0 of 0']

def statsparser1(rounds, stats):
 
  fighterone = []
  fightertwo = []
  
  if rounds == 2:
    fighterone.append(int(stats[0])) # KD
    fightertwo.append(int(stats[1])) # KD

     # take only everything before of
    trimmed = re.search("^(.*)(?= of)", stats[2])
    fighterone.append(int(trimmed.group(1))) # SS
    trimmed2 = re.search("^(.*)(?= of)", stats[3])
    fightertwo.append(int(trimmed2.group(1))) # SS

    # take only everything after of
    trimmed = re.search("(?s).*?of(.*)", stats[2])
    # shave off first character
    fighterone.append(int(trimmed.group(1)[1:])) # SSA
    # take only everything after of
    trimmed2 = re.search("(?s).*?of(.*)", stats[3])
    # shave off first character
    fightertwo.append(int(trimmed2.group(1)[1:])) # SSA

    # take only everything before of
    trimmed = re.search("^(.*)(?= of)", stats[8])
    fighterone.append(int(trimmed.group(1))) # TD
     # take only everything before of
    trimmed2 = re.search("^(.*)(?= of)", stats[9])
    fightertwo.append(int(trimmed2.group(1))) # TD

     # take only everything after of
    trimmed = re.search("(?s).*?of(.*)", stats[8])
    # shave off first character
    fighterone.append(int(trimmed.group(1)[1:])) # TDA
     # take only everything after of
    trimmed2 = re.search("(?s).*?of(.*)", stats[9])
    # shave off first character
    fightertwo.append(int(trimmed2.group(1)[1:])) # TDA

    fighterone.append(int(stats[12])) # SUBATT
    fightertwo.append(int(stats[13])) # SUBATT

    fighterone.append(int(stats[14])) # REV
    fightertwo.append(int(stats[15])) # REV

    # take only everything before :
    trimmed = re.search("^(.*)(?=:)", stats[16])
    fighterone.append(int(trimmed.group(1))) # CTRL in minutes
    # take only everything before :
    trimmed2 = re.search("^(.*)(?=:)", stats[17])
    fightertwo.append(int(trimmed2.group(1))) # CTRL in minutes
    

     # take only everything before :
    trimmed = re.search("^(.*)(?=:)", stats[17])
    fighterone.append(int(trimmed.group(1))) # BTM in minutes
    trimmed2 = re.search("^(.*)(?=:)", stats[16])
    fightertwo.append(int(trimmed2.group(1))) # CTRL in minutes

    x = 18 + 18 * rounds + 4
    y = 19 + 18 * rounds + 4

    print(stats[x])

     # take only everything before of
    trimmed = re.search("^(.*)(?= of)", stats[x])
    fighterone.append(int(trimmed.group(1))) # HS 
    trimmed2 = re.search("^(.*)(?= of)", stats[y])
    fightertwo.append(int(trimmed2.group(1))) # HS


    # take only everything after of
    trimmed = re.search("(?s).*?of(.*)", stats[x])
    # shave off first character
    fighterone.append(int(trimmed.group(1)[1:])) # HSA
    # take only everything after of
    trimmed2 = re.search("(?s).*?of(.*)", stats[y])
    # shave off first character
    fightertwo.append(int(trimmed2.group(1)[1:])) # HSA
    
    x = x + 2
    y = y + 2

     # take only everything before of
    trimmed = re.search("^(.*)(?= of)", stats[x])
    fighterone.append(int(trimmed.group(1))) # BS 
    trimmed2 = re.search("^(.*)(?= of)", stats[y])
    fightertwo.append(int(trimmed2.group(1))) # BS

    # take only everything after of
    trimmed = re.search("(?s).*?of(.*)", stats[x])
    # shave off first character
    fighterone.append(int(trimmed.group(1)[1:])) # BSA
    # take only everything after of
    trimmed2 = re.search("(?s).*?of(.*)", stats[y])
    # shave off first character
    fightertwo.append(int(trimmed2.group(1)[1:])) # BSA
    
    x = x + 2
    y = y + 2

     # take only everything before of
    trimmed = re.search("^(.*)(?= of)", stats[x])
    fighterone.append(int(trimmed.group(1))) # LS 
    trimmed2 = re.search("^(.*)(?= of)", stats[y])
    fightertwo.append(int(trimmed2.group(1))) # LS

    # take only everything after of
    trimmed = re.search("(?s).*?of(.*)", stats[x])
    # shave off first character
    fighterone.append(int(trimmed.group(1)[1:])) # LSA
    # take only everything after of
    trimmed2 = re.search("(?s).*?of(.*)", stats[y])
    # shave off first character
    fightertwo.append(int(trimmed2.group(1)[1:])) # LSA

    x = x + 2
    y = y + 2

     # take only everything before of
    trimmed = re.search("^(.*)(?= of)", stats[x])
    fighterone.append(int(trimmed.group(1))) # DS 
    trimmed2 = re.search("^(.*)(?= of)", stats[y])
    fightertwo.append(int(trimmed2.group(1))) # DS

    # take only everything after of
    trimmed = re.search("(?s).*?of(.*)", stats[x])
    # shave off first character
    fighterone.append(int(trimmed.group(1)[1:])) # DSA
    # take only everything after of
    trimmed2 = re.search("(?s).*?of(.*)", stats[y])
    # shave off first character
    fightertwo.append(int(trimmed2.group(1)[1:])) # DSA

    x = x + 2
    y = y + 2

     # take only everything before of
    trimmed = re.search("^(.*)(?= of)", stats[x])
    fighterone.append(int(trimmed.group(1))) # CS 
    trimmed2 = re.search("^(.*)(?= of)", stats[y])
    fightertwo.append(int(trimmed2.group(1))) # CS

    # take only everything after of
    trimmed = re.search("(?s).*?of(.*)", stats[x])
    # shave off first character
    fighterone.append(int(trimmed.group(1)[1:])) # CSA
    # take only everything after of
    trimmed2 = re.search("(?s).*?of(.*)", stats[y])
    # shave off first character
    fightertwo.append(int(trimmed2.group(1)[1:])) # CSA

    x = x + 2
    y = y + 2

     # take only everything before of
    trimmed = re.search("^(.*)(?= of)", stats[x])
    fighterone.append(int(trimmed.group(1))) # GS 
    trimmed2 = re.search("^(.*)(?= of)", stats[y])
    fightertwo.append(int(trimmed2.group(1))) # GS

    # take only everything after of
    trimmed = re.search("(?s).*?of(.*)", stats[x])
    # shave off first character
    fighterone.append(int(trimmed.group(1)[1:])) # GSA
    # take only everything after of
    trimmed2 = re.search("(?s).*?of(.*)", stats[y])
    # shave off first character
    fightertwo.append(int(trimmed2.group(1)[1:])) # GSA

    fighterone.append(int(stats[1])) # Downed
    fightertwo.append(int(stats[0])) # Downed

    trimmed = re.search("^(.*)(?= of)", stats[2])
   
    trimmed2 = re.search("^(.*)(?= of)", stats[3])
 
    # take only everything after of
    trimmed3 = re.search("(?s).*?of(.*)", stats[2])
    # take only everything after of
    trimmed4 = re.search("(?s).*?of(.*)", stats[3])

    fighterone.append(int(trimmed4.group(1)[1:])-int(trimmed2.group(1))) # SSD
    fightertwo.append(int(trimmed3.group(1)[1:])-int(trimmed.group(1))) # SSD


    print(fighterone)
    print(fightertwo)

statsparser1(2, stat)