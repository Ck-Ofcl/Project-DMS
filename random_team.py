from itertools import combinations
from player_class import Player
import pickle
import pandas as pd
random_filename = input("Enter a file name for random teams csv.\n")
c = input("You want to build the random teams' csv again?\n")

if c == "y":
    a = int(input("Enter the sheet no. to be read\n"))
    b = input("Enter tha name for the dictionary.\n")
    sheet = pd.read_excel(r"C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Player's Data\Dream 11 project.xlsx",sheet_name=a)

    def team_valid (players_tuple):
        WK,BAT,AR,BWL,credit,IND= 0,0,0,0,0,0
        for i in players_tuple:
            credit += i.credit
            if i.house == "IND":
                IND +=1
            if i.profile == "WK":
                WK +=1
            elif i.profile == "BAT":
                BAT +=1
            elif i.profile == "AR":
                AR +=1
            else :
                BWL +=1
        if 1 <= WK <= 4 and 3 <= BAT <= 6 and 1 <= AR <= 4 and 3 <= BWL <= 6 and credit <= 100 and 4 <= IND <= 7:
            return True
        else:
            return False


    def row_add(dct,team,tup,scor):
        # temp = []
        score = 0
        for i in team:
            # temp.append(i.name)
            score += scor[i.name]
        # dct["Players"].append(temp)
        # dct["Captain"].append(tup[0].name)
        # dct["Vice Captain"].append(tup[1].name)
        dct["Score"].append(score+scor[tup[0].name]+0.5*scor[tup[1].name])
        # dct["Players"].append(temp)
        # dct["Captain"].append(tup[1].name)
        # dct["Vice Captain"].append(tup[0].name)
        dct["Score"].append(score+scor[tup[1].name]+0.5*scor[tup[0].name])

    players_list = [Player(row[sheet.columns[0]],row[sheet.columns[1]],row[sheet.columns[2]],row[sheet.columns[3]],row[sheet.columns[4]],row[sheet.columns[5]],row[sheet.columns[6]],row[sheet.columns[7]],row[sheet.columns[8]],row[sheet.columns[9]],row[sheet.columns[10]],row[sheet.columns[11]],row[sheet.columns[12]],row[sheet.columns[13]],row[sheet.columns[14]],row[sheet.columns[15]],row[sheet.columns[16]],row[sheet.columns[17]],row[sheet.columns[18]],row[sheet.columns[19]]) for index, row in sheet.iterrows()]
    # players_list = [Player(row[sheet.columns[ind]] for ind in range(0, 20)) for index, row in sheet.iterrows()]
    players_score = {i.name: i.cal_score() for i in players_list}
    with open(r'C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Output Files\Players score Dict\{}'.format(b), "wb") as myDict:
        pickle.dump(players_score, myDict)
    myDict.close()
    # print(players_score)
    # input("Stop here")
    all_teams = combinations(players_list,11)

    # teams_list = {"Players":[],"Captain":[],"Vice Captain":[],"Score":[]}
    teams_list = {"Score": []}
    # count = 0
    for i in list(all_teams):
        if team_valid(i):
            # count += 1
            cvc = combinations(i,2)
            for j in list(cvc):
                row_add(teams_list, i, j, players_score)
    # print(count*110)
    # input("Stop here")
    # print(teams_list["Players"][0])
    print("Dictionary built successfully.\n")
    df = pd.DataFrame(teams_list)
    df.to_csv(r"C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Output Files\CSV\{}".format(random_filename))
    # df.to_csv(r"C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Output Files\manualgen_3.csv")
    # ax = df.hist(column='Score')
    # plt.show()
else:
    print("Random teams' csv already exists.\n")
