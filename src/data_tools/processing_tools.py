import sqlite3
import pandas as pd
import numpy as np
import sys
from src.data_tools.db_tools import extract_zip_rar


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

def cols_change_list() -> list:
    """ Returns the list of columns that need to be processed."""
    cols_s1_change = ['12th_grade', '11th_grade', '10th_grade',
                      'Indicador de Sucesso', 'pct_stud_in_need_12th_grade',
                      'pct_profs_on_the_board', 'average_moms', 'average_dads', 'Média']
    return cols_s1_change


def cols_filter_list():
    """ Returns the list of columns that are relevant for the analysis."""
    cols_s1_filter = ['12th_grade', '11th_grade', '10th_grade',
                      'pct_stud_in_need_12th_grade', 'pct_profs_on_the_board',
                      'average_dads', 'average_moms', 'year_exam', 'Indicador de Sucesso',
                      'Concelho', 'Pos. Geral', 'Média', 'Escola']
    cols_s2_filter= ['Fase', 'ParaAprov', 'Interno', 'ParaMelhoria', 'ParaIngresso',
                     'ParaCFCEPE', 'TemInterno', 'Sexo', 'Idade', 'Curso', 'EscolaDescr',
                     'ExameDescr', 'DistritoDescr', 'CIF', 'Class_Exam', 'CFD',
                     'year_exam', 'PubPriv', 'TpCursoDescr', 'SubTipoDescr',
                     'SitFreqDescr', 'Ano_Ini', 'Nuts3Descr']
    return cols_s1_filter, cols_s2_filter


def cols_rename_dict():
    cols_s1_rename = {
        'Escola': 'school_name',
        'Concelho': 'county',
        'Indicador de Sucesso': 'success_indicator',
        'Pos. Geral': 'published_rank',
        'Média': 'published_grade',
        '12th_grade': 'rate_flunk_12th',
        '11th_grade': 'rate_flunk_11th',
        '10th_grade': 'rate_flunk_10th'}
    cols_s2_rename= {
        'Fase': 'exam_phase',
        'ParaAprov': 'for_approval',
        'Interno': 'is_internal',
        'ParaMelhoria': 'for_improvement',
        'ParaIngresso': 'for_entrance',
        'ParaCFCEPE': 'for_cfcepe',
        'TemInterno': 'has_internal',
        'Sexo': 'sex',
        'Idade': 'age',
        'Curso': 'school_track',
        'EscolaDescr': 'school_name',
        'ExameDescr': 'exam_disc',
        'DistritoDescr': 'district',
        'ConcelhoDescr': 'county',
        'CIF': 'grade_internal',
        'Class_Exam': 'grade_exam',
        'CFD': 'grade_final',
        'TpCursoDescr': 'school_track_type',
        'SubTipoDescr': 'school_track_subtype',
        'SitFreqDescr': 'situation_student',
        'Ano_Ini': 'initial_year',
        'PubPriv': 'pub_or_priv',
        'Nuts3Descr': 'nuts3_zone'
    }
    return cols_s1_rename, cols_s2_rename

def school_rename_dict():
    school_names = {
        'Escola Básica e Secundária com Pré-escolar da Calheta': 'Escola Básica e Secundária da Calheta',
        'Colégio Oficinas de São José': 'Escola Secundária Gonçalo Anes Bandarra, Trancoso',
        'Instituto Diocesano de Formação João Paulo II': 'Escola Portuguesa de São Tomé e Príncipe',
        'Externato Infante D. Henrique - ALFACOOP, Braga': 'Externato Infante D. Henrique',
        'Escola Secundária de Padrão da Légua': 'Escola Básica e Secundária de Padrão da Légua',
        'Escola Artística Soares dos Reis, Porto': 'Escola Artística Soares dos Reis',
        'Instituto de Educação e Desenvolvimento - INED': 'Escola INED - Nevogilde'
    }
    return school_names

def fix_school_names_s1(data: pd.DataFrame) -> pd.DataFrame:
    """
    One of the schools (Escola Básica e Secundária da Calheta)
    had two rows that were almost, but not completely, repeated.
    The ranks and everything else were very similar, I do not find
    any differences between the two schools, so I suppose it was an
    error on their part.
    """
    data.loc[:, 'school_name'] = data['school_name'].replace(to_replace=school_rename_dict())
    mask = data['school_name'] == 'Escola Básica e Secundária da Calheta'
    indexes_to_exclude = data.loc[mask, :].index[np.arange(start=1, stop=8, step=2)]
    data = data.drop(indexes_to_exclude)
    return data

def fix_school_names_s2(data: pd.DataFrame) -> pd.DataFrame:
    data.loc[:, 'school_name'] = data['school_name'].replace(to_replace=school_rename_dict())
    return data

def fix_school_names_coords(data: pd.DataFrame) -> pd.DataFrame:
    data.loc[:, 'school_name'] = data['school_name'].replace(to_replace=school_rename_dict())
    data = data.groupby(['school_name']).mean().reset_index()
    return data

def adjust_grade_format(data_s1: pd.DataFrame, data_s2: pd.DataFrame) -> tuple:
    data_s1['published_grade'] = data_s1['published_grade'] * 10
    data_s2['grade_final'] = data_s2['grade_final'] * 10
    fill_grade_final = np.where(data_s2['grade_final'].isna(),
                                (data_s2['grade_exam'] * 0.3
                                 + data_s2['grade_internal'] * 0.7),
                                data_s2['grade_exam'])
    data_s2.loc[:, 'grade_final'] = fill_grade_final
    return data_s1, data_s2

def process_and_save_data(path_iave, path_coords, path_dges, path_processed):
    """
    Cleans the data for study 1 and study 2.
    """
    cols_s1_change = cols_change_list()
    cols_s1_filter, cols_s2_filter = cols_filter_list()
    cols_s1_rename, cols_s2_rename = cols_rename_dict()

    data_s1 = pd.read_csv(path_iave).replace(to_replace={'--': np.nan})
    data_s2 = pd.read_csv(path_dges, low_memory=False).replace(to_replace={'--': np.nan})
    data_coords = pd.read_csv(path_coords)

    # Fix errors/inconsistencies with the data set
    for col in cols_s1_change:
        data_s1[col] = data_s1[col].apply(remove_pct).apply(str_to_float)
    data_coords = data_coords.pipe(fix_school_names_coords)
    data_s1 = (data_s1.filter(items=cols_s1_filter)
                      .rename(columns=cols_s1_rename)
                      .join(how='outer', other=data_coords.set_index('school_name'),
                            on='school_name')
                      .reset_index(drop=True)
                      .pipe(fix_school_names_s1))
    data_s2 = (data_s2.filter(items=cols_s2_filter)
                      .rename(columns=cols_s2_rename)
                      .pipe(fix_school_names_s2))
    data_s2 = data_s2.replace(to_replace={'f': 'F', 'm': 'M', 'N': 0, 'S': 1})
    data_s1 = data_s1.replace(to_replace={'N': 0, 'S': 1})
    data_s1, data_s2 = adjust_grade_format(data_s1, data_s2)

    # Create the final data sets and save them
    data_s2 = (data_s2.join(other=data_s1.set_index(['school_name', 'year_exam']),
                            how='outer', on=['school_name', 'year_exam'])
                      .dropna(subset=['grade_exam']))  # Because year_exam is NAN in some schools
    data_s1 = (data_s2.groupby(['school_name', 'exam_disc', 'exam_phase', 'year_exam'])
                      .mean()
                      .reset_index())
    data_s1.to_csv(path_processed + 'data_study_1.zip',
                   compression={'method': 'zip', 'archive_name': 'data_study_1.csv'})
    data_s2.to_csv(path_processed + 'data_study_2.zip',
                   compression={'method': 'zip', 'archive_name': 'data_study_2.csv'})
