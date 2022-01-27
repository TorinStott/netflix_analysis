# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 11:10:01 2022

@author: local1
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#Read in files
df = pd.read_csv('netflix_titles.csv', sep=',')
titles = pd.read_csv('titles.tsv', sep='\t')
user_ratings = pd.read_csv('user_ratings.tsv', sep='\t')
#
#       DATA PREP
#

def findRatingsForNetflixData():
    # drop excess columns from IMDB data
    titles.drop(['titleType','primaryTitle','isAdult','startYear','endYear','runtimeMinutes','genres'], axis='columns', inplace=True)
    titles['originalTitle'] = titles['originalTitle'].fillna('Title_Unknown')
    # Merge two IMDB files
    title_with_rating = pd.merge(titles,user_ratings,how = 'inner', on = 'tconst')
    title_with_rating.rename(columns={'originalTitle':'title'}, inplace = True)
    # Merge Into Netflix data
    #Merge the DataFrames
    df2 = pd.merge(df, title_with_rating, how='inner', left_index=True, right_index=True, suffixes=('', '_drop'))
    #Drop the duplicate columns
    df2.drop([col for col in df2.columns if 'drop' in col], axis=1, inplace=True)
    #Write the data to a file for Analyzing later
    df2.to_csv('mergedData')


#Make ratings uniform (TV ratings don't need to be separate)
df['rating'] = df['rating'].replace({
                'PG-13': 'Teens - Age above 12',
                'TV-MA': 'Adults',
                'PG': 'Kids - PG',
                'TV-14': 'Teens - Age above 14',
                'TV-PG': 'Kids - PG',
                'TV-Y': 'Kids',
                'TV-Y7': 'Kids - Age above 7',
                'TV-Y7-FV': 'Kids - Age above 7',
                'R': 'Adults',
                'TV-G': 'Kids',
                 'G': 'Kids',
                'NC-17': 'Adults',
                'NR': 'NR',
                'UR': '',
                '74 min': '',
                '84 min': '',
                '66 min': '',
})

# Date added should be converted to Date type in pandas
df["date_added"] = pd.to_datetime(df["date_added"])

#
#       DATA VIS
#

def showPreliminaryData():    
    # What dates were shows added?
    df["date_added"].hist(bins=100)
    plt.show()
    # What ratings are most common?
    df["rating"].value_counts().plot(kind="bar")
    plt.show()
    # What is the breakdown for movies/shows on Netflix data?
    df["type"].value_counts().plot(kind="pie", autopct='%1.1f%%') #autopct just formats the %
    plt.show()
