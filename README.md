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
using student-level data from [IAVE](https://www.dge.mec.pt/relatoriosestatisticas-0).

### Major TODOs for the first question

1. Continue building Stan models and the respective simulations (in
/python_scripts/stan_utils/sim_helper.py) that allow for:
    - Spatial relationships (with gaussian processes/gaussian random fields)
    - Missing data imputation
    - Measurement error

2. Make corrections to the 2016 data set (the website I'm scraping it from has
a different format for the tables in that year). 

3. Manually gather the coordinates ~640 schools (this will be fun...).

4. Fit the model analyze the results (this will actually be fun, but it never 
lasts).

5. Write an article about it (maybe with a dashboard?).

### Major TODOs for the second question

1. Everything (but it is *much* more straightforward to model this and clean
the data).




