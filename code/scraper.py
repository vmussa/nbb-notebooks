import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm

BASE_URLS = [
    'https://lnb.com.br/nbb/estatisticas/'
]

TAGS = [
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

OUTPUT_PATH = (
    f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}{os.sep}"
    f"data{os.sep}scraped{os.sep}"
)


def get_soup(url):
    """Gets soup object for given URL."""
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def get_stats_table(base_url, tag):
    """Scrapes the stats table for the given URL an returns it as a 
    DataFrame."""
    url = f'{base_url}{tag}'
    data = pd.read_html(url)[0]
    return data


def get_player_position(url):
    """Scrapes player's position data from given URL and return a tuple
     with their position and their team. Returns data as a string."""
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    position = soup.select_one('td:last-child').text.strip()
    return position


def get_players_urls_names_teams(soup):
    """Scrapes players pages' URLs plus players' names and teams data.
    Returns scraped data as tuple."""
    urls_tags = soup.select('tbody tr td.headcol.no_sorter a')
    urls = [i['href'] for i in urls_tags]
    names = [i.text.strip() for i in urls_tags]
    teams_tags = soup.select('tbody tr td:nth-of-type(3)')
    teams = [i.text.strip() for i in teams_tags]
    return urls, names, teams


def get_players_positions_df(urls, names, teams):
    """Returns a DataFrame with players data."""
    positions = []
    for url in tqdm(urls):
        positions.append(get_player_position(url))

    players_names_and_positions = {
        'Jogador': names,
        'Posicao': positions,
        'Equipe': teams
    }

    df = pd.DataFrame(players_names_and_positions)
    return df


def get_stats_dfs(base_urls, tags):
    """Returns a list of DataFrames containing each stats table."""
    dfs = [
        get_stats_table(base_url, tag) for base_url in base_urls for tag in tags
    ]
    return dfs


def main():
    """Main function."""
    # scrape players' data
    soup = get_soup(BASE_URLS[0] + TAGS[0])
    urls, names, teams = get_players_urls_names_teams(soup)

    # get dfs
    positions_df = get_players_positions_df(urls, names, teams)   
    stats_dfs = get_stats_dfs(BASE_URLS, TAGS)

    # outputs stats tables DataFrames based on tags names
    for i, _ in enumerate(stats_dfs):
        stats_dfs[i].to_csv(
            f'{OUTPUT_PATH}{TAGS[i]}.csv',
            index=False
        )

    # outputs positions DataFrame
    positions_df.to_csv(
        f'{OUTPUT_PATH}posicoes.csv',
        index=False
    )


if __name__ == "__main__":
    main()
