# %% Código para a raspagem de dados do site do NBB, temporada 2019-2020

# %% configurações iniciais
# importa as bibliotecas
import requests
from bs4 import BeautifulSoup
import pandas as pd

# %% extração do html
# monta lista de categorias
categorias = ['pontos', 'rebotes', 'assistencias',
              'arremessos', 'bolas-recuperadas', 'tocos',
              'erros', 'eficiencia', 'duplos-duplos']

# monta dicionário de urls
url_suffix = '/?aggr=avg&type=athletes&suffered_rule=0&season%5B%5D=54&wherePlaying=-1'
lista_urls = [
    f'https://lnb.com.br/nbb/estatisticas/{categoria+url_suffix}' for categoria in categorias
    ]
urls = dict(zip(categorias, lista_urls))

# captura a resposta http dos urls de cada tabela
lista_responses = [requests.get(urls[categoria]) for categoria in categorias]
responses = dict(zip(categorias, lista_responses))

# força codificação do texto para UTF-8
for response in responses:
    responses[response].encoding = 'utf-8'

# extrai html das respostas http
lista_textos_html = [responses[categoria].text for categoria in categorias]
htmls = dict(zip(categorias, lista_textos_html))

# cria objeto BeuatifulSoup para a análise do html
lista_soups = [BeautifulSoup(htmls[categoria], 'html.parser') for categoria in categorias]
soups = dict(zip(categorias, lista_soups))

# captura html das linhas das tabelas
lista_html_linhas = [soups[categoria].find_all('tr') for categoria in categorias]
html_linhas = dict(zip(categorias, lista_html_linhas))

# %% começa a construção da tabela de Pontos
# cria dicionário para armanzenar a tabela
categorias_pontos = ['pos', 'jogador', 'equipe',
                     'jo', 'min', 'pts',
                     '3p', '2p', 'll']
matriz_vazia_pontos = [[], [], [],
                       [], [], [],
                       [], [], []]
tabela_pontos = dict(zip(categorias_pontos, matriz_vazia_pontos))

# preenche tabela_pontos
for linha in html_linhas['pontos']:
    try:
        tabela_pontos['pos'].append(int(linha.find('td', {'class': 'headcol-2'}).text))
        tabela_pontos['jogador'].append(linha.find('td', {'class': 'headcol'}).text)
        tabela_pontos['equipe'].append(linha.find_all('a')[1].text)
        tabela_pontos['jo'].append(int(linha.find_all('td')[3].text))
        tabela_pontos['min'].append(float(linha.find_all('td')[4].text))
        tabela_pontos['pts'].append(float(linha.find_all('td')[5].text))
        tabela_pontos['3p'].append(float(linha.find_all('td')[6].text))
        tabela_pontos['2p'].append(float(linha.find_all('td')[7].text))
        tabela_pontos['ll'].append(float(linha.find_all('td')[8].text))
    except:
        pass

# transforma tabela_pontos em DataFrame e o apresenta
tabela_pontos_df = pd.DataFrame(tabela_pontos, index=None)

# %% começa a construção da tabela de Rebotes
# cria dicionário para armazenar a tabela
categorias_rebotes = ['pos', 'jogador', 'equipe',
                      'jo', 'min', 'rt',
                      'ro', 'rd']
matriz_vazia_rebotes = [[], [], [], 
                        [], [], [],
                        [], []]
tabela_rebotes = dict(zip(categorias_rebotes, matriz_vazia_rebotes))

# preenche tabela_rebotes
for linha in html_linhas['rebotes']:
    try:
        tabela_rebotes['pos'].append(int(linha.find('td', {'class': 'headcol-2'}).text))
        tabela_rebotes['jogador'].append(linha.find('td', {'class': 'headcol'}).text)
        tabela_rebotes['equipe'].append(linha.find_all('a')[1].text)
        tabela_rebotes['jo'].append(int(linha.find_all('td')[3].text))
        tabela_rebotes['min'].append(float(linha.find_all('td')[4].text))
        tabela_rebotes['rt'].append(float(linha.find_all('td')[5].text))
        tabela_rebotes['ro'].append(float(linha.find_all('td')[6].text))
        tabela_rebotes['rd'].append(float(linha.find_all('td')[7].text))
    except:
        pass

tabela_rebotes_df = pd.DataFrame(tabela_rebotes)

# %% começa a construção da tabela de Assistências
# cria dicionário para armazenar a tabela
categorias_assistencias = ['pos', 'jogador', 'equipe',
                           'jo', 'min', 'as',
                           'er', 'ia_pct']
matriz_vazia_assistencias = [[], [], [], 
                             [], [], [],
                             [], []]
tabela_assistencias = dict(zip(categorias_assistencias, matriz_vazia_assistencias))

# preenche tabela_assistencias
for linha in html_linhas['assistencias']:
    try:
        tabela_assistencias['pos'].append(int(linha.find('td', {'class': 'headcol-2'}).text))
        tabela_assistencias['jogador'].append(linha.find('td', {'class': 'headcol'}).text)
        tabela_assistencias['equipe'].append(linha.find_all('a')[1].text)
        tabela_assistencias['jo'].append(int(linha.find_all('td')[3].text))
        tabela_assistencias['min'].append(float(linha.find_all('td')[4].text))
        tabela_assistencias['as'].append(float(linha.find_all('td')[5].text))
        tabela_assistencias['er'].append(float(linha.find_all('td')[6].text))
        tabela_assistencias['ia_pct'].append(float(linha.find_all('td')[7].text))
    except:
        pass

tabela_assistencias_df = pd.DataFrame(tabela_assistencias)

# %% começa a construção da tabela de Arremessos
# cria dicionário para armazenar a tabela
categorias_arremessos = ['pos', 'jogador', 'equipe',
                         'jo', 'min', 'pts',
                         '3pc', '3pt', '3p_pct',
                         '2pc', '2pt', '2p_pct',
                         'llc', 'llt', 'll_pct',
                         'en']
matriz_vazia_arremessos = [[], [], [], 
                           [], [], [],
                           [], [], [],
                           [], [], [],
                           [], [], [],
                           []]
tabela_arremessos = dict(zip(categorias_arremessos, matriz_vazia_arremessos))

# preenche tabela_arremessos
for linha in html_linhas['arremessos']:
    try:
        tabela_arremessos['pos'].append(int(linha.find('td', {'class': 'headcol-2'}).text))
        tabela_arremessos['jogador'].append(linha.find('td', {'class': 'headcol'}).text)
        tabela_arremessos['equipe'].append(linha.find_all('a')[1].text)
        tabela_arremessos['jo'].append(int(linha.find_all('td')[3].text))
        tabela_arremessos['min'].append(float(linha.find_all('td')[4].text))
        tabela_arremessos['pts'].append(float(linha.find_all('td')[5].text))
        tabela_arremessos['3pc'].append(float(linha.find_all('td')[6].text))
        tabela_arremessos['3pt'].append(float(linha.find_all('td')[7].text))
        tabela_arremessos['3p_pct'].append(float(linha.find_all('td')[8].text))
        tabela_arremessos['2pc'].append(float(linha.find_all('td')[9].text))
        tabela_arremessos['2pt'].append(float(linha.find_all('td')[10].text))
        tabela_arremessos['2p_pct'].append(float(linha.find_all('td')[11].text))
        tabela_arremessos['llc'].append(float(linha.find_all('td')[12].text))
        tabela_arremessos['llt'].append(float(linha.find_all('td')[13].text))
        tabela_arremessos['ll_pct'].append(float(linha.find_all('td')[14].text))
        tabela_arremessos['en'].append(float(linha.find_all('td')[15].text))
    except:
        pass

tabela_arremessos_df = pd.DataFrame(tabela_arremessos)

# %% começa a construção da tabela de Bolas Recuperadas
# cria dicionário para armazenar a tabela
categorias_bolas_recuperadas = ['pos', 'jogador', 'equipe',
                                'jo', 'min', 'br',
                                'er', 'b_e']
matriz_vazia_bolas_recuperadas = [[], [], [],
                                  [], [], [],
                                  [], []]
tabela_bolas_recuperadas = dict(zip(categorias_bolas_recuperadas, matriz_vazia_bolas_recuperadas))

# preenche tabela_bolas_recuperadas
for linha in html_linhas['bolas-recuperadas']:
    try:
        tabela_bolas_recuperadas['pos'].append(int(linha.find('td', {'class': 'headcol-2'}).text))
        tabela_bolas_recuperadas['jogador'].append(linha.find('td', {'class': 'headcol'}).text)
        tabela_bolas_recuperadas['equipe'].append(linha.find_all('a')[1].text)
        tabela_bolas_recuperadas['jo'].append(int(linha.find_all('td')[3].text))
        tabela_bolas_recuperadas['min'].append(float(linha.find_all('td')[4].text))
        tabela_bolas_recuperadas['br'].append(float(linha.find_all('td')[5].text))
        tabela_bolas_recuperadas['er'].append(float(linha.find_all('td')[6].text))
        tabela_bolas_recuperadas['b_e'].append(float(linha.find_all('td')[7].text))
    except:
        pass

tabela_bolas_recuperadas_df = pd.DataFrame(tabela_bolas_recuperadas)

# %% começa a construção da tabela de Tocos
# cria dicionário para armazenar a tabela
categorias_tocos = ['pos', 'jogador', 'equipe',
                    'jo', 'min', 'to',
                    'fc', 't_fc']
matriz_vazia_tocos = [[], [], [], 
                      [], [], [],
                      [], []]
tabela_tocos = dict(zip(categorias_tocos, matriz_vazia_tocos))

# preenche tabela_tocos
for linha in html_linhas['tocos']:
    try:
        tabela_tocos['pos'].append(int(linha.find('td', {'class': 'headcol-2'}).text))
        tabela_tocos['jogador'].append(linha.find('td', {'class': 'headcol'}).text)
        tabela_tocos['equipe'].append(linha.find_all('a')[1].text)
        tabela_tocos['jo'].append(int(linha.find_all('td')[3].text))
        tabela_tocos['min'].append(float(linha.find_all('td')[4].text))
        tabela_tocos['to'].append(float(linha.find_all('td')[5].text))
        tabela_tocos['fc'].append(float(linha.find_all('td')[6].text))
        tabela_tocos['t_fc'].append(float(linha.find_all('td')[7].text))
    except:
        pass

tabela_tocos_df = pd.DataFrame(tabela_tocos)

# %% começa a construção da tabela de Erros
# cria dicionário para armazenar a tabela
categorias_erros = ['pos', 'jogador', 'equipe',
                    'jo', 'min', 'et',
                    'vi', 'er']
matriz_vazia_erros = [[], [], [], 
                      [], [], [],
                      [], []]
tabela_erros = dict(zip(categorias_erros, matriz_vazia_erros))

# preenche tabela_erros
for linha in html_linhas['erros']:
    try:
        tabela_erros['pos'].append(int(linha.find('td', {'class': 'headcol-2'}).text))
        tabela_erros['jogador'].append(linha.find('td', {'class': 'headcol'}).text)
        tabela_erros['equipe'].append(linha.find_all('a')[1].text)
        tabela_erros['jo'].append(int(linha.find_all('td')[3].text))
        tabela_erros['min'].append(float(linha.find_all('td')[4].text))
        tabela_erros['et'].append(float(linha.find_all('td')[5].text))
        tabela_erros['vi'].append(float(linha.find_all('td')[6].text))
        tabela_erros['er'].append(float(linha.find_all('td')[7].text))
    except:
        pass

tabela_erros_df = pd.DataFrame(tabela_erros)

# %% começa a construção da tabela de Eficiência
# cria dicionário para armazenar a tabela
categorias_eficiencia = ['pos', 'jogador', 'equipe',
                         'jo', 'min', 'ef',
                         'pts', 'rt', 'as',
                         'br', 'to', 'er']
matriz_vazia_eficiencia = [[], [], [], 
                           [], [], [],
                           [], [], [],
                           [], [], []]
tabela_eficiencia = dict(zip(categorias_eficiencia, matriz_vazia_eficiencia))

# preenche tabela_eficiencia
for linha in html_linhas['eficiencia']:
    try:
        tabela_eficiencia['pos'].append(int(linha.find('td', {'class': 'headcol-2'}).text))
        tabela_eficiencia['jogador'].append(linha.find('td', {'class': 'headcol'}).text)
        tabela_eficiencia['equipe'].append(linha.find_all('a')[1].text)
        tabela_eficiencia['jo'].append(int(linha.find_all('td')[3].text))
        tabela_eficiencia['min'].append(float(linha.find_all('td')[4].text))
        tabela_eficiencia['ef'].append(float(linha.find_all('td')[5].text))
        tabela_eficiencia['pts'].append(float(linha.find_all('td')[6].text))
        tabela_eficiencia['rt'].append(float(linha.find_all('td')[7].text))
        tabela_eficiencia['as'].append(float(linha.find_all('td')[8].text))
        tabela_eficiencia['br'].append(float(linha.find_all('td')[9].text))
        tabela_eficiencia['to'].append(float(linha.find_all('td')[10].text))
        tabela_eficiencia['er'].append(float(linha.find_all('td')[11].text))
    except:
        pass

tabela_eficiencia_df = pd.DataFrame(tabela_eficiencia)

# %% começa a construção da tabela de Duplos Duplos
# cria dicionário para armazenar a tabela
categorias_duplos_duplos = ['pos', 'jogador', 'equipe',
                            'jo', 'min', 'ef',
                            'pts', 'rt', 'as',
                            'br', 'to', 'dd',
                            'td']
matriz_vazia_duplos_duplos = [[], [], [], 
                              [], [], [],
                              [], [], [],
                              [], [], [],
                              []]
tabela_duplos_duplos = dict(zip(categorias_duplos_duplos, matriz_vazia_duplos_duplos))

# preenche tabela_duplos_duplos
for linha in html_linhas['duplos-duplos']:
    try:
        tabela_duplos_duplos['pos'].append(int(linha.find('td', {'class': 'headcol-2'}).text))
        tabela_duplos_duplos['jogador'].append(linha.find('td', {'class': 'headcol'}).text)
        tabela_duplos_duplos['equipe'].append(linha.find_all('a')[1].text)
        tabela_duplos_duplos['jo'].append(int(linha.find_all('td')[3].text))
        tabela_duplos_duplos['min'].append(float(linha.find_all('td')[4].text))
        tabela_duplos_duplos['ef'].append(float(linha.find_all('td')[5].text))
        tabela_duplos_duplos['pts'].append(float(linha.find_all('td')[6].text))
        tabela_duplos_duplos['rt'].append(float(linha.find_all('td')[7].text))
        tabela_duplos_duplos['as'].append(float(linha.find_all('td')[8].text))
        tabela_duplos_duplos['br'].append(float(linha.find_all('td')[9].text))
        tabela_duplos_duplos['to'].append(float(linha.find_all('td')[10].text))
        tabela_duplos_duplos['dd'].append(float(linha.find_all('td')[11].text))
        tabela_duplos_duplos['td'].append(float(linha.find_all('td')[12].text))
    except:
        pass

tabela_duplos_duplos_df = pd.DataFrame(tabela_duplos_duplos)

# %% transforma DataFrames em csv
tabela_pontos_df.to_csv('output/pontos.csv', index=False)
tabela_rebotes_df.to_csv('output/rebotes.csv', index=False)
tabela_assistencias_df.to_csv('output/assistencias.csv', index=False)
tabela_arremessos_df.to_csv('output/arremessos.csv', index=False)
tabela_bolas_recuperadas_df.to_csv('output/bolas_recuperadas.csv', index=False)
tabela_tocos_df.to_csv('output/tocos.csv', index=False)
tabela_erros_df.to_csv('output/erros.csv', index=False)
tabela_eficiencia_df.to_csv('output/eficiencia.csv', index=False)
tabela_duplos_duplos_df.to_csv('output/duplos_duplos.csv', index=False)
