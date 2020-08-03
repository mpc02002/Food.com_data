# Food.com_data
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mpc02002/Food.com_data/master?filepath=%2Fingredient_tester.ipynb)

<h3> Overview </h3>
<p>
The goal of this project is to conduct analysis of the impact of various features of recipes (like length, complexity, technique inclusion, and ingredient inclusion) on their overall user ratings.  At present the project contains (1) a detailed analysis of the effect of recipe complexity on user ratings, and (2) a standalone script which allows the user to run a statistical test on the impact of a particular choice of ingredient on user ratings.  All scripts are designed to run in Python 3.  Click the "launch binder" link above to run the Jupyter notebook version.
  
<h3> The Datasets </h3>
<p>
We use datasets containing over 180K recipes from Food.com, together with over 700K user ratings, obtained from <a href="https://www.kaggle.com/shuyangli94/food-com-recipes-and-user-interactions">Kaggle.com</a>.   The raw datasets were too large to upload directly, so they were broken up into smaller csv files using a short simple Python script.  The scripts in this repository reassemble them before working with them.
  
<h3> Recipe Complexity Analysis </h3>

The Jupyter Notebook recipe_complexity_analysis.ipynb contains a statistical and visual study of the question, "Does complexity of recipes affect user ratings positively or negatively?"  This question seems natural because cooking is a both a practical skill and an art form, and users may be alternatively frustrated or inspired by attempting to implement a recipe which requires a more involved process, a longer duration, or a more difficult cooking technique.

We study complexity in two forms: (1) "naive" complexity measures, namely duration of cook time, number of steps, and number of ingredients, and (2) inclusion of particular techniques, like barbecue, emulsification, or poaching.  We extract these techniques from the recipe descriptions using some nice tools from the Natural Language Toolkit (NLTK).  We analyze connections between these complexity measures and three types of outcomes in terms of user ratings: mean rating, one ratio, and overall distribution of ratings.

The included scrips conduct a large number of Mann-Whitney U-tests to determine which techniques have a statistically significant impact on outcomes.  
  
<h3> The Ingredient Tester </h3>
<p>
The Python script ingredient_tester2.py runs from the command line and prompts the user for a choice of ingredient (ingr).  The script then extracts all recipes which include ingr from the raw data, and combines them with their given user ratings; this operation is also performed for recipes which lack ingr.  Data for recipes without ratings is dropped.  The script returns the mean rating and the sample size for recipes with ingr and for recipes without ingr, then runs a Mann-Whitney U-Test to determine if there is a statistically significant gap in the sample means.  
  
The null hypothesis being tested is "The probability that a random recipe with ingr has a lower rating than a random recipe without ingr is equal to the probability that its rating is greater."  The alternative (one-sided) hypothesis is that a recipe with ingr is more likely to have a lower rating than a recipe without.

We use the Mann-Whitney U-Test because the ratings consist of ordinal data which is not normally distributed.  The test returns a p-value and if p is less than the critical value (.10, .05, or .01) then the null hypothesis is rejected with confidence 1 - p.  The U-Test is aborted if either sample size is less than or equal to 20, because it does not give a meaningful result in this circumstance.  When the hypothesis is rejected, an estimate is calculated of the probability that (random recipe with ingr)'s rating is lower than (random recipe without ingr).

Lastly, the user is asked whether they want to plot the rating distributions for recipes with ingr vs. recipes without ingr.  If the user affirms, then a bar plot is exported to the filename 'plot.png'.

<h3> Some Results </h3>
<p>
The investigations conducted in recipe_complexity_analysis.ipynb find no evidence of correlation between any of the naive measures (cook time, number of steps, number of ingredients) with the outcomes of mean rating or one ratio.

On the other hand, we find strong evidence that inclusion of the technique 'caramelize' is damaging to user ratings of recipes.  A random recipe with 'caramelize' is likely to have a higher one ratio than a random recipe without (sample probability 50.64%; null hypothesis rejected with 95% confidence), and a random user rating of a recipe with 'caramelize' will be lower than than one without (sample probability 51.52%; null hypothesis rejected with 99% confidence).

 We find evidence that inclusion of the technique 'roast' improves mean ratings (sample probability 50.76%, null hypothesis rejected with 95% confidence), as does the technique 'microwave' improves mean ratings (sample probability 50.84%, null hypothesis rejected with 95% confidence).  Moreover, 'roast' and 'microwave' both decrease the one ratio and increase the overall rating distribution in the analyzed sample.  But the latter two findings are not statistically significant, so more evidence is needed to assume that 'roast' improves user ratings.

 We find with high confidence that 'steam', 'brine', 'boil', 'baste', and 'barbecue' damage rating distributions, but may actually lower one ratio or increase mean rating (in the case of 'boil', in a statistically significant way).  Conversely, we with high confidence that 'puree', and 'pressure' improve mean ratings or decrease one ratios, but they each appear to damage overall rating distributions in the analyzed sample.  So we regard these latter findings as inconclusive.  A deeper or more subtle analysis could improve these findings.
  
The script ingredient_tester2.py produces strong evidence that certain ingredients have a detractive effect on user ratings.  For example, kale and lamb almost certainly lower the mean rating of recipes which include them, with confidence over 99%.  Other ingredients, like tofu and apple, appear to have a positive effect on mean ratings, although the evidence is less conclusive for tofu.  I invite the reader to look for other interesting conclusions!  This project will soon be updated with a report on ingredient inclusion.
