import pandas as pd
import pickle

# a = int(input("Enter the sheet no. to be read\n"))
b = input("Enter the name for the dictionary.\n")
# sheet = pd.read_excel(r"C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Player's Data\Dream 11 project.xlsx",sheet_name=a)
sheet = pd.read_excel(r"C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Player's Data\Data.xlsx")


class Player:

    def __init__(self, name, code_name,house, profile, credit, row):
        self.name, self.code_name,self.house, self.profile, self.credit, self.row = name,code_name, house, profile, credit, row
        self.r, self.fours,self.sixes,self.thirt,self.fif,self.cent,self.mdn,self.w,self.lb,self.dro,self.rro,self.ca,self.o,self.eco,self.sr,self.b,self.dot = [0]*17
        self.WktOrder = [0]*10

    def cal_score(self):
        WktNoPts = [14,14,12,10,8,6,4,2,0,0]
        self.readBall()
        score = 0
        # score += int(self.r) + int(self.fours) + 2 * int(self.sixes) + 4 * int(self.thirt) + 8 * int(self.fif) + 16 * int(self.cent) + 12 * int(self.mdn) + 25 * int(self.w) + 8 * int(self.lb) + 12 * int(self.dro) + 6 * int(self.rro)+ 8 * int(self.ca)
        score += int(self.r) +  4 * int(self.thirt) + 8 * int(self.fif) + 16 * int(self.cent) + 12 * int(self.mdn) + 25 * int(self.w) + 8 * int(self.lb) + 12 * int(self.dro) + 6 * int(self.rro)+ 6 * int(self.ca)
        for i in range(10):
            score += self.WktOrder[i] * WktNoPts[i]
        score += 2*self.dot
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

    def readBall(self):
        # extras = 0  # not calculated correctly yet
        r_bat, b_bat,r_bowl, b_bowl,wkt, cWkt = [0]*6
        self.thirt, self.fif, self.cent, self.sr, self.eco, self.o, self.w, self.lb = 0, 0, 0, 0, 0, 0, 0, 0
        for i in range(5, 133):
            entry = (self.row[sheet.columns[i]]).split(',')
            if entry[0] == 'N': continue
            else:
                run = int(entry[0])
                if entry[1] == 'A':
                    b_bat += 1
                    r_bat += run
                    if run == 4: self.fours +=1
                    if run == 6: self.sixes +=1
                elif entry[1] == 'B':
                    r_bowl,b_bowl = r_bowl + run, b_bowl+1 # G = for bowlers
                    if run == 0: self.dot +=1
                else : pass
                l = len(entry)
                if l > 2 :
                    if entry[2].isdigit() :
                        r_bat += int(entry[2])
                        self.fours += int(entry[3])
                        self.sixes += int(entry[4])
                        b_bat += int(entry[5])
                    else :
                        i = 2
                        while i < l:
                        #     if entry[i] == 'W': wkt += 1
                        #     elif entry[i] == 'C': cWkt += 1
                        #     elif entry[i] == 'CA':
                        #         self.ca += 1
                        #         if entry[1] == 'B': cWkt += 1
                        #     elif entry[i] == 'M' : self.mdn +=1
                        #     elif entry[i] == 'DRO' : self.dro += 1
                        #     else : self.rro += 1

                            ################# When Wicket order matters ###################
                            temp = entry[i].split('-')
                            if temp[0] == 'W': wkt,self.WktOrder[int(temp[1])-1] = wkt+1,1
                            elif temp[0] == 'C': cWkt,self.WktOrder[int(temp[1])-1] = cWkt +1,1
                            elif temp[0] == 'CA':
                                self.ca += 1
                                if len(temp) > 1: cWkt,self.WktOrder[int(temp[1])-1] = cWkt +1,1
                            elif temp[0] == 'M' : self.mdn +=1
                            elif temp[0] == 'DRO' : self.dro += 1
                            else : self.rro += 1
                            ################################################################

                            i += 1

        if 30 <= r_bat < 50:
            self.thirt += 1
        elif 50 <= r_bat < 100:
            self.fif += 1
        elif 100 <= r_bat:
            self.cent += 1
        else: pass
        self.b = b_bat
        if b_bat > 0 : self.sr += (r_bat / b_bat) *100
        self.o += b_bowl / 6
        if self.o > 0 : self.eco += r_bowl / self.o
        self.w += wkt + cWkt
        self.lb += wkt
        self.r = r_bat


def DictionaryMaker(dct):
    player_score = {}
    CodeNameToScr = {}
    for index,row in sheet.iterrows():
        p = Player(row[sheet.columns[0]],row[sheet.columns[1]],row[sheet.columns[2]],row[sheet.columns[3]],row[sheet.columns[4]],row)
        scr = p.cal_score()
        player_score[p.name] = [p.house,p.profile,p.credit,scr,p.code_name]
        CodeNameToScr[p.code_name] = scr

    with open(r'C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Output Files\Players score Dict\{}'.format(dct), "wb") as myDct:
        pickle.dump(player_score, myDct)
    myDct.close()

    with open(r'C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Output Files\Players score Dict\CodeNameToScr', "wb") as dfct:
        pickle.dump(CodeNameToScr, dfct)
    dfct.close()


DictionaryMaker(b)


with open(r'C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Output Files\Players score Dict\{}'.format(b), "rb") as myFile:
    players_score = pickle.load(myFile)
    myFile.close()

with open(r'C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Output Files\Players score Dict\CodeNameToScr', "rb") as Dcty:
    cname = pickle.load(Dcty)
    Dcty.close()

print(players_score)
print(cname)

#//////////////////////////////////Previous Code/////////////////////////////////////////////#

# for i in range(4, 244):
#     entry = self.row[sheet.columns[i]].split(',')
#     if not entry[0].isalpha():
#         run = int(entry[0])
#         if run < 0:
#             r_bowl += run
#             b_bowl += 1
#         else:
#             r_bat += run
#             b_bat += 1
#             if run == 4: self.fours += 1
#             if run == 6: self.sixes += 1
#     elif entry[0] == 'NP':
#         pass
#     elif entry[0] == 'D':
#         b_bowl += 1
#         if len(entry) == 2: self.mdn += 1
#     elif entry[0] == 'W':
#         wkt += 1
#     elif entry[0] == 'C':
#         cWkt += 1
#     elif entry[0] == 'DRO':  # bowler
#         self.dro += 1
#         if not entry[1] == 'NP':
#             r_bowl += int(entry[1])
#             b_bowl += 1
#     elif entry[0] == 'RRO':  # NP
#         self.rro += 1
#         if not entry[1] == 'NP':
#             r_bowl += int(entry[1])
#             b_bowl += 1
#     elif entry[0] == 'CA':  # bowler
#         self.ca += 1
#         if not entry[1] == 'NP':
#             cWkt += 1
#             b_bowl += 1
#     elif entry[0] == 'L':
#         extras += int(entry[1])
#         b_bowl += 1
#         if len(entry == 3):
#             if entry[2] == 'DRO' : self.dro += 1
#             else : self.rro += 1
#         if len(entry) == 4: self.mdn += 1
#     elif entry[0] == 'WD':  # extras calculation ; + --> , ; doubt in wides
#         r_bowl += int(entry[1])
#         b_bowl += 1
#         if len(entry == 3):
#             if entry[2] == 'CA' :  # CA means BOWLER taken a catch on bal next to wide and so wicket + catch increment
#                 cWkt += 1
#                 self.ca += 1
#             elif entry[2] == 'C': cWkt +=1 # only catch out by bowler catch by different person
#             elif entry[2] == 'W' : wkt += 1
#             elif entry[2] == 'DRO': self.dro += 1
#             else: self.rro += 1
#     else:
#         if entry[1] == 'BAT':
#             run1, run2 = int(entry[2]), int(entry[3])
#             r_bat += run1 + run2
#             b_bat += 2
#             if run1 == 4: self.fours += 1
#             if run2 == 4: self.fours += 1
#             if run1 == 6: self.sixes += 1
#             if run2 == 6: self.sixes += 1
#         elif entry[1] == 'BWL':
#             b_bowl += 1
#             ball1, ball2 = entry[2], entry[3]
#             if not ball1.isalpha():
#                 r_bowl += int(ball1)
#             elif ball1 == 'DRO':
#                 self.dro += 1
#             elif ball1 == 'RRO':
#                 self.rro += 1
#             else:
#                 pass
#             if not ball2.isalpha():
#                 r_bowl += int(ball2)
#             elif ball2 == 'DRO':
#                 self.dro += 1
#             elif ball2 == 'RRO':
#                 self.rro += 1
#             else:
#                 pass
#             if len(entry) == 5: r_bowl += int(entry[4])
#         else:
#             if entry[2] == 'DRO': self.dro += 1
#             if entry[3] == 'DRO': self.dro += 1
#             if entry[2] == 'RRO': self.rro += 1
#             if entry[3] == 'RRO': self.rro += 1

