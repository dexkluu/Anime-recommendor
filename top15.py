# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 15:36:56 2018

@author: dluu1
"""
# Data from September 6, 2018

import pandas as pd
import numpy as np

usermap = pd.read_csv('user_id_mapping.csv', index_col = 0)
titlemap = pd.read_csv('title_id_mapping.csv', index_col = 0)
ratingsmap = pd.read_csv('ratings_finalv2.csv', index_col = 0)
map1 = ratingsmap.merge(usermap, on = 'user_id')
map2 = map1.merge(titlemap, on = 'item_id')
ratings = map2[['user', 'titles', 'value']]
# userRatings = ratings.pivot_table(index = ['user'], columns = ['titles'], values = 'value')
# The above command will pivot the ratings data. Because this takes some time, it was done once and the csv file was saved. Below, it
# read in.
userRatings = pd.read_csv('userrating_final.csv', index_col = 0)

# Find the average rating and how many ratings there were for each show
ratings = pd.DataFrame(userRatings.mean(), columns = ['mean'])
ratings['num of ratings'] = userRatings.count()

# Drop any show that has less than 1000 ratings
userRatings.drop(list(ratings[ratings['num of ratings'] < 1000].index), axis = 1, inplace = True)
ratings.drop(list(ratings[ratings['num of ratings'] < 1000].index), axis = 0, inplace = True)

# Find correlation coefficients for each show where more than 200 users rated both
corrMat = userRatings.corr(min_periods = 200) # min_periods 200 was decent

# Make a top 15 recommendation based off correlation coefficients
rank = np.arange(1,16)
top15 = pd.DataFrame(data = rank, columns = np.array(['Recommendation Rank']))
for i in range(userRatings.shape[1]):
    # Creating the top 15 dataframe
    # Creates a pandas series object sorted by highest correlation values
    top = pd.Series(corrMat.iloc[:,i].sort_values(ascending = False).index[0:16])
    
    # Drops the current title from the recommendation list because it has 1.0
    # correlation with itself
    top.drop(top[top == userRatings.columns[i]].index, inplace = True)
    
    # After dropping the title, resets index
    top.reset_index(inplace = True, drop = True)
    
    # Name the current show of interest the correct name
    top.name = userRatings.columns[i]
    
    # Consolidates the recommendations into one dataframe
    top15 = top15.join(top)
    

