# from itertools import combinations
# import csv
# import pandas as pd
# # dct = {'ab':[4,5,'IND'],'cd' : [2,5,'AUS'],'D' : [12,7,'WI']}
# # # arr = [i for i in dct]
# # allt = combinations(dct,2)
# # for i in list(allt):
# #     print(i[1][1])
#
# row = ['a','b','c','d','e','f']
# head = ['P{}'.format(i) for i in range(1,23)]
# # print(head)
# with open("try.csv" ,'w',newline= '') as f:
#     writer = csv.writer(f)
#     writer.writerow(head)
#     writer.writerow(row)
#     f.close()
#
# with open('try.csv','r') as file:
#     df = pd.read_csv(file)
#     print(df)
#     file.close()
#
# class player:
#
#     def __init__(self,name):
#         self.name = name
#         self.r, self.b,self.fours,self.sixes,self.sr,self.thirt,self.fif,self.cent,self.o,self.M,self.w,self.eco,self.bwl,self.dro,self.rro,self.ca = [0]*16
#
# 'Mohammad Rizwan', 'Babar Azam', 'Fakhar Zaman', 'Iftikhar Ahmed', 'Khushdil Shah', 'Shadab Khan', 'Asif Ali', 'Rohit Sharma', 'Dinesh Karthik', 'Yuzvendra Chahal', 'Avesh Khan')
import pickle
with open(r"C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Output Files\Players score Dict\INDvsPAK_GR", "rb") as myFile:
            players_score = pickle.load(myFile)
            print(players_score)
            myFile.close()
a = 'er4 567t,  '
a = a.rstrip()
a = a[:-1]
# a = '2.67'
# b = float(a)
print(a,len(a))
