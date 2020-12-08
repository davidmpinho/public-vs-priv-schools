import codecs
from bs4 import BeautifulSoup as soup


def correct_2016_html(path_html_2016: str, path_output_html: str):
    """Changes the 2016 html file to match the others (this is less
    messy than changing the code)."""
    # TODO: There are other problems with the 2016 file, fix those. 
    html = codecs.open(path_html_2016, 'r', 'utf-8')
    soup_html = soup(html.read(), 'html.parser')
    html_tables = soup_html.findAll(attrs={'class': 'columnDetailsInner',
                                           'colspan': '7'})

    def get_new_tr(soup_html: soup) -> soup.new_tag:
        """Get tags for column names that are missing in the 2016
        file relative to all other files."""
        new_tr = soup_html.new_tag('tr')
        tr_empty = soup_html.new_tag('th', attrs={'class': 'column'})
        tr_school = soup_html.new_tag('th', attrs={'class': 'column'})
        tr_school.string = 'Média na Escola'
        tr_national = soup_html.new_tag('th', attrs={'class': 'column'})
        tr_national.string = 'Média Nacional'
        new_tr.append(tr_empty)
        new_tr.append(tr_school)
        new_tr.append(tr_national)
        return new_tr

    def get_new_td(soup_html: soup) -> soup.new_tag:
        """Get tags for a column that is missing ('Média Nacional'). """
        new_td = soup_html.new_tag('td', attrs={'class': 'column'})
        new_td.string = '--'
        return new_td

    for table in html_tables:
        new_tr = get_new_tr(soup_html=soup_html)
        table_head = table.findAll('table')[2].find('thead')
        table_head.append(new_tr)

        for table_tr in table.findAll('table')[2].find('tbody').findAll('tr'):
            new_td = get_new_td(soup_html=soup_html)
            table_tr.append(new_td)

    with open(path_output_html, 'w', encoding='utf-8') as file:
        file.write(str(soup_html))

