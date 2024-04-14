import requests
# url = f"https://api.polygon.io/v2/aggs/ticker/gold/range/1/day/2023-01-09/2023-01-09?adjusted=true&sort=asc&limit=120&apiKey=jeMfFHedjPJ3zIZfbpMEduqaxyqgXzbR"

# res = requests.get(f"https://api.polygon.io/v1/open-close/gold/2024-04-05?adjusted=true&apiKey=LnR21zv6euM7KmY_HafxN9XgwdnmltXE")
# print(res)
# breakpoint()

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SimplyWealthProject.settings")
# django.setup()


# API_KEY= "THYPFDH0SM8R242R"
# # url = f'https://www.alphavantage.co/query?function=MARKET_STATUS&apikey={API_KEY}'
# # r = requests.get(url)
# # data = r.json()

# # print(data)
# # breakpoint()


# # import requests

# import requests

# # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
# url = 'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={API_KEY}'
# r = requests.get(url)
# data = r.json()

# print(data)
# breakpoint()

#https://www.alphavantage.co/support/#api-key
# from SimplyWealthApp.models import StocksPriceHistory



import requests

# all_ticker_url = f"https://api.polygon.io/v3/reference/tickers?active=true&apiKey=LnR21zv6euM7KmY_HafxN9XgwdnmltXE"
all_ticker_url = requests.get(f"https://api.polygon.io/v1/open-close/ASML/2024-04-05?adjusted=true&apiKey=LnR21zv6euM7KmY_HafxN9XgwdnmltXE")
res = requests.get(all_ticker_url)
print(res)
# rests = res.json().get('results')
breakpoint()
# for details in rests:
#     name = details.get('name')
#     ticker = details.get('ticker')
#     price = requests.get(f"https://api.polygon.io/v1/open-close/{price}/2024-04-05?adjusted=true&apiKey=LnR21zv6euM7KmY_HafxN9XgwdnmltXE")
#     print(price)
#     StocksPriceHistory.objects.create(stock_name=name, ticker=ticker, price=price)
