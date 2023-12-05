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
        user_input = request.POST.get('product_name')
        return starting_date, ending_date, user_input

    def fetch_news_data(product_name: str = 'Brent') -> tuple or str:
        """
        fetch news by utilise get_new functions.
        :param product_name: product name
        :return: (Top 3 articles_title, Top 3 articles, Top 3 articles date)
        """
        return dt.get_news(api_key=dt.NEWS_API_KEY,
                           product_name=product_name,
                           from_date=dt.NEWS_STARTING_DATE,
                           to_date=dt.NEWS_ENDING_DATE,
                           sort_by=dt.SORT_BY,
                           lang=dt.LANGUAGE)

    def get_posts(product_name: str = 'Brent') -> list:
        """
        Parse news from fetch_news_data. Store processed data into posts.

        :param product_name: product name
        :return : lists of posts.
        """
        news = fetch_news_data(product_name)
        try:
            posts = [
                {
                    'title': news[0][0],
                    'content': news[1][0],
                    'date': news[2][0]
                },
                {
                    'title': news[0][1],
                    'content': news[1][1],
                    'date': news[2][1]
                },
                {
                    'title': news[0][2],
                    'content': news[1][2],
                    'date': news[2][2]
                }
            ]
        # if there is no new, return ""
        except IndexError:
            posts = ""
        return posts

    # use draw_graph function to show a chart
    # get value from fetch_form_value, as it returns (start_date, end_date, product_date)
    start_date = fetch_form_value()[0]
    end_date = fetch_form_value()[1]
    product_name = fetch_form_value()[2]
    # give a default value for product_name
    if product_name is None:
        product_name = 'Brent'
    chart = data.draw_graph(start_date=start_date,
                            end_date=end_date,
                            product_name=product_name).to_html()
    context = {
        'posts': get_posts,
        'graph': chart,
        'user_input': product_name
    }
    return render(request, 'oil/home.html', context)
