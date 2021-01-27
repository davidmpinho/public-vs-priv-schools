from itemadapter import ItemAdapter
import pandas as pd
from sqlalchemy import create_engine


class SqlitePipeline:
    def process_item(self, item, spider):
        d_item = ItemAdapter(item).asdict()
        print('Processing item ' + item['name_file'])

        def df_dict(d):
            return pd.DataFrame.from_dict(d)
        engine = create_engine('sqlite://' + spider.path_db
                               + item['name_file'] + '.sqlite')

        # TODO: add if_exists='replace' to .to_sql
        df_dict(d_item['table_main']
                ).to_sql('grades', con=engine)
        df_dict(d_item['table_aux']['grade_averages']['exam']
                ).to_sql('grade_averages_exam', con=engine)
        df_dict(d_item['table_aux']['grade_averages']['internal']
                ).to_sql('grade_averages_internal', con=engine)
        df_dict(d_item['table_aux']['retention_rate']['school_average']
                ).to_sql('ret_rate_school', con=engine)
        df_dict(d_item['table_aux']['indicators']['school_average']
                ).to_sql('indicator_school', con=engine)
        df_dict(d_item['table_aux']['parents_education']
                ).to_sql('parental_edu', con=engine)
        # TODO: close connection
        return item

class CsvPipeline:
    def process_item(self, item, spider):
        print('Processing item ' + item['name_file'])
        d_item = ItemAdapter(item).asdict()

        # TODO: add the html file names to the files 
        # TODO: change the names of repeated columns (those are mentioned in the shell scripts)
        def df_dict(d):
            return pd.DataFrame.from_dict(d)
        df_dict(d_item['table_main']
                ).to_csv('./data/output/grades.csv')
        df_dict(d_item['table_aux']['grade_averages']['exam']
                ).to_csv('./data/output/grade_averages_exam.csv')
        df_dict(d_item['table_aux']['grade_averages']['internal']
                ).to_csv('./data/output/grade_averages_internal.csv')
        df_dict(d_item['table_aux']['retention_rate']['school_average']
                ).to_csv('./data/output/ret_rate_school.csv')
        df_dict(d_item['table_aux']['indicators']['school_average']
                ).to_csv('./data/output/indicator_school.csv')
        df_dict(d_item['table_aux']['parents_education']
                ).to_csv('./data/output/parental_edu.csv')

        # TODO: this return statement is causing the dict to be in the logs.
        # But without it nothing works; I think yield gave the same issue
        return item

