import os
import sys
import unittest

dir_py_scripts = '/'.join(os.getcwd().split('/')[0:-2])
sys.path.insert(0, dir_py_scripts)
from school_rank.spiders.school_rank_spider import SchoolRankSpider


class SchoolRankTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self) -> None:
        path_data = os.path.dirname(os.path.abspath('__file__')) + '/../data/'
        self.srs_inst = SchoolRankSpider(
            folder_name=path_data + 'html/',
            file_names=['tables_2019.html',
                        'tables_2018.html',
                        'tables_2017.html',
                        'tables_2016_adjusted.html'],
            path_db='/../data/output/')

    def tearDown(self) -> None:
        self.srs_inst = None

    def test_clean_text_list(self):
        mock_text_list = ['', ' ', 'a', 'b', '    ']
        mock_text_list = self.srs_inst.clean_text_list(text_list=mock_text_list)
        self.assertEqual(mock_text_list, ['a', 'b'])

    def test_table_main_to_dict(self):
        mock_columns = ['a', 'b', 'c']
        mock_text = list(range(0, 3*3))
        mock_dict = self.srs_inst.table_main_to_dict(columns=mock_columns, text=mock_text,
                                                start_col=0, end_col=2, mod=3)

        self.assertEqual(list(mock_dict.keys()), mock_columns)
        self.assertEqual(mock_dict['a'], [0, 3, 6])
        self.assertEqual(mock_dict['b'], [1, 4, 7])
        self.assertEqual(mock_dict['c'], [2, 5, 8])

    def test_add_pubpri_to_dict(self):
        xpath_text = [
            """< Selector xpath = '//body/div/main/div/div/div/table/tbody/tr[contains(@class, 
               id_ ")]' data = '<tr class="id_  rank_up type_pub resu...' >""",
            """< Selector xpath = '//body/div/main/div/div/div/table/tbody/tr[contains(@class, 
               id_ ")]' data = '<tr class="id_  rank_up type_pri resu...' >"""]
        dictionary = self.srs_inst.add_pubpri_to_dict(xpath_text=xpath_text, dictionary={})
        self.assertEqual(dictionary['pub_or_pri'], ['pub', 'pri'])

    def test_int_value_of_list(self):
        mock_list = list(range(45*3))
        mock_list1 = self.srs_inst.ith_value_of_list(lst=mock_list, i=0, mod=45)
        mock_list2 = self.srs_inst.ith_value_of_list(lst=mock_list, i=1, mod=45)
        self.assertEqual(mock_list1, [0, 45, 90])
        self.assertEqual(mock_list2, [1, 46, 91])


if __name__ == '__main__':
    unittest.main()
