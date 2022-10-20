import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle

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

def webParser(url):
    driver = webdriver.Chrome('.\chromedriver.exe')
    driver.get(url)
    tab = driver.find_elements(By.TAG_NAME,'tbody')
    entries = []
    for j in range(4):
        entries.append(tab[j].find_elements(By.TAG_NAME,'tr'))
    res = []
    for p in range(4):
        arr = []
        for i in entries[p]:
            temp = i.text.split('\n')
            for j in temp:
                if j == '':
                    pass
                elif j == ', ' or j == ' ':
                    pass
                else:
                    arr.append(j)
        res.append(arr)

    driver.close()
    driver.quit()
    return res

########################## Script Patcher####################################


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
                a = a.rstrip()
                if a[-1] == ',':
                    a = a[:-1]
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
            A[c] = A[c].rstrip()            # to remove the error of the , and whitespaces at the end of the players name resulting in turn the duplicate of the player entries in dictionary.
            if A[c][-1] == ',':
                A[c] = A[c][:-1]
            if A[c] not in dt:
                dt[A[c]] = player(A[c])
            c += 1


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
            a = a.rstrip()
            if a[-1] == ',':
                a = a[:-1]
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


def StatsFinder(url,a,sitedct,dct,x):
    if x == 'y':
        dt = {}
        res = []
        array = webParser(url)
        Batting(array[0],dt,res)
        Batting(array[2],dt,res)
        Balling(array[1],dt)
        Balling(array[3],dt)
        Fielding(dt,res)
        sheet = pd.read_excel(r"C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Player's Data\{}.xlsx".format(a))
        for index,row in sheet.iterrows():
            nam = row[sheet.columns[0]]
            dt[nam].code_name,dt[nam].house,dt[nam].profile,dt[nam].credit = row[sheet.columns[1]],row[sheet.columns[2]],row[sheet.columns[3]],row[sheet.columns[4]]

        with open(r'C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Output Files\Players score Dict\{}'.format(sitedct), "wb") as myDcty:
            pickle.dump(dt, myDcty)
        myDcty.close()

    with open(r'C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Output Files\Players score Dict\{}'.format(sitedct), "rb") as myFile:
        dt = pickle.load(myFile)
    myFile.close()

    player_score = {}
    CodeNameToScr = {}
    for nam in dt:
        scr = dt[nam].cal_score()
        player_score[nam] = [dt[nam].house, dt[nam].profile, dt[nam].credit,scr, dt[nam].code_name]
        CodeNameToScr[dt[nam].code_name] = scr

    with open(r'C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Output Files\Players score Dict\{}'.format(dct), "wb") as myDct:
        pickle.dump(player_score, myDct)
    myDct.close()

    with open(r'C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Output Files\Players score Dict\{}CodeNameToScr'.format(dct), "wb") as dfct:
        pickle.dump(CodeNameToScr, dfct)
    dfct.close()

    print(player_score)
    print(CodeNameToScr)

# def StatsFinder(url,a,dct):
#     dt = {}
#     res = []
#     array = webParser(url)
#     Batting(array[0],dt,res)
#     Batting(array[2],dt,res)
#     Balling(array[1],dt)
#     Balling(array[3],dt)
#     Fielding(dt,res)
#     player_score = {}
#     CodeNameToScr = {}
#     sheet = pd.read_excel(r"C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Player's Data\{}.xlsx".format(a))
#     for index,row in sheet.iterrows():
#         nam = row[sheet.columns[0]]
#         dt[nam].code_name,dt[nam].house,dt[nam].profile,dt[nam].credit = row[sheet.columns[1]],row[sheet.columns[2]],row[sheet.columns[3]],row[sheet.columns[4]]
#         scr = dt[nam].cal_score()
#         player_score[nam] = [dt[nam].house, dt[nam].profile, dt[nam].credit,scr, dt[nam].code_name]
#         CodeNameToScr[dt[nam].code_name] = scr
#
#     with open(r'C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Output Files\Players score Dict\{}'.format(dct), "wb") as myDct:
#         pickle.dump(player_score, myDct)
#     myDct.close()
#
#     with open(r'C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Output Files\Players score Dict\{}CodeNameToScr'.format(dct), "wb") as dfct:
#         pickle.dump(CodeNameToScr, dfct)
#     dfct.close()
#
#     print(player_score)
#     print(CodeNameToScr)


sitedct = 'INDvsHK_WebDct'
a = 'INDvsHKWebscrap'
dct = 'INDvsHK_GR'
url = 'https://www.espncricinfo.com/series/india-in-united-arab-emirates-2022-1327266/india-vs-pakistan-2nd-match-group-a-1327270/full-scorecard'
url2 = 'https://www.espncricinfo.com/series/sri-lanka-in-united-arab-emirates-2022-1327265/india-vs-sri-lanka-9th-match-super-four-1327277/full-scorecard'
url3 = 'https://www.espncricinfo.com/series/india-in-united-arab-emirates-2022-1327266/hong-kong-vs-india-4th-match-group-a-1327272/full-scorecard'
StatsFinder(url3,a,sitedct,dct,'y')















