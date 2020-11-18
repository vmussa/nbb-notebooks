# %% Código para a limpeza inicial dos dados raspados do site do NBB

# %% configurações iniciais
# importa as bibliotecas
import pandas as pd
import numpy as np
import os
import re

# importa os dados
path = "../scraper/output/"
filenames = os.listdir(path)
dfs = []
for filename in filenames:
    if filename.endswith(".csv"):
        df = pd.read_csv(path+filename)
        dfs.append(df)

# %% unifica os DataFrames
# remove coluna pos (info redundante)
for i in range(len(dfs)):
    dfs[i] = dfs[i].drop('pos', axis=1)

# loop com merge em cada df da lista: último df é a tabela unfiicada
for i in range(len(dfs)):
    try:
        dfs[i+1] = pd.merge(dfs[i], dfs[i+1])
    except IndexError:
        pass

all_data = dfs[-1]

# %% separa em duas colunas nomes dos jogadores e números das camisas
# cria coluna nova com o número das camisas
camisas = all_data.jogador.str.extract(r'(?P<camisa>#\d\d?)')
all_data['camisa'] = camisas['camisa']

# remove número das camisas da coluna jogador
all_data.jogador = all_data.jogador.str.replace(
    re.compile(r"\s#\d\d?"),
    ''
    )

# %% altera a ordem das colunas para uma melhor leitura dos dados

# %% verifica inconsistências na entrada de dados
# colunas categóricas

# colunas numéricas

# %% exporta tabela unificada para csv e excel
all_data.to_csv('output/nbb_estatisticas.csv', index=False)
all_data.to_excel('output/nbb_estatisticas.xlsx', index=False)
