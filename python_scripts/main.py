import os
from adjust_2016_data import correct_2016_html
from school_rank.spiders.school_rank_spider import SchoolRankSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from school_rank.test.test_school_rank_spider import SchoolRankTest


PATH_CWD = os.path.dirname(os.path.abspath('__file__'))  # This is '/python_scripts/'
PATH_DATA = PATH_CWD + '/../data/'
PATH_SCHOOL_RANK = PATH_CWD + '/python_scripts/school_rank/'

process = CrawlerProcess(get_project_settings())
process.crawl(SchoolRankSpider,
              folder_name=PATH_DATA + 'html/',
              file_names=['tables_2019.html', 'tables_2018.html', 'tables_2017.html'],
              path_db='/../data/output/')
process.start()
