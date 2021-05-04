"""Code for the inital data cleaning of NBB website's scraped data."""
import pandas as pd
import numpy as np
import os
import re

INPUT_PATH = (
    f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}{os.sep}"
    f"data{os.sep}scraped{os.sep}"
)
    
OUTPUT_PATH = (
    f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}{os.sep}"
    f"data{os.sep}cleaned{os.sep}"
)


def get_dfs(path):
    """Get scraped data and returns it as a list of DataFrames."""
    filenames = os.listdir(path)
    dfs = []
    for filename in filenames:
        if filename.endswith(".csv") and filename != "posicoes.csv":
            df = pd.read_csv(path+filename)
            dfs.append(df)
    return dfs


def remove_ranks(dfs):
    """Removes ranks' column."""
    for i, _ in enumerate(dfs):
        dfs[i] = dfs[i].drop('Pos.', axis=1)


def merge_dfs(dfs):
    """Merge all DataFrames in dfs."""
    for i, _ in enumerate(dfs):
        try:
            dfs[i+1] = pd.merge(dfs[i], dfs[i+1])
        except IndexError:
            pass


def add_shirts_numbers(df):
    """Add shirts numbers' column."""
    shirts_numbers = df['Jogador'].str.extract(r'(?P<camisa>#\d\d?)')
    df['camisa'] = shirts_numbers['camisa']


def clean_players_names(df):
    """Clean players' names."""
    df['Jogador'] = df['Jogador'].str.replace(
        re.compile(r"\s#\d\d?"), ''
    )


def main():
    """Main function."""
    dfs = get_dfs(path=INPUT_PATH)
    remove_ranks(dfs)
    merge_dfs(dfs)
    all_data = dfs[-1]
    positions_df = pd.read_csv(INPUT_PATH+"posicoes.csv")
    all_data = pd.merge(
        all_data, positions_df, how='left', on=['Jogador', 'Equipe']
    )
    add_shirts_numbers(all_data)
    clean_players_names(all_data)

    # export data
    all_data.to_csv(OUTPUT_PATH+'/nbb_estatisticas.csv', index=False)
    all_data.to_excel(OUTPUT_PATH+'/nbb_estatisticas.xlsx', index=False)


if __name__ == "__main__":
    main()
