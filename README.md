# FIFA/Coca-Cola World Ranking
Parsing the table FIFA World Ranking from fifa.com to csv file. Data is available from 2007.

Last rank updates in Google sheets [here](https://docs.google.com/spreadsheets/d/1MdviCBLSXoXJHP9RyiU1mlbUZMp9TpUNhfqbMoHob-A/).

## Data
##### Base table "fifa_ranking-LASTDATE"
- **id** — counrty id
- **country_full** — country full name
- **country_abrv** — country abbreviation
- **rank** — current country rank
- **total_points** — current total points
- **previous_points** — total points in last rating
- **rank_change** — how rank has changed since the last publication
- **confederation** — FIFA confederations
- **rank_date** — date of rating calculation

##### Advanced custom table "fifa_ranking_plus-LASTDATE"
- **delta_points** — delta between `total_points` and `previous_points`
- **points_mean_(alltime/4year/1year)** — average points for: all time, last 4 year, last year
- **delta_points_mean_(alltime/4year/1year)** — average delta points for: all time, last 4 year, last year
- **delta_points_sum_(alltime/4year/1year)** — amount of points delta for: all time, last 4 year, last year
- **rank_change_mean_(alltime/4year/1year)** — average rank change for: all time, last 4 year, last year
- **rank_change_sum_(alltime/4year/1year)** — sum of rank changes for: all time, last 4 year, last year
- **rank_mean_(alltime/4year/1year)** — average rank for: all time, last 4 year, last year
- **best_rank_last_4y** — best rank in the last 4 years
- **worst_rank_last_4y** — worst rank in the last 4 years
- **delta_ranks_last_4y** — delta between best rank and worst rank in the last 4 years


## How to use
1. For parsing last update:

    Download and run `scraper.py`
    
    Example:
    ```commandline
    F:\PATH_TO\fifa-ranking-database>python scraper.py  # or python3
    First date: 2007-06-13 00:00:00
    Last date: 2019-06-14 00:00:00
    Start parsing..  0:00:00
    Complite 25/139 dates
    Complite 50/139 dates
    Complite 75/139 dates
    Complite 100/139 dates
    Complite 125/139 dates
    Parsing complite. Time 0:13:54.575583
    File fifa_ranking-2019-06-14 was saved to F:\CURRENTLY_PATH
    
          id rank country_full country_abrv total_points previous_points rank_change confederation  rank_date
    0  43935    1      Belgium          BEL         1746            1737           0          UEFA 2019-06-14
    1  43946    2       France          FRA         1718            1734           0          UEFA 2019-06-14
    2  43924    3       Brazil          BRA         1681            1676           0      CONMEBOL 2019-06-14
    3  43942    4      England          ENG         1652            1647           0          UEFA 2019-06-14
    4  43963    5     Portugal          POR         1631            1607           2          UEFA 2019-06-14

    ```
2. For rework:

    Use Jupyter notebook from from repository or code from 'scraper.py'

3. For analysis:

    - Use csv files from repository or [table from google sheet](https://docs.google.com/spreadsheets/d/1MdviCBLSXoXJHP9RyiU1mlbUZMp9TpUNhfqbMoHob-A/)
    - Use csv files as a DataFrame
    Example for python & pandas:
    ```python
    import pandas as pd
    
    
    df = pd.read_csv('PATH_TO_FILE/fifa_ranking-2019-06-14.csv')
    ```
## Requirements
Python 3.7 or newest and packages from requirements.txt
```commandline
pip install -r requirements.txt  # or pip3
```

## Target
This project was created for easy analysis of the national teams FIFA ranks.