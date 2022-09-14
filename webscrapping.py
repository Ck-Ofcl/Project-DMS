# from bs4 import BeautifulSoup
# import requests
# req = requests.get(url)
# soup = BeautifulSoup(req.content, 'lxml')
import pandas as pd
from selenium import webdriver
import time
import pickle

from selenium.webdriver.common.by import By

driver = webdriver.Chrome('.\chromedriver.exe')
url3 = 'https://www.espncricinfo.com/series/caribbean-premier-league-2022-1320379/barbados-royals-vs-jamaica-tallawahs-14th-match-1323157/full-scorecard' ####### No mintes in battins stats
url2 = 'https://www.espncricinfo.com/series/new-zealand-in-australia-2022-1317459/australia-vs-new-zealand-3rd-odi-1317481/full-scorecard'
url1 = 'https://www.espncricinfo.com/series/india-in-zimbabwe-2022-1325547/zimbabwe-vs-india-3rd-odi-1325551/full-scorecard' ###### wicketkeeper skipper
url4 = 'https://www.espncricinfo.com/series/asia-cup-2022-1327237/hong-kong-vs-india-4th-match-group-a-1327272/full-scorecard'
url5 = 'https://www.espncricinfo.com/series/indian-premier-league-2022-1298423/gujarat-titans-vs-mumbai-indians-51st-match-1304097/full-scorecard'
url6 = 'https://www.espncricinfo.com/series/india-in-ireland-2022-1303299/ireland-vs-india-1st-t20i-1303307/full-scorecard' ###### IND VS IRE ########
driver.get(url6)
# time.sleep(1)

tab = driver.find_elements(By.TAG_NAME,'tbody')
entries  = []
for j in range(4):
    entries.append(tab[j].find_elements(By.TAG_NAME,'tr'))
# entry = tab[1].find_elements(By.TAG_NAME,'tr')
# for i in range(len(entries)):
#     print(entries[i])
#     for k in entries[i]:
#         print(k.text)
#         print('//////////////////////break //////////////')
# print(entry[0].text)
# st = []
# for i in range(4):
#     st[i] = tab[i].text
#     print(tab[i].text)
#     print('/////////////////////////////////////////////////////////////////////////////////')
# for i in entry:
#     head = i.find_element(By.TAG_NAME,'th').text
#     print(head)
# for i in bat_entry:
#     print(i.text)
# print(len(bat_entry))
# tables = driver.find_elements(By.CLASS_NAME,'ds-table-row-compact-bottom ds-border-none')
# print(tables)

################################  Player Class  ############################################

class player:

    def __init__(self,name):
        self.name,self.code_name,self.house,self.profile,self.credit = name,'','','',0
        self.r, self.b,self.fours,self.sixes,self.sr,self.thirt,self.fif,self.cent,self.o,self.M,self.w,self.eco,self.bwl,self.dro,self.rro,self.ca,self.dot = [0]*17

    def cal_score(self):
        score = 0
        score += int(self.r) + int(self.fours) + 2 * int(self.sixes) + 4 * int(self.thirt) + 8 * int(self.fif) + 16 * int(self.cent) + 12 * int(self.M) + 25 * int(self.w) + 8 * int(self.bwl) + 12 * int(self.dro) + 6 * int(self.rro) + 8 * int(self.ca)
        # score += 2*self.dot
        if float(self.b) >= 10:
            if float(self.sr) > 170:
                score += 6
            elif 150 < float(self.sr) <= 170:
                score += 4
            elif 130 <= float(self.sr) <= 150:
                score += 2
            elif 70 > float(self.sr) >= 60:
                score -= 2
            elif 60 > float(self.sr) >= 50:
                score -= 4
            elif float(self.sr) < 50:
                score -= 6
            else:
                score += 0
        if float(self.o) >= 2:
            if float(self.eco) < 5:
                score += 6
            elif 5 <= float(self.eco) < 6:
                score += 4
            elif 6 <= float(self.eco) < 7:
                score += 2
            elif 10 <= float(self.eco) < 11:
                score -= 2
            elif 11 <= float(self.eco) < 12:
                score -= 4
            elif float(self.eco) >= 12:
                score -= 6
            else:
                score += 0
        return score



########################## Script Patcher####################################

# for i in range(len(entries)):
#     for k in entries[i]:
#         print(k.text)
#         print('//////////////////////break //////////////')




def BatParser(inn):
    arr = []
    for i in entries[inn]:
        temp = i.text.split('\n')
        for j in temp:
            if j == '':
                pass
            elif j == ', ' or j == ' ':
                pass
            else:
                arr.append(j)
    return arr


array = [BatParser(i) for i in range(4)]

driver.close()
driver.quit()
# print(array)


def Batting(A,dt,res):
    mark = ''
    c = 0
    for i in range(len(A)):
        temp = A[i].split(' ')
        l = len(temp)
        a = ''
        if temp[0] != 'Extras':
            if temp[0] == 'c':
                pt = 1
                while temp[pt] != 'b':
                    a += temp[pt] + ' '
                    pt += 1

                if a[0] == '†':                       #### for wicketkeeper catch
                    a = a[1:-1]
                    res.append([a, 'c'])
                elif a == '&':
                    b = ''
                    for k in range(pt+1,l):
                        b += temp[k] + ' '
                    b = b[:-1]
                    res.append([b,'c'])
                else:
                    a = a[:-1]
                    res.append([a, 'c'])

            elif temp[0] == 'lbw':
                for k in range(2,l):
                    a += temp[k] + ' '
                a = a[:-1]
                res.append([a,'bwl'])

            elif temp[0] == 'st':
                a += temp[1][1:] + ' '
                pt = 2
                while temp[pt] != 'b':
                    a += temp[pt] + ' '
                    pt += 1
                a = a[:-1]
                res.append([a,'dro'])

            elif temp[0] == 'run':
                strg = temp[2]
                slh = strg.find('/')
                wk = strg.find('†')
                if slh == -1:          ##### if slash is not present ##########
                    if wk != -1:
                        a += strg[wk+1:-1]
                    else:
                        a += strg[1:-1]
                    res.append([a,'dro'])
                else:
                    a += strg[1:slh]
                    rro = strg[slh+1:-1]
                    if wk != -1:
                        if strg[1] == '†':
                            a = a[1:]
                        else:
                            rro = rro[1:]
                    res.append([a,'rro'])
                    res.append([rro,'rro'])

            elif temp[0] == 'not':
                dt[mark].b = int(temp[3])
                if l == 8:                                  ###### To deal with the case if Minutes spent also given in scorecard
                    dt[mark].fours = int(temp[5])
                    dt[mark].sixes = int(temp[6])
                    if temp[7] != '-':
                        dt[mark].sr = float(temp[7])
                else:
                    dt[mark].fours = int(temp[4])
                    dt[mark].sixes = int(temp[5])
                    if temp[6] != '-':
                        dt[mark].sr = float(temp[6])
                run = int(temp[2])
                dt[mark].r = run
                if run >= 30:
                    if 30 <= run < 50:
                        dt[mark].thirt += 1
                    elif 50 <= run < 100:
                        dt[mark].fif += 1
                    else:
                        dt[mark].cent += 1

            elif temp[0].isdigit():
                dt[mark].b = int(temp[1])
                if l == 6:
                    dt[mark].fours = int(temp[3])
                    dt[mark].sixes = int(temp[4])
                    if temp[5] != '-':
                        dt[mark].sr = float(temp[5])
                else:
                    dt[mark].fours = int(temp[2])
                    dt[mark].sixes = int(temp[3])
                    if temp[4] != '-':
                        dt[mark].sr = float(temp[4])
                run = int(temp[0])
                dt[mark].r = run
                if run >= 30:
                    if 30 <= run < 50:
                        dt[mark].thirt += 1
                    elif 50 <= run < 100:
                        dt[mark].fif += 1
                    else:
                        dt[mark].cent += 1

            elif temp[0] == 'b':
                for j in range(1,l):
                    a += temp[j] + ' '
                a = a[:-1]
                res.append([a,'bwl'])

            elif temp[0] == 'hit':
                pass

            else:
                a = A[i][:-1]
                s = A[i].find('(')
                wt = A[i].find('†')
                if s != -1 and wt != -1:
                    mn = min(s,wt)
                    a = A[i][:mn-1]
                else:
                    if s != -1:
                        a = A[i][:s-1]
                    if wt != -1:
                        a = A[i][:wt-1]
                if a not in dt:
                    dt[a] = player(a)
                mark = a

        else:
            c = i+5
            break

    if A[c] == 'Did not bat:':
        c += 1
        while A[c].find('Fall of wickets') == -1:
            s = A[c].find('(')
            wt = A[c].find('†')
            if s != -1 and wt != -1:
                mn = min(s,wt)
                A[c] = A[c][:mn-1]
            else:
                if s != -1:
                    A[c] = A[c][:s-1]
                if wt != -1:
                    A[c] = A[c][:wt-1]
            if A[c] not in dt:
                dt[A[c]] = player(A[c])
            c += 1

# Batting(array)
# for i in dt:
#     print(dt[i].name+'#')
#
# print(res)

def Balling(B,dt):
    mark = ''
    for i in range(len(B)):
        temp = B[i].split(' ')
        l = len(temp)
        if temp[0].isalpha():
            a = B[i]
            s = B[i].find('(')
            wt = B[i].find('†')
            if s != -1 and wt != -1:
                mn = min(s,wt)
                a = B[i][:mn-1]
            else:
                if s != -1:
                    a = B[i][:s-1]
                if wt != -1:
                    a = B[i][:wt-1]
            if a not in dt:
                dt[a] = player(a)
            mark = a

        elif temp[0].isdigit():
            if l == 1:
                dt[mark].w = int(temp[0])
            elif l == 3:
                dt[mark].o,dt[mark].M = float(temp[0]),int(temp[1])
            else:
                dt[mark].o,dt[mark].M,dt[mark].w,dt[mark].eco,dt[mark].dot = float(temp[0]),int(temp[1]),int(temp[3]),float(temp[4]),int(temp[5])
        else:
            if l == 3:
                dt[mark].o,dt[mark].M = float(temp[0]),int(temp[1])
            else:
                dt[mark].eco,dt[mark].dot = float(temp[0]),int(temp[1])

# Balling(array)
# for i in dt:
#     print(dt[i].name+'#',dt[i].eco)

def Fielding(dt,res):
    for i in res:
        for j in dt:
            f = j.find(i[0])
            if f == -1:
                pass
            else:
                w = i[1]
                if w == 'c': dt[j].ca +=1
                elif w == 'bwl' : dt[j].bwl += 1
                elif w == 'dro': dt[j].dro += 1
                else: dt[j].rro += 1

def StatsFinder(a,dct):
    dt = {}
    res = []
    Batting(array[0],dt,res)
    Batting(array[2],dt,res)
    Balling(array[1],dt)
    Balling(array[3],dt)
    Fielding(dt,res)
    u = dt['Josh Little']
    print(u.name,u.r,u.eco,u.w,u.bwl,u.o)
    print(len(dt))
    sheet = pd.read_excel(r"C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Player's Data\{}.xlsx".format(a))
    player_score = {}
    CodeNameToScr = {}
    for index,row in sheet.iterrows():
        nam = row[sheet.columns[0]]
        dt[nam].code_name,dt[nam].house,dt[nam].profile,dt[nam].credit = row[sheet.columns[1]],row[sheet.columns[2]],row[sheet.columns[3]],row[sheet.columns[4]]
        scr = dt[nam].cal_score()
        player_score[nam] = [dt[nam].house, dt[nam].profile, dt[nam].credit,scr, dt[nam].code_name]
        CodeNameToScr[dt[nam].code_name] = scr

    with open(r'C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Output Files\Players score Dict\{}'.format(dct), "wb") as myDct:
        pickle.dump(player_score, myDct)
    myDct.close()

    with open(r'C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Output Files\Players score Dict\CodeNameToScr', "wb") as dfct:
        pickle.dump(CodeNameToScr, dfct)
    dfct.close()

    print(player_score)
    print(CodeNameToScr)


StatsFinder('INDvsIREwebscrap', 'IvsZ')















