# -*- coding: utf-8 -*-
"""
Prompts the user for a choice of ingredient, then runs a Mann-Whitney U-test
to determine if the mean rating for Food.com recipes with that ingredient 
differs from the mean rating for Food.com recipes without that ingredient in
a statistically significant way.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import pickle
from scipy import stats

def get_ingr_map():
    if os.access("datasets-raw/ingr_map.pkl",os.F_OK):
        infile = open("datasets-raw/ingr_map.pkl",'rb')
        ingr_map = pickle.load(infile)
        infile.close()
        ingr_map = ingr_map[['replaced','id']].set_index('replaced').drop_duplicates().sort_index()
        return ingr_map
    else:
        print('Error: cannot access ingredient map file.')
        return 
    
def get_cleaned_datasets(ingr):    
    if os.access("datasets-raw/PP_recipes.csv",os.F_OK):
        df = (pd.read_csv('datasets-raw/PP_recipes.csv')[['i','ingredient_ids']]
              .set_index('i').sort_index())
        if os.access("datasets-raw/RAW_interactions.csv",os.F_OK):
            print('Extracting and cleaning data ...\n')
            interactions = (pd.read_csv('datasets-raw/RAW_interactions.csv')[['recipe_id','rating']]
                            .set_index('recipe_id').sort_index())
            df = pd.merge(df,interactions,how='inner',left_index=True,right_index=True)
            df.index.rename('recipe_id',inplace=True)
            ingr_map = get_ingr_map()
            ingr_id = ingr_map.loc[ingr.lower()]['id']
            dfGood = df[df['ingredient_ids'].str.contains(str(ingr_id))]
            dfBad = df[~df['ingredient_ids'].str.contains(str(ingr_id))]
            return(dfGood, dfBad)
        else:
            print('Error: cannot access interactions data file.')
            return
    else:
        print('Error: cannot access recipes data file.')
        return
    
def test_datasets(ingr):
    dfGood,dfBad = get_cleaned_datasets(ingr)
    countGood = len(dfGood)
    countBad = len(dfBad)
    meanGood = np.average(dfGood['rating'])
    meanBad = np.average(dfBad['rating'])
    print('The average rating for recipes with '+ingr+', based on '+str(countGood)+' samples, is '+str(meanGood)+'.')
    print('The average rating for recipes without '+ingr+', based on '+str(countBad)+' samples, is '+str(meanBad)+'.')
    print()
    if countGood <= 20:
        print('Since no more than 20 recipes contain '+ingr+', we cannot execute a meaningful hypothesis test.')
    else:
        print('Applying Mann-Whitney U-Test ...')
        print()
        (s, p) = stats.mannwhitneyu(dfGood['rating'],dfBad['rating'],alternative='two-sided')
        if p <= 0.01:
            print('With 99% confidence, we reject the hypothesis that the two distributions have the same mean.  (p = '+str(p)+')')
        elif p <= 0.05:
            print('With 95% confidence, we reject the hypothesis that the two distributions have the same mean.  (p = '+str(p)+')')
        elif p <= 0.1:
            print('With 90% confidence, we reject the hypothesis that the two distributions have the same mean.  (p = '+str(p)+')')
        else:
            print('We cannot reject the hypothesis that the distributions have the same mean.  (p = '+str(p)+')')
    plotans = input('Plot the rating comparison for recipes'+
                     ' with/without this ingredient? (y/n) ')
    if plotans.lower() == 'y':
        plot_datasets(ingr,dfGood,dfBad)
        
def plot_datasets(ingr,dfGood,dfBad):
    countGood = len(dfGood)
    countBad = len(dfBad)
    meanGood = np.average(dfGood['rating'])
    meanBad = np.average(dfBad['rating'])
    
    plt.figure()
    plt.suptitle('Food.com Recipe Ratings (2000-2018)')

    plt.subplot(1,2,1)
    xvals = np.array([1,2,3,4,5])
    x = np.arange(len(xvals))
    ratingsGood = []
    for i in xvals:
        n = len(dfGood.where(dfGood['rating'] == i).dropna())
        ratingsGood = ratingsGood+[n]
    ratingsGood = np.array(ratingsGood)
    plt.gcf().subplots_adjust(bottom=0.15)  # make room for two-line x labels
    plt.title('Recipes With '+ingr.capitalize(), size='medium')
    plt.xlabel('Number of Ratings\n(Total: '+str(countGood)+')')
    plt.yticks(x, xvals)
    plt.barh(x, ratingsGood, height=1, color=['red','pink','yellow','cyan','blue'])
    plt.axhline(y=meanGood-1,color='green')
    plt.text(x=plt.gca().get_xlim()[1], y=meanGood-1.2, horizontalalignment='right',
             s='Average Rating '+"{:.5f}".format(meanGood)+'  ', size='smaller', color='green')

    plt.subplot(1,2,2)
    ratingsBad = []
    for i in xvals:
        n = len(dfBad.where(dfBad['rating'] == i).dropna())
        ratingsBad = ratingsBad + [n]
    ratingsBad = np.array(ratingsBad)
    plt.title('Recipes Without '+ingr.capitalize(), size='medium')
    plt.xlabel('Number of Ratings\n(Total: '+str(countBad)+')')
    plt.yticks(x, xvals)
    plt.barh(x, ratingsBad, height=1, color=['red','pink','yellow','cyan','blue'])
    plt.axhline(y=meanBad-1,color='green')
    plt.text(x=plt.gca().get_xlim()[1], y=meanBad-1.2, horizontalalignment='right',
             s='Average Rating '+"{:.5f}".format(meanBad)+'  ', size='smaller', color='green')

    plt.savefig('plot.png')
    print("Plot saved as 'plot.png'")

def main_loop():
    ingr_map = get_ingr_map()
    print('Enter the ingredient you would like to test, or press <enter> to quit.')
    print('(Examples: sugar, kale, tofu, lamb, bread crumb, jackfruit ... )\n')
    ingr = input('Ingredient: ')
    while ingr.lower() not in ingr_map.index.tolist():
        if ingr == '':
            break
        print('There are no recipes with that ingredient.  Please enter another or press <enter> to quit.')
        print()
        ingr = input('Ingredient: ')
    ingr=ingr.lower()
    test_datasets(ingr)

if __name__ == '__main__':
    main_loop()