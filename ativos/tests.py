import datetime
import requests
from time import sleep

# while True:
#     try:
#         api_key = "8QU6ELEHQEM8383U"
#         api_key2 = "J4ZSRVVHMVS5PEAR"
#         try:
#             url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={"USDBRL"}&interval=1min&apikey={api_key}&outputsize=compact'
#             r = requests.get(url)
#             last_busday = r.json()['Meta Data']['3. Last Refreshed'][:10]
#             data = r.json()['Time Series (Daily)'][last_busday]['5. adjusted close']
#             print(data)
#         except:
#             url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={"USDBRL"}&interval=1min&apikey={api_key2}&outputsize=compact'
#             r = requests.get(url) .json()
#             last_busday = r.['Meta Data']['3. Last Refreshed'][:10]
#
#             data = r.json()['Time Series (Daily)'][last_busday]['5. adjusted close']
#             print(data)
#     except Exception as e:
#         print(e)
#         pass



url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={"USDBRL"}&interval=1min&apikey={"8QU6ELEHQEM8383U"}&outputsize=compact'
r = requests.get(url).json()
last_busday = r['Meta Data']['3. Last Refreshed'][:10]
data = r['Time Series (Daily)'][last_busday]['5. adjusted close']
float_data = round(float(data), 2)
print(float_data)