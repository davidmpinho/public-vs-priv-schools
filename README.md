# Comparison of Portuguese public and private schools' grades (WIP)

This is a personal project in progress. 

There are two topics I want to address:

1. Do Portuguese private schools outperform public schools because of
the student's characteristics? Or because they are of higher (average)
quality relative to comparable schools?

2. In general, how much grade inflation is there? What are the best
predictors of that inflation?

For the first question, the school-level data (in /data/) is scraped using
Scrapy (see code in /python_scripts/school_rank/). The second one is answered
using student-level data from [DGES](https://www.dge.mec.pt/relatoriosestatisticas-0).

### Major to-do tasks for the first question

1. Continue building Stan models and the respective simulations (in
/python_scripts/stan_utils/sim_helper.py) that allow for:
    - Spatial relationships (with gaussian processes/gaussian random fields);
    - Missing data imputation;
    - Measurement error.

2. Manually gather the coordinates for ~640 schools (this will be fun...).

3. Fit the model analyze the results (this will actually be fun, but it never 
lasts).

4. Write an article about it. The idea is to have a more technical case study
on using complex models with small data sets (similar to [Michael Betancourt's](https://betanalpha.github.io/writing/) 
case studies, but with more applied, rather than introductory, material), and
then a more accessible article showing the results with a dashboard. 

### Major to-do tasks for the second question

1. Figure out the causal model. I am pretty sure I can't put every variable in there.  
2. Based on the causal model, merge the data sets with whatever is needed.
3. Build a model for this (similar to the first one, but simpler). 


