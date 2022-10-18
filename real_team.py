import PyPDF2
import pandas as pd
import pickle
import re

real_filename = input("Enter a file name for real teams csv.\n")
c = input("Do you want to build the real teams' csv again?\n")

if c == "y":
    b = input("Enter tha name for the dictionary.\n")
    with open(r'C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Output Files\Players score Dict\{}'.format(b), "rb") as myFile:
        players_score = pickle.load(myFile)
    myFile.close()
    # players_score = {'Ishan Kishan': 39, 'Deepak Hooda': 73, 'Suryakumar Yadav': 0, 'Hardik Pandya': 56, 'Dinesh Karthik': 14, 'Ruturaj Gaikwad': 0, 'Axar Patel': 8, 'Umran Malik': 0, 'Bhuvneshwar Kumar': 49, 'Avesh Khan': 21, 'Yuzvendra Chahal': 31, 'Andy Balbirnie': 0, 'Paul Stirling': 5, 'Gareth Delany': 9, 'Harry Tector': 90, 'Lorcan Tucker': 22, 'George Dockrell': 4, 'Mark Adair': 0, 'Andy McBrine': 0, 'Craig Young': 66, 'Joshua Little': 27, 'Conor Olphert': 0}
    # teams_list = {"Players":[],"Captain":[],"Vice Captain":[],"Score":[]
    teams_list = {"Score": []}
    store = "User (Team)Player 1 (Captain)Player 2 (Vice Captain)Player 3Player 4Player 5Player 6Player 7Player 8Player 9Player 10Player 11"
    pdf_file = input("Enter the pdf to be read.\n")
    pdfopen = open(r'C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Documnets\{}'.format(pdf_file),'rb')
    pdf = PyPDF2.PdfFileReader(pdfopen)
    n = pdf.numPages
    for ind in range(n):
        text = pdf.getPage(ind).extract_text()
        text = text.splitlines()
        m = len(text)
        for c in range(m):
            if text.pop(0) == store:
                break

        for i in text:
            temp = i.split(")")
            try:
                temp = re.findall('[A-Z][^A-Z]*', temp[1])
                players = []
                ############### Customized for IND vs IRE #####################
                if len(temp) == 23:
                    y = 0
                    while y < 23:
                        if temp[y] == "Brine":
                            players[(y//2)-1] += "Brine"
                            y += 1
                        else:
                            players.append(temp[y]+temp[y+1])
                            y += 2
                ############### Customized for IND vs IRE #####################
                else:
                    for j in range(0,22,2):
                        players.append(temp[j]+temp[j+1])

                score = 0
                # print(players)
                for k in players:
                    score += players_score[k]
                score += players_score[players[0]] + 0.5*players_score[players[1]]
                # teams_list["Players"].append(players)
                # teams_list["Captain"].append(players[0])
                # teams_list["Vice Captain"].append(players[1])
                teams_list["Score"].append(score)
            except :
                pass
        print(ind+1)

    df = pd.DataFrame(teams_list)
    df.to_csv(r"C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Output Files\CSV\{}".format(real_filename))

else:
    print("Real teams' csv already exists.")







