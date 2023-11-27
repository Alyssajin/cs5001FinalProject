import requests
import datetime
import plotly.graph_objects as go
import numpy as np
import re
from dateutil.parser import parse

EIA_API_KEY = '215LPlEH4HEH9iCacvem0zZlJytc6I6N34HkAVEM'
NEWS_API_KEY = '2d7846b501ec4d0dafa4816805a47174'
EIA_ENDPOINT = 'https://api.eia.gov/v2/petroleum/pri/spt/data'
NEWS_ENDPOINT = 'https://newsapi.org/v2/everything'


PRODUCT = 'EPCBRENT'
PRICE_FREQUENCY = 'daily'
PRICE_STARTING_DATE = '2015-01-01'
PRICE_ENDING_DATE = str(datetime.date.today())
DATE_FORMAT = r'(\d{4})-(\d{2})-(\d{2})'

COMPANY_NAME = 'oil'
LANGUAGE = 'en'
SORT_BY = 'popularity'
NEWS_STARTING_DATE = datetime.date.today() - datetime.timedelta(days=2)
NEWS_ENDING_DATE = datetime.date.today() - datetime.timedelta(days=1)


def is_date(date: str, fuzzy=False) -> bool:
    """
    Check if the string is a date.
    If yes, return true
    If no, return false
    :param fuzzy: if is a fuzzy date
    :param date: inputted string
    :return: bool

    Example:
    >>> is_date('2013/14/21')
    False
    >>> is_date('hap')
    False
    >>> is_date('2023/12/25')
    True
    """
    try:
        parse(str(date), fuzzy=fuzzy)
        return True
    except ValueError:
        return False


def format_date(date: str, start: bool = True) -> str:
    """
    Test if the inputted date is a formatted date. e.g. 1999-01-01
    If yes, return date.
    If no, see if we need a starting date.
    If yes, the default date is the starting date. If no, the default date is the ending date.
    :param start: bool. if we need a starting date
    :param date: str
    :return: formatted date

    Example:
    >>> format_date('2023/2/31')
    '2015-01-01'
    >>> format_date('happy')
    '2015-01-01'
    >>> format_date('2023-01-03')
    '2023-01-03'
    """
    if is_date(date) and re.match(DATE_FORMAT, date):
        return date
    elif start:
        return PRICE_STARTING_DATE
    elif not start:
        return PRICE_ENDING_DATE


def get_oil_data(api_key: str = EIA_API_KEY,
                 start_date: str = PRICE_STARTING_DATE,
                 end_date: str = PRICE_ENDING_DATE) -> list:
    """
    Get oil data from EIA website.
    :param end_date: endint date
    :param start_date: starting date
    :param api_key: EIA API KEY
    :return: oil data
    """
    price_params = {
        'api_key': api_key,
        'frequency': PRICE_FREQUENCY,
        'data[0]': 'value',
        'facets[product][]': PRODUCT,
        'start': format_date(start_date, start=True),
        'end': format_date(end_date, start=False),
        'sort[0][column]': 'period',
        'sort[0][direction]': 'asc',
        'offset': 0,
        'length': 5000
    }

    oil_data_response = requests.get(EIA_ENDPOINT, params=price_params)
    oil_data = oil_data_response.json()['response']['data']
    return oil_data


def get_price_date(start_date: str, end_date: str) -> list:
    """
    get oil prices and related dates from get_oil_data.

    :return: list(price, date)
    """
    value = get_oil_data(EIA_API_KEY, start_date=start_date, end_date=end_date)
    price = []
    date = []
    for v in value:
        price.append(v["value"])
        date.append(v["period"])
    return [price, date]


def draw_graph(start_date: str, end_date: str):
    """
    Draw a graph according to the oil price.
    :return: None
    """
    x_data = np.array(get_price_date(start_date, end_date)[1])
    y_data = np.array(get_price_date(start_date, end_date)[0])
    trace = go.Scatter(x=x_data, y=y_data, mode='lines', name='lines')
    # set layout
    layout = dict(
        title='Brent Price',
        xaxis_title='Period',
        yaxis_title='$/BBL',
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            zeroline=False,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        autosize=False,
        margin=dict(
            autoexpand=False,
            l=100,
            r=20,
            t=110,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )
    # get the figure
    fig = go.Figure(data=[trace], layout=layout)
    return fig


def get_news(api_key: str, company_name: str, from_date: datetime, to_date: datetime, lang: str, sort_by: str) -> tuple:
    """
    Get latest oil from oil api.

    :param api_key: NEWS API KEY
    :param company_name: company name
    :param from_date: starting date
    :param to_date: ending date
    :param lang: language
    :param sort_by: sorted by popularity
    :return: articles
    """
    news_params = {
        "apiKey": api_key,
        "qInTitle": company_name,
        "from": from_date,
        "to": to_date,
        "language": lang,
        "sortBy": sort_by
    }
    # fetch news through NEW API
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    article = news_response.json()["articles"]
    # initialize a article list, a title list and a date list.
    three_articles = []
    three_articles_title = []
    three_articles_date = []
    # choose the most popular articles and related info into lists
    for article_num in range(3):
        articles = article[article_num]['description']
        titles = article[article_num]['title']
        dates = f"\n{article[article_num]['publishedAt']}"
        three_articles.append(articles)
        three_articles_title.append(titles)
        three_articles_date.append(dates)
    return three_articles_title, three_articles, three_articles_date