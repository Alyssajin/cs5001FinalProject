from django.shortcuts import render
from . import data as dt
from . import data


def home(request):
    """
    Handle the traffic from the home page of "oil".
    Take in request argument. Load templates.
    Return what the users would see when they're sent to this route.
    """
    # Get search range from users' input.
    starting_date = request.POST.get('starting_date')
    ending_date = request.POST.get('ending_date')

    def fetch_data():
        return dt.get_news(api_key=dt.NEWS_API_KEY,
                           company_name=dt.COMPANY_NAME,
                           from_date=dt.NEWS_STARTING_DATE,
                           to_date=dt.NEWS_ENDING_DATE,
                           sort_by=dt.SORT_BY,
                           lang=dt.LANGUAGE)
    # get news from fetch_data function
    posts = [
        {
            'title': fetch_data()[0][0],
            'content': fetch_data()[1][0],
            'date': fetch_data()[2][0]
        },
        {
            'title': fetch_data()[0][1],
            'content': fetch_data()[1][1],
            'date': fetch_data()[2][1]
        },
        {
            'title': fetch_data()[0][2],
            'content': fetch_data()[1][2],
            'date': fetch_data()[2][2]
        }
    ]
    # use draw_graph function to show a chart
    chart = data.draw_graph(start_date=starting_date, end_date=ending_date).to_html()
    context = {
        'posts': posts,
        'graph': chart
    }
    return render(request, 'oil/home.html', context)


def about(request):
    """
    Handle the traffic from the about page of "oil".
    Take in request argument.
    Return what the users would see when they're sent to this route.
    """
    return render(request, 'oil/about.html')
