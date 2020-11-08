import concurrent.futures
import pandas
import requests
from bs4 import BeautifulSoup, SoupStrainer

gene_file = open('genes.txt', 'r')
GENES = gene_file.read().split('\n')
only_white_bkg_class = SoupStrainer(class_='white_bkg')


def get_gene_data(gene):
    matches = []

    r = requests.get(f'https://spell.yeastgenome.org/search/show_results?num_genes=20&search_string={gene}')
    raw_cookie = r.cookies['_spell_session']
    cookie = '_spell_session=' + raw_cookie + ';'

    print(f'Getting {gene} data')
    url = 'https://spell.yeastgenome.org/search/expr_results'
    payload = {'referer': f'https://spell.yeastgenome.org/search/show_results?num_genes=20&search_string={gene}', 'cookie': cookie}

    r = requests.post(url, headers=payload)

    soup = BeautifulSoup(r.text, 'html.parser', parse_only=only_white_bkg_class)

    # 13 to 22 are the top 10 genes
    # min is 13
    # max is 43
    for i in range(13, 23):
        matches.append(soup.find_all('td', class_='white_bkg')[i].get_text())
    
    matches.append('')
    return matches


if __name__ == '__main__':
    result = []

    with concurrent.futures.ProcessPoolExecutor() as executor:
        processes = [executor.submit(get_gene_data, gene) for gene in GENES]

        for f in concurrent.futures.as_completed(processes):
            result += f.result()
    
    matches_df = pandas.DataFrame(result, columns=['Genes'])
    writer = pandas.ExcelWriter('raw_matches.xlsx', engine='xlsxwriter')
    matches_df.to_excel(writer)
    writer.save()
