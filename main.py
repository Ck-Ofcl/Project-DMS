from Ball_random_team import random_filename
from Ball_real_team import real_filename
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import pandas as pd
import numpy as np
# import time
# start = time.time()
Random_teams = pd.read_csv(r'C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Output Files\CSV\{}_Random.csv'.format(random_filename))
Real_teams = pd.read_csv(r'C:\Users\chira\PycharmProjects\Dream11_Agam_Gupta\Output Files\CSV\{}_Real.csv'.format(real_filename))
w = 5
a = 0
b = int(max(max(Random_teams['Score']), max(Real_teams['Score']))) + 1
plt.hist(Random_teams['Score'],color = 'pink',bins = range(a, b+w, w),label = 'Random Teams',weights=np.ones(35571470)/35571470,alpha = 0.8)
plt.hist(Real_teams['Score'],color = 'violet',bins = range(a, b+w, w),label = 'Real Teams',weights=np.ones(2735042)/2735042,alpha = 0.8)
plt.xlim([0,b+50])
# plt.ylim([0,1000000])
plt.title("Dream 11: IND vs IRE")
plt.xlabel("Score")
plt.ylabel("No. of teams")
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.legend()
# end = time.time()
plt.show()
# print(end-start)
# print(data.describe())
print('Random -',Random_teams['Score'].mean())
print('Real -',Real_teams['Score'].mean())
