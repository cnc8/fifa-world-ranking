# FIFA/Coca-Cola World Ranking
Parsing the table FIFA World Ranking from fifa.com to csv file. Data is available from 1992.

Last rank updates on Kaggle [here](https://www.kaggle.com/cashncarry/fifaworldranking).

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


## How to use
1. For parsing last update:

    Download and run `scraper.py`
    
    Example:
    ```commandline
    F:\PATH_TO\fifa-ranking-database>python scraper.py  # or python3
    Last date: 2020-09-17
    Start parsing..
    Complite 50/306 dates
    Complite 100/306 dates
    Complite 150/306 dates
    Complite 200/306 dates
    Complite 250/306 dates
    Complite 300/306 dates
    Parsing complite. Time 0:03:10.035290
    Dataset fifa_ranking-2020-09-17.csv was saved to PATH_TO_PROJECT
    
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

    - Use csv files from repository or [Kaggle dataset](https://www.kaggle.com/cashncarry/fifaworldranking)
    - Use csv files as a DataFrame
    Example for python & pandas:
    ```python
    import pandas as pd
    
    
    df = pd.read_csv('PATH_TO_FILE/fifa_ranking-2020-09-17.csv')
    ```
## Requirements
Python 3.7 or newest and packages from requirements.txt
```commandline
pip install -r requirements.txt  # or pip3
```

## Target
This project was created for easy analysis of the national teams FIFA ranks.