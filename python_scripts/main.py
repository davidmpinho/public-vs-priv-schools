import os
from school_rank.spiders.school_rank_spider import SchoolRankSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from school_rank.test.test_school_rank_spider import SchoolRankTest
from db_code.clean_dges_db import extract_zip_rar, mdb_to_sqlite


# Data for the first study ---------------------------------------------------------------
PATH_CWD = os.path.dirname(os.path.abspath('__file__'))  # This will be the folder 'python_scripts'
PATH_DATA = PATH_CWD + '/../data/'
PATH_DATA_STUDY_2 = PATH_DATA + 'dges/'
PATH_SCHOOL_RANK = PATH_CWD + '/python_scripts/school_rank/'
PATH_DATA_OUTPUT = PATH_DATA + 'output/'
PATH_DATA_C_OUTPUT = PATH_DATA + 'clean_output/'

process = CrawlerProcess(get_project_settings())
process.crawl(SchoolRankSpider,
              folder_name=PATH_DATA + 'html/',
              file_names=['tables_2019.html',
                          'tables_2018.html',
                          'tables_2017.html',
                          'tables_2016.html'], # Needs to have 2016 in the name
              path_db='/../data/output/')
process.start()


# Data for the second study --------------------------------------------------------------
extract_zip_rar(path=PATH_DATA_STUDY_2)
mdb_to_sqlite(path_mdb=PATH_DATA_STUDY_2, path_output=PATH_DATA_OUTPUT)
