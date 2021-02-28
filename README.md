# Comparison of Portuguese public and private schools' grades (WIP)


This is a personal project in progress. 

There are two topics I want to address:

1. Do Portuguese private schools outperform public schools because of
the student's characteristics? Or because they are of higher (average)
quality relative to comparable schools?

2. In general, how much grade inflation is there? What are the best
predictors of that grade inflation?

For the first question, the school-level data (in /data/raw) is scraped using
Scrapy (see code in /src/school_rank/). The second one is answered
using student-level data from [DGES](https://www.dge.mec.pt/relatoriosestatisticas-0).
All the data has been processed (/data/processed/). Now I am building the models (almost done).

### What I've done so far

* Scraped and processed all the data (in /data/processed/) 
* Finish most of the basic functionality for (what will eventually become) a Python package for probabilistic  
simulations (in /src/stan_utils/sim_helper.py)
* Developed a new(?) type of [spline model](https://github.com/davidmpinho/custom-models/blob/main/regression/fast_1d_splines.stan)
that runs faster and has more interpretable priors.
I have also selected a few other 'parts' for my model that still need to be adapted to my particular problem (with missing 
data and such). 

### Major to-do tasks for the first question

1. Continue building Stan models and the respective simulations (in
/src/stan_utils/sim_helper.py) that allow for:
    - Spatial relationships (with gaussian processes/random fields);
    - Integrate missing data imputation and measurement error.

2. Fit the model analyze the results.

3. Write an article about it. The idea is to have a more technical case study
on using complex models with small data sets (similar to 
[Michael Betancourt's](https://betanalpha.github.io/writing/) 
case studies but with more applied, rather than introductory, material).

### Major to-do tasks for the second question

1. Do experiments (with simulated data) to figure out how long it takes to run even a basic model. 
2. Iterate on that model. 
3. Make an accessible article showing the results with a dashboard. 



