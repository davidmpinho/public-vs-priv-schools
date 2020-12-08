import sqlite3
import pandas as pd
import numpy as np
import sys


def remove_pct(string: str) -> str:
    if pd.isnull(string):
        pass
    elif isinstance(string, str):
        string = string.replace('%', '')
    else:
        sys.exit("Passed object is not a string or null.")
    return string

def str_to_float(string: str) -> float:
    if pd.isnull(string) | isinstance(string, float):
        pass
    elif isinstance(string, str):
        string = string.replace(',', '.')
    else:
        sys.exit("Passed object is not a string, float, or null.")
    return float(string)


db_conn = sqlite3.connect('./../data/clean_output/agg_db.sqlite')
data_scrape_raw = pd.read_sql(sql="select * from all_data;", con=db_conn)

# Clean the data -- this is supposed to have the data for ALL models
col_map = {
    'Escola': 'school',
    'Média': 'average_internal_and_exam',
    'N.º Provas': 'school_n_exams',
    'Concelho': 'county',
    '12th_grade': 'rate_flunk_12th',
    '11th_grade': 'rate_flunk_11th',
    '10th_grade': 'rate_flunk_10th'}
relevant_cols = ['pub_or_pri', 'rate_flunk_12th',
                 'rate_flunk_11th', 'rate_flunk_10th']

data_scrape_clean = (data_scrape_raw
    .copy()
    .drop(['index', 'number', 'Pos. +100 Provas',
           'Pos. Geral', 'Indicador de Sucesso'], axis=1)
    .rename(columns=col_map)
    .replace(to_replace={'--': np.nan})
    .groupby(['school', 'year_exam'])
    .first()[relevant_cols]
    .reset_index())
for col in ['rate_flunk_12th', 'rate_flunk_11th', 'rate_flunk_10th']:
    data_scrape_clean[col] = data_scrape_clean[col].apply(remove_pct).apply(str_to_float)

# TODO: now go get the other data and form the actual columns for it (exams, year, etc.)
# I had a lot of this done in the python script already

# The data should be in python dictionaries on their own files.
# For stan, the data should be in a file with a dictionary (which includes missing data)
# But I should also save the joint data in a dataframe so that I can use it more
# easily.

