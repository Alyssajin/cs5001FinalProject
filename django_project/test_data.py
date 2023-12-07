"""
This is test_data.py for testing all functions in data.py except the draw_graph function.
It utilises unittest and mock to test fetching API data and process raw data.
Files of oil_data.json and new_data.json will be called while running this py file.

Student: Alyssa Nuanxin Jin
Semester: Fall 2023
"""

import json
import unittest
import requests_mock
import requests
from .oil import data as dt


class TestData(unittest.TestCase):
    def test_fetch_api_data_using_mocks(self):
        """Test fetch_api_data function"""
        test_url = (f'{dt.EIA_ENDPOINT}/?api_key={dt.EIA_API_KEY}'
                    f'&frequency=daily&data[0]=value&facets[product][]=EPLLPA'
                    f'&start=2001-01-03&end=2001-01-03&sort[0][column]=period'
                    f'&sort[0][direction]=desc&offset=0&length=5000')
        # Creates a fake expected value
        with open('./django_project/oil_data.json') as f:
            expected = json.load(f)
        # Creates a fake requests response object
        with requests_mock.Mocker() as m:
            m.get(test_url, json=expected)
            response = requests.get(test_url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['response']['data'][0]['value'],
                             0.78)

    def test_get_news_params(self):
        """Test get_news_params function"""
        product_name = 'Brent'
        expected = {
            'apiKey': '2d7846b501ec4d0dafa4816805a47174',
            'qInTitle': 'Brent',
            'from': dt.NEWS_STARTING_DATE,
            'to': dt.NEWS_ENDING_DATE,
            'language': 'en',
            'sortBy': 'popularity'
        }
        actual = dt.get_news_params(product_name)
        self.assertEqual(actual, expected)

    def test_get_oil_params(self):
        """Test get_oil_params function"""
        product_name = 'Brent'
        start_date = '2020-01-28'
        end_date = '2020-04-29'
        expected = {
            "api_key": '215LPlEH4HEH9iCacvem0zZlJytc6I6N34HkAVEM',
            'frequency': 'daily',
            'data[0]': 'value',
            'facets[product][]': 'EPCBRENT',
            'start': '2020-01-28',
            'end': '2020-04-29',
            'sort[0][column]': 'period',
            'sort[0][direction]': 'asc',
            'offset': 0,
            'length': 5000
        }
        actual = dt.get_oil_params(start_date=start_date, end_date=end_date, product_name=product_name)
        self.assertEqual(actual, expected)

    def test_clean_news(self):
        """Test clean_news function"""
        data = {
            'articles': {
                'description': 'Happy'
            }
        }
        expected = {'description': 'Happy'}
        actual = dt.clean_news(data)
        self.assertEqual(actual, expected)

    def test_clean_oil_data(self):
        """Test clean_oil_data"""
        data = {
            'response': {
                'data': {
                    'value': 0.34
                }
            }
        }
        expected = {'value': 0.34}
        actual = dt.clean_oil_data(data)
        self.assertEqual(actual, expected)

    def test_is_data(self):
        """Test is_data function."""
        # Test 1 is_date('2013/14/21') == False
        date = '2013/14/21'
        expected = False
        actual = dt.is_date(date)
        self.assertEqual(actual, expected)
        # Test 2 is_date('hap') == False
        date = 'hap'
        expected = False
        actual = dt.is_date(date)
        self.assertEqual(actual, expected)
        # Test 3 is_date('2023/12/25') == True
        date = '2023/12/25'
        expected = True
        actual = dt.is_date(date)
        self.assertEqual(actual, expected)

    def test_format_date(self):
        """Test format_date"""
        # Test 1 format_date('2023/2/31') == '2015-01-01'
        date = '2023/2/31'
        expected = '2015-01-01'
        actual = dt.format_date(date)
        self.assertEqual(actual, expected)
        # Test 2 format_date('happy') == '2015-01-01'
        date = 'happy'
        expected = '2015-01-01'
        actual = dt.format_date(date)
        self.assertEqual(actual, expected)
        # Test 3 format_date('2023-01-03') =='2023-01-03'
        date = '2023-01-03'
        expected = '2023-01-03'
        actual = dt.format_date(date)
        self.assertEqual(actual, expected)

    def test_choose_product(self):
        """Test choose_product function."""
        # Test 1 choose_product('WTI') == 'EPCWTI'
        product_name = 'WTI'
        expected = 'EPCWTI'
        actual = dt.choose_product(product_name)
        self.assertEqual(actual, expected)
        # Test 2 choose_product('Propane') == 'EPLLPA'
        product_name = 'Propane'
        expected = 'EPLLPA'
        actual = dt.choose_product(product_name)
        self.assertEqual(actual, expected)
        # Test 3 choose_product('Diesel') == 'EPD2DXL0'
        product_name = 'Diesel'
        expected = 'EPD2DXL0'
        actual = dt.choose_product(product_name)
        self.assertEqual(actual, expected)
        # Test 4 choose_product('Brent') == 'EPCBRENT'
        product_name = 'Brent'
        expected = 'EPCBRENT'
        actual = dt.choose_product(product_name)
        self.assertEqual(actual, expected)

    def test_process_oil_data(self):
        """Test process_oil_data function."""
        with open("./django_project/oil_data.json") as f:
            data = json.load(f)['response']['data']
        expected = [[0.78], ["2001-01-03"]]
        actual = dt.process_oil_data(data)
        self.assertEqual(actual, expected)

    def test_get_product_unit(self):
        """Test get_product_unit function."""
        # Test 1 get_product_unit('Brent') == '$/BBL'
        product_name = 'Brent'
        expected = '$/BBL'
        actual = dt.get_product_unit(product_name)
        self.assertEqual(actual, expected)
        # Test 2 get_product_unit('Gasoline') =='$/GAL'
        product_name = 'Gasoline'
        expected = '$/GAL'
        actual = dt.get_product_unit(product_name)
        self.assertEqual(actual, expected)
        # Test 3 get_product_unit('Propane')
        product_name = 'Propane'
        expected = '$/GAL'
        actual = dt.get_product_unit(product_name)
        self.assertEqual(actual, expected)

    def test_process_news(self):
        """Test process_news function."""
        with open("./django_project/news_data.json") as f:
            data = json.load(f)
        expected = (
            [
                'Oil prices tumble as OPEC+ pushes back key meeting and Saudi Arabia grows frustrated',
                'Russia\'s oil exports are climbing near 4-month highs despite big production cuts',
                'Oil prices are at their lowest level since August. Here\'s everything moving crude markets.'
            ],
            [
                'Saudi Arabia has expressed frustration with other oil cartel members\' production levels, sources told Bloomberg.',
                'Moscow\'s crude exports climbed higher in the last four weeks despite earlier its move to slash its production along with Saudi Arabia.',
                'Factors include the Israel-Hamas conflict, production cuts from Russia and Saudi Arabia, uncertainty in China, and shaky global demand.'
            ],
            [
                '2023-11-22T14:51:30Z',
                '2023-11-07T16:43:31Z',
                '2023-11-07T15:45:59Z'
            ],
            [
                'https://markets.businessinsider.com/news/commodities/oil-prices-today-crude-opec-saudi-arabia-russia-economy-energy-2023-11',
                'https://markets.businessinsider.com/news/stocks/russia-oil-exports-production-cuts-crude-prices-revenue-ukraine-economy-2023-11',
                'https://markets.businessinsider.com/news/commodities/oil-price-wti-crude-markets-china-israel-hamas-war-demand-2023-11'
            ]
        )
        actual = dt.process_news(data)
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
