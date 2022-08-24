from itertools import combinations
import csv
import pandas as pd
# dct = {'ab':[4,5,'IND'],'cd' : [2,5,'AUS'],'D' : [12,7,'WI']}
# # arr = [i for i in dct]
# allt = combinations(dct,2)
# for i in list(allt):
#     print(i[1][1])

row = ['a','b','c','d','e','f']
head = ['P{}'.format(i) for i in range(1,23)]
# print(head)
with open("try.csv" ,'w',newline= '') as f:
    writer = csv.writer(f)
    writer.writerow(head)
    writer.writerow(row)
    f.close()

with open('try.csv','r') as file:
    df = pd.read_csv(file)
    print(df)
    file.close()

