# Final Project Report

* Student Name: Alyssa Nuanxin Jin
* Github Username: Alyssajin
* Semester: Fall 2023
* Course: CS 5001



## Description 
General overview of the project, what you did, why you did it, etc. 

Purpose:
The purpose of this project is to present Crude Oil prices as a graph and its latest news on one HTML page. Also, this page allows users to search for their preferred date ranges.

Background:


To achieve this goal:
•	I fetch data of {latest news, oil prices} by using APIs from NEWS API website and EIA.
•	I process data by using different functions of {is_date, format_date, get_oil_data, get_price_data, get_news}.
•	I use Plotly to draw a graph for the oil prices.
•	I utilise Django to construct a web page.


## Key Features
Highlight some key features of this project that you want to show off/talk about/focus on. 

## Guide
How do we run your project? What should we do to see it in action? - Note this isn't installing, this is actual use of the project.. If it is a website, you can point towards the gui, use screenshots, etc talking about features. 


## Installation Instructions
If we wanted to run this project locally, what would we need to do?  If we need to get API key's include that information, and also command line startup commands to execute the project. If you have a lot of dependencies, you can also include a requirements.txt file, but make sure to include that we need to run `pip install -r requirements.txt` or something similar.

## Code Review
Go over key aspects of code in this section. Both link to the file, include snippets in this report (make sure to use the [coding blocks](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#code)).  Grading wise, we are looking for that you understand your code and what you did. 
```python
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
```
### Major Challenges
Key aspects could include pieces that your struggled on and/or pieces that you are proud of and want to show off.


## Example Runs
Explain how you documented running the project, and what we need to look for in your repository (text output from the project, small videos, links to videos on youtube of you running it, etc)

## Testing
How did you test your code? What did you do to make sure your code was correct? If you wrote unit tests, you can link to them here. If you did run tests, make sure you document them as text files, and include them in your submission. 

> _Make it easy for us to know you *ran the project* and *tested the project* before you submitted this report!_


## Missing Features / What's Next
Focus on what you didn't get to do, and what you would do if you had more time, or things you would implement in the future. 

## Final Reflection
Write at least a paragraph about your experience in this course. What did you learn? What do you need to do to learn more? Key takeaways? etc.