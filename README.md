# Food.com_data
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mpc02002/Food.com_data/master?filepath=%2Fingredient_tester.ipynb)

<h3> Overview </h3>
<p>
The goal of this project is to determine whether the inclusion of a given ingredient in online recipes results in higher overall user ratings.  All scripts are designed to run in Python 3.  Click the binder link to run the Jupyter notebooks.
  
<h3> The Datasets </h3>
<p>
We use datasets containing over 180K recipes from Food.com, together with over 700K user ratings, obtained from <a href="https://www.kaggle.com/shuyangli94/food-com-recipes-and-user-interactions">Kaggle.com</a>.   The raw datasets were too large to upload directly, so they were broken up into smaller csv files using a short simple Python script.  The main script ingredient_tester2.py reassembles them before working with them.
  
<h3> Script Details </h3>
<p>
The Python script ingredient_tester2.py runs from the command line and prompts the user for a choice of ingredient (ingr).  The script then extracts all recipes which include ingr from the raw data, and combines them with their given user ratings; this is also performed for recipes which lack ingr.  Data for recipes without ratings is dropped.  The script returns the mean rating and the sample size for recipes with ingr and for recipes without ingr, then runs the Mann-Whitney U-Test to determine if there is a statistically significant gap in the sample means.  
  
The null hypothesis being tested is "Recipes with ingr have the same mean rating as recipes without ingr," and the alternative (two-sided) hypothesis is that the mean ratings are different.  We use the Mann-Whitney U-Test because the ratings consist of ordinal data which is not normally distributed.  The test returns a p-value and if p is less than the critical value (.10, .05, or .01) then the null hypothesis is rejected with confidence 1-p.  The U-Test is aborted if either sample size is less than or equal to 20, because it does not give a meaningful result in this circumstance.

Lastly, the user is asked whether they want to plot the rating distributions for recipes with ingr vs. recipes without ingr.  If the user affirms, then a bar plot is exported to the filename 'plot.png'.

<h3> Some Results </h3>
<p>
Some ingredients appear to have a strong detractive effect on user ratings: for example, kale and lamb almost certainly lower the mean rating of recipes which include them.  Other ingredients, like tofu and apple, appear to have a positive effect on mean ratings.  I invite the reader to look for other interesting conclusions.
  
This project is still in progress.
