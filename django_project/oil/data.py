"""
This is data.py, retrieving raw data and process them for running views.py.

Student: Alyssa Nuanxin Jin
Semester: Fall 2023
"""

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
PRODUCT = {
    'Brent': 'EPCBRENT',
    'WTI': 'EPCWTI',
    'Propane': 'EPLLPA',
    'Gasoline': 'EPMRU',
    'Diesel': 'EPD2DXL0',
    'Heating Oil': 'EPD2F',
    }
PRICE_FREQUENCY = 'daily'
PRICE_STARTING_DATE = '2015-01-01'
PRICE_ENDING_DATE = str(datetime.date.today())
DATE_FORMAT = r'(\d{4})-(\d{2})-(\d{2})'
LANGUAGE = 'en'
SORT_BY = 'popularity'
NEWS_STARTING_DATE = datetime.date.today() - datetime.timedelta(days=2)
NEWS_ENDING_DATE = datetime.date.today() - datetime.timedelta(days=1)


def fetch_api_data(endpoint: str, params: dict) -> dict:
    """
    Fetch api data from websites.

    :param endpoint: endpoint of websites
    :param params: parameters used for fetching data
    :return: API data
    """
    return requests.get(endpoint, params).json()


def get_news_params(product_name) -> dict:
    """
    Return oil parameters for fetching news data from NEWS API.

    :param product_name: product name used for searching news
    :return: news parameters
    """
    return {
        'apiKey': NEWS_API_KEY,
        'qInTitle': product_name,
        'from': NEWS_STARTING_DATE,
        'to': NEWS_ENDING_DATE,
        'language': LANGUAGE,
        'sortBy': SORT_BY
    }


def get_oil_params(start_date: str = PRICE_STARTING_DATE,
                   end_date: str = PRICE_ENDING_DATE,
                   product_name: str = 'Brent') -> dict:
    """
    Return oil parameters for fetching oil data from EIA.

    :param product_name: product name
    :param start_date: starting date
    :param end_date: ending date
    :return: EIA oil parameters
    """
    product_id = choose_product(product_name)
    return {
        'api_key': EIA_API_KEY,
        'frequency': PRICE_FREQUENCY,
        'data[0]': 'value',
        'facets[product][]': product_id,
        'start': format_date(start_date, start=True),
        'end': format_date(end_date, start=False),
        'sort[0][column]': 'period',
        'sort[0][direction]': 'asc',
        'offset': 0,
        'length': 5000
    }


def clean_news(data: dict) -> list:
    """
    Clean latest oil from oil api.

    :param data: news data for cleaning
    :return: titles, description and dates.
    """
    return data['articles']


def clean_oil_data(data: dict) -> dict:
    """
    Clean oil data from EIA website.

    :param data: oil data
    :return: oil data
    """
    return data['response']['data']


def is_date(date: str, fuzzy=False) -> bool:
    """
    Check if the string is a date.
    If yes, return true
    If no, return false

    :param fuzzy: if is a fuzzy date
    :param date: inputted string
    :return: bool
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
    """
    if is_date(date) and re.match(DATE_FORMAT, date):
        return date
    elif start:
        return PRICE_STARTING_DATE
    elif not start:
        return PRICE_ENDING_DATE


def choose_product(product_name: str = 'Brent') -> str:
    """
    Users select one product. Returns its product code that can be read by EIA.
    :param product_name: product name
    :return: product code
    """
    return PRODUCT[product_name]


def process_oil_data(data) -> list:
    """
    get oil prices and related dates from get_oil_data.
    :param data: data for processing

    :return: list(price, date)
    """
    value = data
    price = []
    date = []
    for v in value:
        price.append(v['value'])
        date.append(v['period'])
    return [price, date]


def get_product_unit(product_name: str = 'Brent') -> str:
    """
    get the oil product's unit

    :param product_name: product name
    :return: its unit
    """
    if product_name == 'Brent' or product_name == 'WTI':
        return '$/BBL'
    else:
        return '$/GAL'


def draw_graph(data: dict, product_name: str = 'Brent'):
    """
    Draw a graph according to the oil price.
    :param data: data for the graph
    :param product_name: product name

    :return: None
    """
    # x_data is date value
    x_value = process_oil_data(data=data)[1]
    x_data = np.array(x_value)
    # y_data is price value
    y_value = process_oil_data(data=data)[0]
    y_data = np.array(y_value)
    trace = go.Scatter(x=x_data, y=y_data, mode='lines', name='lines')
    # Set layout
    layout = dict(
        title={
            'text': f'{product_name} Price',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
            },
        xaxis_title='Period',
        yaxis_title=get_product_unit(product_name),
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
    # Get the figure
    fig = go.Figure(data=[trace], layout=layout)
    return fig


def process_news(data: dict) -> tuple or str:
    """
    Process news from fetch_news function.
    if the product has news, return (titles, descriptions, and dates) of the top 3 news.
    If not, return 'No news'

    :param data: data for processing
    :return: ([Top_1 titles, Top_2 titles, ...], [Top_1 descriptions, ...], [Top_1 dates,...]) or 'No news'
    """
    # Get a list of news info
    news = clean_news(data)
    # Initialize a article list, a title list, a date list and a url list.
    three_articles = []
    three_articles_title = []
    three_articles_date = []
    three_articles_url = []
    try:
        # Choose the top 3 popular articles and their related infos into lists
        for article_num in range(3):
            articles = news[article_num]['description']
            titles = news[article_num]['title']
            dates = f"{news[article_num]['publishedAt']}"
            urls = news[article_num]['url']
            # Store descriptions of the Top 3 news into three_articles
            three_articles.append(articles)
            # Store titles of the Top 3 news into three_articles_titles
            three_articles_title.append(titles)
            # Store dates pf the Top 3 news into three_articles_date
            three_articles_date.append(dates)
            # Store urls of the Top 3 news into three_articles_url
            three_articles_url.append(urls)
        return three_articles_title, three_articles, three_articles_date, three_articles_url
    # If there is no news related to the product, return No news.
    except IndexError:
        return 'No news'
