__author__ = 'Dante'


import pandas as pn

data = pn.read_csv('/Dropbox/NFL_scores_2015.csv')
week1 = data.loc[data.week == 1]

# Fill in the missing games
week1.loc[:, 'vs'] = week1.loc[]