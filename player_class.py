import pandas as pd


# a = int(input("Enter the sheet no. to be read\n"))

class Player:

    def __init__(self, name, house, profile, credit, r, b, fours, sixes, sr, thirt, fif, cent, o, M, w, eco, bwl, dro,
                 rro, ca):
        self.name = name
        self.house = house
        self.profile = profile
        self.credit = credit
        self.r = r
        self.b = b
        self.fours = fours
        self.sixes = sixes
        self.sr = sr
        self.thirt = thirt
        self.fif = fif
        self.cent = cent
        self.o = o
        self.M = M
        self.w = w
        self.eco = eco
        self.bwl = bwl
        self.dro = dro
        self.rro = rro
        self.ca = ca

    def cal_score(self):
        score = 0
        score += int(self.r) + int(self.fours) + 2 * int(self.sixes) + 4 * int(self.thirt) + 8 * int(self.fif) + 16 * int(self.cent) + 12 * int(self.M) + 25 * int(self.w) + 8 * int(self.bwl) + 12 * int(self.dro) + 6 * int(self.rro) + 8 * int(self.ca)
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


def read_Cal_Score(a,players_list):
    sheet = pd.read_excel(r"C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Player's Data\Dream 11 project.xlsx", sheet_name=a)
    extras = 0 # not calculated correctly yet
    for index, row in sheet.iterrows():
        Name = row[sheet.columns[0]]
        r_bat, b_bat, fours, sixes, r_bowl, b_bowl, mdn, wkt, cWkt, dro, rro, ca = [0 for ind in range(12)]
        thirt,fif,cent,sr,eco,o,w,lb = 0,0,0,0,0,0,0,0
        for i in range(4, 244):
            entry = row[sheet.columns[i]].split(',')
            if not entry[0].isalpha():
                run = int(entry[0])
                if run < 0:
                    r_bowl += run
                    b_bowl += 1
                else:
                    r_bat += run
                    b_bat += 1
                    if run == 4 : fours += 1
                    if run == 6 : sixes += 1
            elif entry[0] == 'NP': pass
            elif entry[0] == 'D':
                b_bowl += 1
                if len(entry) == 2: mdn += 1
            elif entry[0] == 'W': wkt += 1
            elif entry[0] == 'C': cWkt += 1
            elif entry[0] == 'DRO':  # bowler
                dro += 1
                if not entry[1] == 'NP':
                     r_bowl += int(entry[1])
                     b_bowl += 1
            elif entry[0] == 'RRO': # NP
                rro += 1
                if not entry[1] == 'NP':
                     r_bowl += int(entry[1])
                     b_bowl += 1
            elif entry[0] == 'CA': # bowler
                 ca += 1
                 if not entry[1] == 'NP':
                     cWkt += 1
                     b_bowl += 1
            elif entry[0] == 'L':
                extras += int(entry[1])
                b_bowl += 1
                if entry[2] == 'DRO' : dro +=1
                elif entry[2] == 'RRO' : rro +=1
                else:pass
                if len(entry) == 4: mdn += 1
            elif entry[0] == 'WD': # extras calculation ; + --> , ; doubt in wides
                r_bowl += int(entry[1])
                b_bowl += 1
                if entry[2] == 'C':
                    cWkt += 1
                    ca += 1
                elif entry[2] == 'DRO' : dro += 1
                elif entry[2] == 'RRO': rro += 1
                else : r_bowl += int(entry[2])
            else :
                if entry[1] == 'BAT':
                    run1,run2 = int(entry[2]),int(entry[3])
                    r_bat += run1 + run2
                    b_bat += 2
                    if run1 == 4 : fours += 1
                    if run2 == 4 : fours += 1
                    if run1 == 6 : sixes += 1
                    if run2 == 6 : sixes += 1
                elif entry[1] == 'BWL':
                    ball1,ball2 = entry[2],entry[3]
                    if not ball1.isalpha(): r_bowl += int(ball1)
                    elif ball1 == 'DRO' : dro += 1
                    elif ball1 == 'RRO' : rro += 1
                    else : pass
                    if not ball2.isalpha(): r_bowl += int(ball2)
                    elif ball2 == 'DRO' : dro += 1
                    elif ball2 == 'RRO' : rro += 1
                    else : pass
                    if len(entry) == 5: r_bowl += int(entry[4])
                else:
                    if entry[2] == 'DRO': dro +=1
                    if entry[3] == 'DRO': dro +=1
                    if entry[2] == 'RRO': rro +=1
                    if entry[3] == 'RRO': rro +=1
        if 30 <= r_bat < 50: thirt += 1
        elif 50 <= r_bat < 100 : fif += 1
        elif 100 <= r_bat : cent +=1
        else : pass
        sr += r_bat/b_bat
        o += b_bowl/6
        eco += r_bowl/o
        w += wkt + cWkt
        lb += wkt

