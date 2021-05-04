"""Código para a limpeza inicial dos dados raspados do site do NBB."""
import pandas as pd
import numpy as np
import os
import re

# importa os dados
path = "../scraper/output/"
filenames = os.listdir(path)
dfs = []
for filename in filenames:
    if filename.endswith(".csv") and filename != "posicoes.csv":
        df = pd.read_csv(path+filename)
        dfs.append(df)

# remove coluna pos (info redundante)
for i, _ in enumerate(dfs):
    dfs[i] = dfs[i].drop('Pos.', axis=1)

# loop com merge em cada df da lista: último df é a tabela unificada
for i, _ in enumerate(dfs):
    try:
        dfs[i+1] = pd.merge(dfs[i], dfs[i+1])
    except IndexError:
        pass

all_data = dfs[-1]

# adiciona posição dos jogadores
positions_df = pd.read_csv(path+"posicoes.csv")
all_data = pd.merge(
    all_data, positions_df, how='left', on=['Jogador', 'Equipe']
    )

# separa em duas colunas nomes dos jogadores e números das camisas
# cria coluna nova com o número das camisas
camisas = all_data['Jogador'].str.extract(r'(?P<camisa>#\d\d?)')
all_data['camisa'] = camisas['camisa']

# remove número das camisas da coluna jogador
all_data['Jogador'] = all_data['Jogador'].str.replace(
    re.compile(r"\s#\d\d?"),
    ''
    )

# altera a ordem das colunas para uma melhor leitura dos dados

# verifica inconsistências na entrada de dados
# colunas categóricas

# colunas numéricas

# exporta tabela unificada para csv e excel
all_data.to_csv('output/nbb_estatisticas.csv', index=False)
all_data.to_excel('output/nbb_estatisticas.xlsx', index=False)
