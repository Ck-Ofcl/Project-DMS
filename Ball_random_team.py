from itertools import combinations
import pickle
import pandas as pd

random_filename = input("Enter a file name for random teams csv.\n")
c = input("You want to build the random teams' csv again?\n")

if c == "y":
    b = input("Enter tha name for the dictionary.\n")
    with open(r'C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Output Files\Players score Dict\{}'.format(b), "rb") as myFile:
        players_score = pickle.load(myFile)
    myFile.close()
    players_list = [index for index in players_score]

    def team_valid (players_tuple):
        WK,BAT,AR,BWL,credit,IND= 0,0,0,0,0,0
        for i in players_tuple:
            credit += players_score[i][2]
            if players_score[i][0] == "IND":
                IND +=1
            if players_score[i][1] == "WK":
                WK +=1
            elif players_score[i][1] == "BAT":
                BAT +=1
            elif players_score[i][1] == "AR":
                AR +=1
            else :
                BWL +=1
        if 1 <= WK <= 4 and 3 <= BAT <= 6 and 1 <= AR <= 4 and 3 <= BWL <= 6 and credit <= 100 and 4 <= IND <= 7:
            return True
        else:
            return False


    def row_add(dct,team,tup):
        score = 0
        for index in team:
            score += players_score[index][3]
        dct["Score"].append(score+players_score[tup[0]][3]+0.5*players_score[tup[1]][3])
        dct["Score"].append(score+players_score[tup[1]][3]+0.5*players_score[tup[0]][3])

    all_teams = combinations(players_list,11)
    teams_list = {"Score": []}
    for i in list(all_teams):
        if team_valid(i):
            cvc = combinations(i,2)
            for j in list(cvc):
                row_add(teams_list, i, j)

    df = pd.DataFrame(teams_list)
    df.to_csv(r"C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Output Files\CSV\{}_Random.csv".format(random_filename))
    print('Calculated scores for random teams.\n')

else:
    print("Random teams' csv already exists.\n")
