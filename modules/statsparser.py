import re

# stat = ['0', '0', '26 of 41', '25 of 47', '63%', '53%', '26 of 41', '25 of 47', '0 of 0', '0 of 0', '---', '---', '0', '0', '0', '0', '0:00', '0:00', '0', '0', '19 of 25', '15 of 26', '76%', '57%', '19 of 25', '15 of 26', '0 of 0', '0 of 0', '---', '---', '0', '0', '0', '0', '0:00', '0:00', '0', '0', '7 of 16', '10 of 21', '43%', '47%', '7 of 16', '10 of 21', '0 of 0', '0 of 0', '---', '---', '0', '0', '0', '0', '0:00', '0:00', '26 of 41', '25 of 47', '63%', '53%', '0 of 9', '14 of 30', '0 of 2', '8 of 14', '26 of 30', '3 of 3', '26 of 41', '25 of 47', '0 of 0', '0 of 0', '0 of 0', '0 of 0', '19 of 25', '15 of 26', '76%', '57%', '0 of 3', '7 of 13', '0 of 0', '5 of 10', '19 of 22', '3 of 3', '19 of 25', '15 of 26', '0 of 0', '0 of 0', '0 of 0', '0 of 0', '7 of 16', '10 of 21', '43%', '47%', '0 of 6', '7 of 17', '0 of 2', '3 of 4', '7 of 8', '0 of 0', '7 of 16', '10 of 21', '0 of 0', '0 of 0', '0 of 0', '0 of 0']

stat = ['0', '0', '116 of 230', '90 of 157', '50%', '57%', '163 of 277', '141 of 217', '0 of 0', '0 of 4', '---', '0%', '0', '0', '0', '0', '0:00', '4:14', '0', '0', '22 of 48', '18 of 28', '45%', '64%', '22 of 48', '18 of 28', '0 of 0', '0 of 0', '---', '---', '0', '0', '0', '0', '0:00', '0:00', '0', '0', '28 of 48', '19 of 31', '58%', '61%', '28 of 48', '19 of 31', '0 of 0', '0 of 0', '---', '---', '0', '0', '0', '0', '0:00', '0:00', '0', '0', '17 of 35', '17 of 36', '48%', '47%', '35 of 53', '38 of 62', '0 of 0', '0 of 2', '---', '0%', '0', '0', '0', '0', '0:00', '1:29', '0', '0', '24 of 45', '16 of 36', '53%', '44%', '40 of 61', '31 of 55', '0 of 0', '0 of 1', '---', '0%', '0', '0', '0', '0', '0:00', '1:18', '0', '0', '25 of 54', '20 of 26', '46%', '76%', '38 of 67', '35 of 41', '0 of 0', '0 of 1', '---', '0%', '0', '0', '0', '0', '0:00', '1:27', '116 of 230', '90 of 157', '50%', '57%', '60 of 165', '36 of 89', '26 of 31', '32 of 40', '30 of 34', '22 of 28', '114 of 226', '78 of 143', '2 of 4', '12 of 14', '0 of 0', '0 of 0', '22 of 48', '18 of 28', '45%', '64%', '7 of 29', '1 of 6', '6 of 8', '6 of 8', '9 of 11', '11 of 14', '22 of 48', '18 of 28', '0 of 0', '0 of 0', '0 of 0', '0 of 0', '28 of 48', '19 of 31', '58%', '61%', '12 of 32', '6 of 15', '9 of 9', '9 of 11', '7 of 7', '4 of 5', '28 of 47', '19 of 31', '0 of 1', '0 of 0', '0 of 0', '0 of 0', '17 of 35', '17 of 36', '48%', '47%', '9 of 26', '7 of 22', '4 of 4', '6 of 8', '4 of 5', '4 of 6', '17 of 34', '9 of 27', '0 of 1', '8 of 9', '0 of 0', '0 of 0', '24 of 45', '16 of 36', '53%', '44%', '15 of 34', '8 of 27', '5 of 7', '6 of 7', '4 of 4', '2 of 2', '24 of 45', '14 of 33', '0 of 0', '2 of 3', '0 of 0', '0 of 0', '25 of 54', '20 of 26', '46%', '76%', '17 of 44', '14 of 19', '2 of 3', '5 of 6', '6 of 7', '1 of 1', '23 of 52', '18 of 24', '2 of 2', '2 of 2', '0 of 0', '0 of 0']

def statsparser(rounds, stats):
 
  fighterone = []
  fightertwo = []

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


  # print("stats: ", stats)
  # take only everything before :
  trimmed = re.search("^(.*)(?=:)", stats[16])
   # take only everything after :
  seconds = re.search("(?s).*?:(.*)", stats[16])
  # print("trimmed: ", trimmed)
  # print("seconds: ", seconds)
  if trimmed != None and seconds != None:
    time1 = int(trimmed.group(1)) * 60 + int(seconds.group(1))
  else:
    time1 = 0
  fighterone.append(time1) # CTRL in seconds

  # take only everything before :
  trimmed2 = re.search("^(.*)(?=:)", stats[17])
  seconds2 = re.search("(?s).*?:(.*)", stats[17])
  if trimmed2 != None and seconds2 != None:
    time2 = int(trimmed2.group(1)) * 60 + int(seconds2.group(1))
  else:
    time2 = 0
  fightertwo.append(time2) # CTRL in seconds
  
  x = 18 + 18 * rounds + 4
  y = 19 + 18 * rounds + 4
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
  # basic math to compute defensive stats
  trimmed = re.search("^(.*)(?= of)", stats[2])
  trimmed2 = re.search("^(.*)(?= of)", stats[3])
   # take only everything after of
  trimmed3 = re.search("(?s).*?of(.*)", stats[2])
  trimmed4 = re.search("(?s).*?of(.*)", stats[3])
  fighterone.append(int(trimmed4.group(1)[1:])-int(trimmed2.group(1))) # SSD
  fightertwo.append(int(trimmed3.group(1)[1:])-int(trimmed.group(1))) # SSD
   # take only everything after of
  trimmed3 = re.search("(?s).*?of(.*)", stats[2])
  trimmed4 = re.search("(?s).*?of(.*)", stats[3])
  fighterone.append(int(trimmed4.group(1)[1:])) # SSR
  fightertwo.append(int(trimmed3.group(1)[1:])) # SSR
  # basic math to compute defensive stats
  trimmed = re.search("^(.*)(?= of)", stats[8])
  trimmed2 = re.search("^(.*)(?= of)", stats[9])
   # take only everything after of
  trimmed3 = re.search("(?s).*?of(.*)", stats[8])
  trimmed4 = re.search("(?s).*?of(.*)", stats[9])
  fighterone.append(int(trimmed4.group(1)[1:])-int(trimmed2.group(1))) # TDD
  fightertwo.append(int(trimmed3.group(1)[1:])-int(trimmed.group(1))) # TDD
  fighterone.append(int(trimmed4.group(1)[1:])) # TDR
  fightertwo.append(int(trimmed3.group(1)[1:])) # TDR
  fighterone.append(int(stats[15])) # REVD
  fightertwo.append(int(stats[14])) # REVD

  # take only everything before :
  trimmed = re.search("^(.*)(?=:)", stats[16])
   # take only everything after :
  seconds = re.search("(?s).*?:(.*)", stats[16])
  if trimmed != None and seconds != None:
    time1 = int(trimmed.group(1)) * 60 + int(seconds.group(1))
  else:
    time1 = 0
  fightertwo.append(time1) # CTRLED in seconds

  # take only everything before :
  trimmed2 = re.search("^(.*)(?=:)", stats[17])
  seconds2 = re.search("(?s).*?:(.*)", stats[17])
  if trimmed2 != None and seconds2 != None:
    time2 = int(trimmed2.group(1)) * 60 + int(seconds2.group(1))
  else:
    time2 = 0
  fighterone.append(time2) # CTRLED in seconds


  x = 18 + 18 * rounds + 4
  y = 19 + 18 * rounds + 4
  # take only everything before of
  trimmed = re.search("^(.*)(?= of)", stats[x])
  trimmed2 = re.search("^(.*)(?= of)", stats[y])
  # take only everything after of
  trimmed3 = re.search("(?s).*?of(.*)", stats[x])
  trimmed4 = re.search("(?s).*?of(.*)", stats[y])
  fighterone.append(int(trimmed4.group(1)[1:])-int(trimmed2.group(1))) # HSD
  fightertwo.append(int(trimmed3.group(1)[1:])-int(trimmed.group(1))) # HSD
  # take only everything after of
  trimmed3 = re.search("(?s).*?of(.*)", stats[x])
  trimmed4 = re.search("(?s).*?of(.*)", stats[y])
  fighterone.append(int(trimmed4.group(1)[1:])) # HSR
  fightertwo.append(int(trimmed3.group(1)[1:])) # HSR
  
  x = x + 2
  y = y + 2
   # take only everything before of
  trimmed = re.search("^(.*)(?= of)", stats[x])
  trimmed2 = re.search("^(.*)(?= of)", stats[y])
  # take only everything after of
  trimmed3 = re.search("(?s).*?of(.*)", stats[x])
  trimmed4 = re.search("(?s).*?of(.*)", stats[y])
  fighterone.append(int(trimmed4.group(1)[1:])-int(trimmed2.group(1))) # BSD
  fightertwo.append(int(trimmed3.group(1)[1:])-int(trimmed.group(1))) # BSD
  # take only everything after of
  trimmed3 = re.search("(?s).*?of(.*)", stats[x])
  trimmed4 = re.search("(?s).*?of(.*)", stats[y])
  fighterone.append(int(trimmed4.group(1)[1:])) # BSR
  fightertwo.append(int(trimmed3.group(1)[1:])) # BSR
  
  x = x + 2
  y = y + 2
  # take only everything before of
  trimmed = re.search("^(.*)(?= of)", stats[x])
  trimmed2 = re.search("^(.*)(?= of)", stats[y])
  # take only everything after of
  trimmed3 = re.search("(?s).*?of(.*)", stats[x])
  trimmed4 = re.search("(?s).*?of(.*)", stats[y])
  fighterone.append(int(trimmed4.group(1)[1:])-int(trimmed2.group(1))) # LSD
  fightertwo.append(int(trimmed3.group(1)[1:])-int(trimmed.group(1))) # LSD
  # take only everything after of
  trimmed3 = re.search("(?s).*?of(.*)", stats[x])
  trimmed4 = re.search("(?s).*?of(.*)", stats[y])
  fighterone.append(int(trimmed4.group(1)[1:])) # LSR
  fightertwo.append(int(trimmed3.group(1)[1:])) # LSR
  x = x + 2
  y = y + 2
  # take only everything before of
  trimmed = re.search("^(.*)(?= of)", stats[x])
  trimmed2 = re.search("^(.*)(?= of)", stats[y])
  # take only everything after of
  trimmed3 = re.search("(?s).*?of(.*)", stats[x])
  trimmed4 = re.search("(?s).*?of(.*)", stats[y])
  fighterone.append(int(trimmed4.group(1)[1:])-int(trimmed2.group(1))) # DSD
  fightertwo.append(int(trimmed3.group(1)[1:])-int(trimmed.group(1))) # DSD
  # take only everything after of
  trimmed3 = re.search("(?s).*?of(.*)", stats[x])
  trimmed4 = re.search("(?s).*?of(.*)", stats[y])
  fighterone.append(int(trimmed4.group(1)[1:])) # DSR
  fightertwo.append(int(trimmed3.group(1)[1:])) # DSR
  x = x + 2
  y = y + 2
  # take only everything before of
  trimmed = re.search("^(.*)(?= of)", stats[x])
  trimmed2 = re.search("^(.*)(?= of)", stats[y])
  # take only everything after of
  trimmed3 = re.search("(?s).*?of(.*)", stats[x])
  trimmed4 = re.search("(?s).*?of(.*)", stats[y])
  fighterone.append(int(trimmed4.group(1)[1:])-int(trimmed2.group(1))) # CSD
  fightertwo.append(int(trimmed3.group(1)[1:])-int(trimmed.group(1))) # CSD
  # take only everything after of
  trimmed3 = re.search("(?s).*?of(.*)", stats[x])
  trimmed4 = re.search("(?s).*?of(.*)", stats[y])
  fighterone.append(int(trimmed4.group(1)[1:])) # CSR
  fightertwo.append(int(trimmed3.group(1)[1:])) # CSR
  x = x + 2
  y = y + 2
  # take only everything before of
  trimmed = re.search("^(.*)(?= of)", stats[x])
  trimmed2 = re.search("^(.*)(?= of)", stats[y])
  # take only everything after of
  trimmed3 = re.search("(?s).*?of(.*)", stats[x])
  trimmed4 = re.search("(?s).*?of(.*)", stats[y])
  fighterone.append(int(trimmed4.group(1)[1:])-int(trimmed2.group(1))) # GSD
  fightertwo.append(int(trimmed3.group(1)[1:])-int(trimmed.group(1))) # GSD
  # take only everything after of
  trimmed3 = re.search("(?s).*?of(.*)", stats[x])
  trimmed4 = re.search("(?s).*?of(.*)", stats[y])
  fighterone.append(int(trimmed4.group(1)[1:])) # GSR
  fightertwo.append(int(trimmed3.group(1)[1:])) # GSR


  # print(len(fighterone))
  # print(len(fightertwo))

    
  fightobj = {'fighter1': fighterone, 'fighter2': fightertwo}

  # print(fightobj)

  return fightobj

