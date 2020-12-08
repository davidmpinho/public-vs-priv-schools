import scrapy
import re
from school_rank.items import SchoolRankItem

# TODO: I am pretty sure I can start with /tbody/ and this will pick it up, although I am not sure.
class SchoolRankSpider(scrapy.Spider):
    name = 'school_rank_spider'

    def __init__(self, category=None, *args, **kwargs):
        super(SchoolRankSpider, self).__init__(*args, **kwargs)
        folder_name = 'file://' + kwargs.get('folder_name')
        self.path_db = kwargs.get('path_db')
        self.start_urls = [folder_name + s for s in kwargs.get('file_names')]

    def parse(self, response, **kwargs):
        self.logger.info(f"Parsing {response.url}")
        xpath_table_main_cols = '//body/div/main/div/div/div/table/thead/tr/th/span'
        xpath_table_main_text = ('//body/div/main/div/div/div/table/tbody/tr'
                                 + '[contains(@class, "id_")]')
        xpath_tables_aux = ('//body/div/main/div/div/div/table/tbody/tr'
                            + '[contains(@class, "columnDetails")]')

        table_main_cols = ['number'] + [
            x for x in response.xpath(xpath_table_main_cols + '//text()').getall()]
        text_table_main = response.xpath(xpath_table_main_text + '//text()').getall()
        text_table_main = self.clean_text_list(text_list=text_table_main)
        dict_table_main = self.table_main_to_dict(columns=table_main_cols,
                                                  text=text_table_main,
                                                  start_col=0, end_col=7, mod=8)
        dict_table_main = self.add_pubpri_to_dict(
            xpath_text=[str(x) for x in response.xpath(xpath_table_main_text)],
            dictionary=dict_table_main)

        table_aux_selectors = response.xpath(
            xpath_tables_aux + '/td[contains(@class, "columnDetailsInner")]')
        dict_table_aux = self.tables_aux_to_dict(selectors=table_aux_selectors)

        item = SchoolRankItem()
        item['name_file'] = response.url.split('/')[-1].split('.')[0]
        item['table_main'] = dict_table_main
        item['table_aux'] = dict_table_aux
        return item

    @staticmethod
    def clean_text_list(text_list: list) -> list:
        text_list = [text.strip() for text in text_list]
        text_list = [text for text in text_list if text != '']
        return text_list

    @staticmethod
    def table_main_to_dict(columns: list, text: list, start_col: int,
                      end_col: int, mod: int) -> dict:
        dictionary = {}
        for i in range(start_col, end_col+1):
            dictionary.update(
                {columns[i]: [x for j, x in enumerate(text) if ((j-i) % mod) == 0]})
        return dictionary

    @staticmethod
    def add_pubpri_to_dict(xpath_text: list, dictionary: dict) -> dict:
        pub_or_pri = [re.findall(r'(pub|pri)', x) for x in xpath_text]
        pub_or_pri = [y for x in pub_or_pri for y in x]
        dictionary['pub_or_pri'] = pub_or_pri
        return dictionary

    @staticmethod
    def ith_value_of_list(lst: list, i: int, mod: int) -> list:
        return [x for j, x in enumerate(lst) if (((j - i) % mod) == 0)]

    def tables_aux_to_dict(self, selectors: list) -> dict:
        dictionary = {}
        tables_selector = selectors.xpath('./table[not(contains(@class, "tableExtra"))]')
        data = self.clean_text_list(tables_selector.xpath('.//text()').getall())
        dictionary['grade_averages'] = {'exam': {
            'biology_geology': self.ith_value_of_list(lst=data, mod=45, i=4),
            'math': self.ith_value_of_list(lst=data, mod=45, i=7),
            'portuguese': self.ith_value_of_list(lst=data, mod=45, i=10),
            'physics_chemistry': self.ith_value_of_list(lst=data, mod=45, i=13)},
                                       'internal': {
            'biology_geology': self.ith_value_of_list(lst=data, mod=45, i=5),
            'math': self.ith_value_of_list(lst=data, mod=45, i=8),
            'portuguese': self.ith_value_of_list(lst=data, mod=45, i=11),
            'physics_chemistry': self.ith_value_of_list(lst=data, mod=45, i=14)}}
        dictionary['retention_rate'] = {'school_average': {
            '12th_grade': self.ith_value_of_list(lst=data, mod=45, i=19),
            '11th_grade': self.ith_value_of_list(lst=data, mod=45, i=22),
            '10th_grade': self.ith_value_of_list(lst=data, mod=45, i=25)},
                                        'national_average': {
            '12th_grade': self.ith_value_of_list(lst=data, mod=45, i=20),
            '11th_grade': self.ith_value_of_list(lst=data, mod=45, i=23),
            '10th_grade': self.ith_value_of_list(lst=data, mod=45, i=26)}}
        dictionary['indicators'] = {'school_average': {
            'pct_stud_in_need_12th_grade': self.ith_value_of_list(lst=data, mod=45, i=28),
            'pct_profs_on_the_board': self.ith_value_of_list(lst=data, mod=45, i=31)},
                                    'national_average': {
            'pct_stud_in_need_12th_grade': self.ith_value_of_list(lst=data, mod=45, i=29),
            'pct_profs_on_the_board': self.ith_value_of_list(lst=data, mod=45, i=32)}}
        dictionary['parents_education'] = {
            'average_dads': self.ith_value_of_list(lst=data, mod=45, i=36),
            'average_moms': self.ith_value_of_list(lst=data, mod=45, i=37)}
        dictionary['ranking'] = {
            '2019': self.ith_value_of_list(lst=data, mod=45, i=42),
            '2018': self.ith_value_of_list(lst=data, mod=45, i=43),
            'change': self.ith_value_of_list(lst=data, mod=45, i=44)}
        return dictionary

