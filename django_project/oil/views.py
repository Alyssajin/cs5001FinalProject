"""
This is views.py, calling functions from data.py.
It retrieves processed data and stores them into 'context' so that the home.html can utilise them.
It allows to save users' inputting values and call back them when needed.

Student: Alyssa Nuanxin Jin
Semester: Fall 2023
"""

from django.shortcuts import render
from . import data as dt
from . import data


def home(request):
    """
    Handle the traffic from the home page of "oil".
    Take in request argument. Load templates.
    Return what the users would see when they're sent to this route.
    """

    def fetch_form_value() -> tuple:
        """
        Get search range from users' input.

        :return: (starting_date, ending_date, user_input)
        """
        starting_date = request.POST.get('starting_date')
        ending_date = request.POST.get('ending_date')
        product_name = request.POST.get('product_name')
        return starting_date, ending_date, product_name

    def fetch_news_data(data: dict) -> tuple or str:
        """
        fetch news by utilise get_new functions.

        :param data: data for fetching news
        :return: (Top 3 articles_title, Top 3 articles, Top 3 articles date)
        """
        return dt.process_news(data=data)

    def get_posts(data:dict) -> list:
        """
        Parse news from fetch_news_data. Store processed data into posts.

        :param data: data for posting
        :return : lists of posts.
        """
        news = fetch_news_data(data=data)
        try:
            posts = [
                {
                    'title': news[0][0],
                    'content': news[1][0],
                    'date': news[2][0],
                    'url': news[3][0]
                },
                {
                    'title': news[0][1],
                    'content': news[1][1],
                    'date': news[2][1],
                    'url': news[3][1]
                },
                {
                    'title': news[0][2],
                    'content': news[1][2],
                    'date': news[2][2],
                    'url': news[3][2]
                }
            ]
        # If there is no new, return ""
        except IndexError:
            posts = ""
        return posts
    # Get users' input value from fetch_form_value
    start_date = fetch_form_value()[0]
    end_date = fetch_form_value()[1]
    product_name = fetch_form_value()[2]
    # Give a default value for product_name
    if product_name is None:
        product_name = 'Brent'
    # Set oil and news parameters for fetching data
    oil_params = dt.get_oil_params(start_date=start_date, end_date=end_date, product_name=product_name)
    news_params = dt.get_news_params(product_name=product_name)
    # Retrieve oil and news data
    oil_data = dt.fetch_api_data(endpoint=dt.EIA_ENDPOINT, params=oil_params)['response']['data']
    news_data = dt.fetch_api_data(endpoint=dt.NEWS_ENDPOINT, params=news_params)
    # Use draw_graph function to show a chart
    chart = data.draw_graph(data=oil_data, product_name=product_name).to_html()
    # Show context
    context = {
        'posts': get_posts(data=news_data),
        'graph': chart,
        'user_input': product_name
    }
    return render(request, 'oil/home.html', context)
