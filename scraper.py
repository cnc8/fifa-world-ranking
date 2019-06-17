import datetime
import os
import requests as r
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup


def get_page_soup(page_id, url):
    try:
        page_source = r.get(f'{url}/{page_id}/')
        page_source.raise_for_status()
        page_source.encoding = 'utf8'
        soup = BeautifulSoup(page_source.content, 'html.parser')
    except r.exceptions.HTTPError:
        exit('ERROR: URL page "FIFA World Ranking" has been changed. Create issue in the project repository.')
    except r.exceptions.ConnectionError:
        exit('ERROR: Connection error. Check the internet and try again')

    return soup


def get_date_ids_soup(soup):
    try:
        date_ids = soup.find('ul', {'class': 'fi-ranking-schedule__nav'}).find_all('li')
    except AttributeError:
        return ['AttributeError']

    return date_ids


def get_date_ids_df(soup):
    df = pd.DataFrame(columns=['date', 'date_id'])

    for date_data in soup:
        date = pd.to_datetime(
            date_data.text.strip(),
            format='%d %B %Y'
        )

        df = df.append({
            'date': date,
            'date_id': date_data['data-value']
        }, ignore_index=True)

    return df


def get_teams_data(soup):
    try:
        html_data = soup.find('tbody').find_all('tr')
    except AttributeError:
        return ['AttributeError']

    return html_data


def parse_team_data(soup):
    try:
        return {
            'id': int(soup['data-team-id']),
            'country_full': soup.find('span', {'class': 'fi-t__nText'}).text,
            'country_abrv': soup.find('span', {'class': 'fi-t__nTri'}).text,
            'rank': int(soup.find('td', {'class': 'fi-table__rank'}).text),
            'total_points': int(soup.find('td', {'class': 'fi-table__points'}).text),
            'previous_points': int(soup.find('td', {'class': 'fi-table__prevpoints'}).text),
            'rank_change': int(soup.find('td', {'class': 'fi-table__rankingmovement'}).text),
            'confederation': soup.find('td', {'class': 'fi-table__confederation'}).text.strip('#'),
            'rank_date': date
        }
    except AttributeError:
        return {'id': 'AttributeError'}


def save_table(dataframe):
    last_date = str(dataframe.rank_date.max())[:10]   # cut last date to format "XXXX-XX-XX"
    file_name = f'fifa_ranking-{last_date}'
    dataframe.to_csv(
        f'{file_name}.csv',
        index=False,
        encoding='utf-8'
    )
    print(f'File {file_name} was saved to {os.getcwd()}\n')


if __name__ == '__main__':
    date_id = 'id8198'  # first date 13 June 2007
    fifa_url = 'https://www.fifa.com/fifa-world-ranking/ranking-table/men/rank'
    attribute_error_msg = 'ERROR: The fifa.com site has changed the code. Create issue in the project repository.'
    page_soup = get_page_soup(date_id, fifa_url)
    date_ids_soup = get_date_ids_soup(page_soup)

    assert date_ids_soup[0] != 'AttributeError', attribute_error_msg

    date_ids_df = get_date_ids_df(date_ids_soup)
    print(f'First date: {date_ids_df.date.min()}\n'
          f'Last date: {date_ids_df.date.max()}')

    fifa_ranking = pd.DataFrame(columns=[
        'id', 'rank', 'country_full', 'country_abrv',
        'total_points', 'previous_points', 'rank_change',
        'confederation', 'rank_date'
    ])
    start_time = datetime.datetime.now()
    print("Start parsing.. ", datetime.datetime.now() - start_time)

    for i, (date, date_id) in enumerate(date_ids_df.values, start=1):
        page_soup = get_page_soup(date_id, fifa_url)
        teams_data = get_teams_data(page_soup)
        assert teams_data[0] != 'AttributeError', attribute_error_msg

        for team_data_html in teams_data:
            team_data = parse_team_data(team_data_html)
            assert team_data['id'] != 'AttributeError', attribute_error_msg

            fifa_ranking = fifa_ranking.append(team_data, ignore_index=True)

        if i % 25 == 0:
            print(f'Complite {i}/{date_ids_df.shape[0]} dates')

    else:
        print(f'Parsing complite. Time {datetime.datetime.now()-start_time}')
        save_table(fifa_ranking)

    print(fifa_ranking.head())
