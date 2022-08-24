import PyPDF2
import pandas as pd
import pickle
import re
import csv

real_filename = input("Enter a file name for real teams csv.\n")
c = input("Do you want to build the real teams' csv again?\n")

if c == "y":

    with open(r'C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Output Files\Players score Dict\CodeNameToScr', "rb") as Dcty:
        CodeNameToScr = pickle.load(Dcty)
        Dcty.close()

    pdf_csv = input('Enter the csv name for real teams pdf.\n')
    d = input('Do you want to read pdf again?\n')
    if d == 'y':
        b = input("Enter tha name for the dictionary.\n")
        with open(r"C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Output Files\Players score Dict\{}".format(b), "rb") as myFile:
            players_score = pickle.load(myFile)
            myFile.close()

        store = "User (Team)Player 1 (Captain)Player 2 (Vice Captain)Player 3Player 4Player 5Player 6Player 7Player 8Player 9Player 10Player 11"
        pdf_file = input("Enter the pdf to be read.\n")
        pdfopen = open(r'C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Documnets\{}'.format(pdf_file),'rb')
        pdf = PyPDF2.PdfFileReader(pdfopen)
        n = pdf.numPages
        head = ['P{}'.format(i) for i in range(1,12)]
        with open(r'C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Output Files\CSV\{}'.format(pdf_csv),'w',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(head)

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
                        if len(temp) == 23:
                            y = 0
                            while y < 23:
                                if temp[y] == "Brine":
                                    players[(y//2)-1] += "Brine"
                                    y += 1
                                else:
                                    players.append(temp[y]+temp[y+1])
                                    y += 2
                        else:
                            for j in range(0,22,2):
                                players.append(temp[j]+temp[j+1])

                        entry = [players_score[players[i]][4] for i in range(11)]
                        writer.writerow(entry)
                    except :
                        pass
                print(ind+1)
            f.close()
            print('Pdf is read successfully.\n')

    teams_list = {"Score": []}
    with open(r'C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Output Files\CSV\RealTeams{}.csv'.format(pdf_csv),'r') as file:
        df = pd.read_csv(file)
        for index,row in df.iterrows():
            score = 0
            for j in range(11):
                score += CodeNameToScr[row[df.columns[j]]]
            score += CodeNameToScr[row[df.columns[0]]] + 0.5*CodeNameToScr[row[df.columns[1]]]
            teams_list['Score'].append(score)
        file.close()

    df = pd.DataFrame(teams_list)
    df.to_csv(r"C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Output Files\CSV\Real_{}.csv".format(real_filename))
    print('Calculated scores for real teams.\n')

else:
    print("Real teams' csv already exists.")







