import os
import re
import warnings
import pandas_access as pa
from pyunpack import Archive
import sqlite3


def extract_zip_rar(path):
    not_zip_rar = 0
    for f in os.listdir(path):
        if re.search(r'\.zip', f) is not None:
            Archive(path + f).extractall_zipfile(path)
        elif re.search(r'\.rar', f) is not None:
            Archive(path + f).extractall(path)
        else:
            not_zip_rar += 1
    if not_zip_rar > 0:
        warnings.warn(f'There were {not_zip_rar} files that are not rar or zip.')


def mdb_to_sqlite(path_mdb, path_output):
    files_mdb = [x for x in os.listdir(path_mdb) if x.endswith('.mdb')]
    for file in files_mdb:
        db_name = f"dges_{re.search('20[0-9][0-9]', file).group()}.sqlite"
        db_path = f'{path_mdb}{file}'
        con = sqlite3.connect(path_output + db_name)
        for table in pa.list_tables(db_path):
            df = pa.read_table(db_path, table)
            df.to_sql(table, con=con, if_exists='replace')
        con.close()
        os.remove(db_path)
