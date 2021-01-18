# %% import libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os


# %% function that scrapes table for the given URL and returns it as a DataFrame
def scrape_table(base_url, tag):
    url = f'{base_url}{tag}'
    scraped_data = pd.read_html(url)
    data = scraped_data[0]

    return data


# %% function that scrapes a player's listed position and returns a
# tuple with player's name and position (player, position)
def scrape_players_positions(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    position = soup.select_one('td:last-child').text

    return position

# %% list of tags and urls to loop through
base_urls = [
    'https://lnb.com.br/nbb/estatisticas/'
]

tags = [
    'cestinhas',
    'rebotes',
    'assistencias',
    'arremessos',
    'bolas-recuperadas',
    'tocos',
    'erros',
    'eficiencia',
    'duplos-duplos',   
]


# %% creates DataFrames for players positions
# gets soup object from NBB's main stats page
positions_url = base_urls[0]
r = requests.get(positions_url)
soup = BeautifulSoup(r.content, 'html.parser')

# gets list of players' pages URLs
players_urls_elements = soup.select('tbody tr td.headcol.no_sorter a')
players_names = [i.text for i in players_urls_elements]
players_urls = [i['href'] for i in players_urls_elements]

# creates list of tuples of players' names and positions
players_positions = []
for i in players_urls:
    players_positions.append(
        scrape_players_positions(i)
    )

players_names_and_positions = {
    'Jogador': players_names,
    'Posicao': players_positions
}

# creates players' positions DataFrame
df_positions = pd.DataFrame(players_names_and_positions)


# %% creates list of scraped stats tables DataFrames 
dfs = [
    scrape_table(base_url, tag) for base_url in base_urls for tag in tags
]

# %% outputs all DataFrames to CSV's
# outputs stats tables DataFrames based on tags names
for i in range(len(dfs)):
    dfs[i].to_csv(
        f'{os.path.dirname(__file__)}{os.sep}output{os.sep}{tags[i]}.csv',
        index=False
        )

# outputs positions DataFrame
df_positions.to_csv(
    f'{os.path.dirname(__file__)}{os.sep}output{os.sep}posicoes.csv',
    index=False
)

# %%
