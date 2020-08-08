# Food.com_data
<h3> Overview </h3>
<p>
The goal of this project is to conduct analysis of the impact of various features of recipes (like length, complexity, technique inclusion, and ingredient inclusion) on their overall user ratings.  At present the project contains (1) a detailed analysis of the effect of recipe complexity on user ratings, and (2) a standalone script which allows the user to run a statistical test on the impact of a particular choice of ingredient on user ratings.  All scripts are designed to run in Python 3.  This repository was last updated 8/8/20.
  
<h3> The Datasets </h3>
<p>
We use datasets containing over 180K recipes from Food.com, together with over 700K user ratings, obtained from <a href="https://www.kaggle.com/shuyangli94/food-com-recipes-and-user-interactions">Kaggle.com</a>.   The raw datasets were too large to upload directly, so they were broken up into smaller csv files using a short simple Python script.  The scripts in this repository reassemble them before working with them.
  
<h3> Recipe Complexity Analysis </h3>

The Jupyter Notebook recipe_complexity_analysis.ipynb contains a statistical and visual study of the question, "Does complexity of recipes affect user ratings positively or negatively?"  This question seems natural because cooking is a both a practical skill and an art form, and users may be alternatively frustrated or inspired by attempting to implement a recipe which requires a more involved process, a longer duration, or a more difficult cooking technique.

We study complexity in two forms: (1) "naive" complexity measures, namely duration of cook time, number of steps, and number of ingredients, and (2) inclusion of particular techniques, like barbecue, emulsification, or poaching.  We extract these techniques from the recipe descriptions using some nice tools from the Natural Language Toolkit (NLTK).  We analyze connections between these complexity measures and three types of outcomes in terms of user ratings: mean rating, one ratio, and overall distribution of ratings.

The included scripts conduct a large number of Mann-Whitney U-tests to determine which techniques have a statistically significant impact on outcomes.  We use the Mann-Whitney U-Test because the ratings consist of ordinal data which are not normally distributed.  The specific null/alternative hypotheses being tested are clearly stated in the report.  A typical null hypothesis takes the form: "The probability that a random rating of a recipe using the technique is lower than a random rating of a recipe without is greater than the probability that it is higher."  Under the null hypothesis the distributions are more or less indistinguishable.  The alternative (one-sided) hypothesis is that ratings for recipes with the technique are likely to be lower than ratings for recipes without the technique.

The test returns a p-value and if p is less than the critical value (.05 or .01) then the null hypothesis is rejected with confidence 1 - p.  We also calculate the associated rho statistic, which represents an estimate of the probability stated in the null hypothesis.
  
<h3> The Ingredient Tester </h3>
<p>
The Python script ingredient_tester2.py runs from the command line and prompts the user for a choice of ingredient (ingr).  The script then extracts all recipes which include ingr from the raw data, and combines them with their given user ratings; this operation is also performed for recipes which lack ingr.  Data for recipes without ratings is dropped.  The script returns the mean rating and the sample size for recipes with ingr and for recipes without ingr, then runs a Mann-Whitney U-Test to determine if there is a statistically significant gap between the two sample distributions.  
  
The null hypothesis being tested is "The probability that a random recipe with ingr has a lower rating than a random recipe without ingr is equal to the probability that its rating is greater."  The alternative (one-sided) hypothesis is that a recipe with ingr is more likely to have a lower rating than a recipe without.

The test returns a p-value and if p is less than the critical value (.10, .05, or .01) then the null hypothesis is rejected with confidence 1 - p.  The U-Test is aborted if either sample size is less than or equal to 20, because it does not give a meaningful result in this circumstance.  When the hypothesis is rejected, an estimate (the rho statistic) is calculated of the probability that (random recipe with ingr)'s rating is lower than (random recipe without ingr).

Lastly, the user is asked whether they want to plot the rating distributions for recipes with ingr vs. recipes without ingr.  If the user affirms, then a bar plot is exported to the filename 'plot.png'.

<h3> Survey of Results </h3>
<p>
The investigations conducted in recipe_complexity_analysis.ipynb find no evidence of correlation between any of the naive measures (cook time, number of steps, number of ingredients) with the outcomes of mean rating or one ratio.

On the other hand, we find strong evidence that inclusion of the techniques 'casserole', 'pressure', 'fry', 'steam', 'simmer', and 'boil' are damaging to user ratings of recipes. With high confidence, a random recipe with one of these techniques will have a lower mean rating than one without, and a random rating of a recipe with one of these techniques will be lower than a random rating of one without. The probability gaps are especially striking in for 'casserole' (lower mean 53.5% chance, lower individual rating 52.1% chance, null hypotheses rejected with 99% confidence) and for 'pressure' (lower mean 56.6% chance, lower individual rating 51.4% chance, null hypotheses rejected with 99% confidence).

We find evidence that inclusion of the techniques 'grill', 'marinate', 'roast', and 'emulsify' improve mean ratings, lower one ratios, and increase overall rating distributions, so they correspond to improved rating outcomes across all three of our metrics, although our confidence levels are not as high as they are for the negative results in the preceding paragraph.

The following heatmap summarizes our probability estimates for mean rating, one ratio, and individual rating for each technique studied.  The visual shorthand is that GREEN means higher ratings, and PURPLE means lower ratings.

![Probability Estimate Heatmap](https://github.com/mpc02002/Food.com_data/blob/master/techniques_probs_heatmap.png)
  
The script ingredient_tester2.py produces strong evidence that certain ingredients have a detractive effect on user ratings.  For example, kale and lamb almost certainly lower the mean rating of recipes which include them, with confidence over 99%.  Other ingredients, like tofu and apple, appear to have a positive effect on mean ratings, although the evidence is less conclusive for tofu.  I invite the reader to look for other interesting conclusions!  This project will soon be updated with a report on ingredient inclusion.

<h3> What Comes Next? </h3>
<p>
My next focus in analyzing this dataset is to focus not on user rating outcomes but on traffic outcomes-- can we predict when a recipe will receive a large number of user interactions?  Presumably recipes with a large number of interactions generate more hit traffic and greater ad revenue for the site hosts.  My next update will attempt to shed light on this question.
