import os
from school_rank.spiders.school_rank_spider import SchoolRankSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.school_rank.test.test_school_rank_spider import SchoolRankTest
from src.data_tools.db_tools import extract_zip_rar, mdb_to_sqlite
from src.data_tools.processing_tools import process_and_save_data

# Data for the first study ---------------------------------------------------------------
PATH_CWD = os.path.dirname(os.path.abspath('__file__'))  # This will be the /src/ folder
PATH_DATA = PATH_CWD + '/../data/'
PATH_DATA_RAW = PATH_DATA + 'raw/'
PATH_DATA_INTERIM = PATH_DATA + 'interim/'
PATH_DATA_PROCESSED = PATH_DATA + 'processed/'

process = CrawlerProcess(get_project_settings())
process.crawl(SchoolRankSpider,
              folder_name=PATH_DATA + 'html/',
              file_names=['tables_2019.html', 'tables_2018.html',
                          'tables_2017.html', 'tables_2016.html'], # Needs to have 2016 in the name
              path_db='/../data/interim/')
process.start()

# Data for the second study --------------------------------------------------------------
extract_zip_rar(path=PATH_DATA_RAW)
mdb_to_sqlite(path_mdb=PATH_DATA_RAW, path_output=PATH_DATA_INTERIM)

# Aggregate tables and save them ---------------------------------------------------------
# TODO: instead of shell scripts, save those files as SQL scripts and run them through here.
# Do not forget to delete the relevant files and such.


# Generate and save the processed data (i.e., data ready for modelling) ----------------
extract_zip_rar(path=PATH_DATA_INTERIM)
process_and_save_data(path_iave=PATH_DATA_INTERIM + 'iave_db.csv',
                      path_coords=PATH_DATA_INTERIM + 'school_coords.csv',
                      path_dges=PATH_DATA_INTERIM + 'dges_db.csv',
                      path_processed=PATH_DATA_PROCESSED)
# Delete useless files
files_del = [PATH_DATA_INTERIM + x for x in ['school_coords.csv', 'dges_db.csv', 'iave_db.csv']]
for f in files_del:
    try:
        os.remove(f)
    except FileNotFoundError:
        pass
