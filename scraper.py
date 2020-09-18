import datetime
import asyncio
import aiohttp
import logging
import os
import requests as r
import pandas as pd
from bs4 import BeautifulSoup
from bs4.element import SoupStrainer


logger: logging.Logger = logging.getLogger('log')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


FIRST_DATE = 'id1'  # first date 31 12 1992
FIFA_URL = 'https://www.fifa.com/fifa-world-ranking/ranking-table/men/rank'


def get_dates_html():
    page_source = r.get(f'{FIFA_URL}/{FIRST_DATE}/')
    page_source.raise_for_status()
    dates = BeautifulSoup(page_source.text,
                          'html.parser',
                          parse_only=SoupStrainer('li', attrs={'class': 'fi-ranking-schedule__nav__item'}))
    return dates


def create_dates_dataset(html_dates):
    date_ids = [li['data-value'] for li in html_dates]
    dates = [li.text.strip() for li in html_dates]
    dataset = pd.DataFrame(data={'date': dates, 'date_id': date_ids})

    # convert 'date' from str to datetime and sorting "old -> new"
    dataset['date'] = pd.to_datetime(dataset['date'], format='%d %B %Y')
    dataset.sort_values('date', ignore_index=True, inplace=True)
    assert dataset.date.min() == dataset.iloc[0].date, \
        "Incorrect dataset sorting"

    return dataset


async def get_rank_page(date_id, session):
    async with session.get(f'{FIFA_URL}/{date_id}/') as response:
        page = await response.text()
        if response.status == 200:
            return {'page': page, 'id': date_id}
        else:
            logger.error(f'Parse error, page: {response.url}')
            return False


def scrapy_rank_table(page, date):
    rows = BeautifulSoup(page,
                         'html.parser',
                         parse_only=SoupStrainer('tbody')).find_all('tr')
    table = []
    for row in rows:
        table.append({
            'id': int(row['data-team-id']),
            'country_full': row.find('span', {'class': 'fi-t__nText'}).text,
            'country_abrv': row.find('span', {'class': 'fi-t__nTri'}).text,
            'rank': int(row.find('td', {'class': 'fi-table__rank'}).text),
            'total_points': int(row.find('td', {'class': 'fi-table__points'}).text),
            'previous_points': int(row.find('td', {'class': 'fi-table__prevpoints'}).text or 0),
            'rank_change': int(row.find('td', {'class': 'fi-table__rankingmovement'}).text.replace('-', '0')),
            'confederation': row.find('td', {'class': 'fi-table__confederation'}).text.strip('#'),
            'rank_date': date
        })
    return table


async def parse_ranks(pages_df):
    fifa_ranking = pd.DataFrame(columns=[
        'id', 'rank', 'country_full', 'country_abrv',
        'total_points', 'previous_points', 'rank_change',
        'confederation', 'rank_date'
    ])

    start_time = datetime.datetime.now()
    logger.info(f"Start parsing..")

    task_parse = []
    async with aiohttp.ClientSession() as session:
        for date_id in pages_df.date_id.to_list():
            task_parse += [asyncio.create_task(get_rank_page(date_id, session))]

        for task in asyncio.as_completed(task_parse):
            page = await task
            if not task:
                continue
            date_ranking = scrapy_rank_table(page['page'],
                                             pages_df[pages_df.date_id == page['id']].date.iloc[0])
            fifa_ranking = fifa_ranking.append(date_ranking, ignore_index=True)

            if fifa_ranking.rank_date.nunique() % 50 == 0:
                logger.debug(f'Complite {fifa_ranking.rank_date.nunique()}/{pages_df.shape[0]} dates')

    fifa_ranking.sort_values('rank_date', ignore_index=True, inplace=True)
    logger.info(f'Parsing complite. Time {datetime.datetime.now()-start_time}')
    return fifa_ranking


def data_correction(df):
    """ Handmade """
    # Lebanon has two abbreviations
    df.replace({'country_abrv': 'LIB'}, 'LBN', inplace=True)
    # Montenegro duplicates
    df.drop(df[df.id == 1903356].index, inplace=True)
    # North Macedonia has two full names
    df.replace({'country_full': 'FYR Macedonia'}, 'North Macedonia', inplace=True)
    # Cabo Verde has two full names
    df.replace({'country_full': 'Cape Verde Islands'}, 'Cabo Verde', inplace=True)
    # Saint Vincent and the Grenadines have two full names
    df.replace({'country_full': 'St. Vincent and the Grenadines'}, 'St. Vincent / Grenadines', inplace=True)
    # Swaziland has two full names
    df.replace({'country_full': 'Eswatini'}, 'Swaziland', inplace=True)
    # Curacao transform to Curaçao (with 'ç')
    df.replace({'country_full': 'Curacao'}, 'Curaçao', inplace=True)
    # São Tomé and Príncipe have three full names
    df.replace({'country_full': ['Sao Tome e Principe', 'São Tomé e Príncipe']},
               'São Tomé and Príncipe', inplace=True)
    return df


def check_data(ranks_df, dates_df):
    if ranks_df.rank_date.nunique() != dates_df.date.nunique():
        logger.warning("Warning! Numbers of rank dates don't match")
    if ranks_df.country_full.nunique() != ranks_df.country_abrv.nunique():
        logger.warning("Warning! Number of names and abbreviations does not match")
    if ranks_df.country_full.nunique() != ranks_df.id.nunique():
        logger.warning("Warning! Number of names and IDs does not match")


def save_as_csv(df):
    file_name = f'fifa_ranking-{df.rank_date.max().date()}.csv'
    df.to_csv(file_name, index=False, encoding='utf-8')

    print(f'Dataset {file_name} was saved to {os.getcwd()}\n')


async def main():
    dates_from_page = get_dates_html()
    dates_dataset = create_dates_dataset(dates_from_page)

    assert len(dates_from_page) == dates_dataset.shape[0], \
        "Number of dates in html and dataset don't match"

    logger.info(f'Last date: {dates_dataset.date.max().date()}')

    fifa_ranking_df = await parse_ranks(dates_dataset)
    fifa_ranking_df = data_correction(fifa_ranking_df)
    check_data(fifa_ranking_df, dates_dataset)
    save_as_csv(fifa_ranking_df)

    print(fifa_ranking_df.head())


if __name__ == '__main__':
    asyncio.run(main())
