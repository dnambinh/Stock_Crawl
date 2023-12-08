import pandas as pd
import requests
from datetime import date
from datetime import timedelta
import time

HEADERS = {'content-type': 'application/x-www-form-urlencoded',
           'User-Agent': 'Mozilla'}
API_VNDIRECT = "https://finfo-api.vndirect.com.vn/v4/stock_prices?sort=date&q=code:{}~date:gte:{}~date:lte:{}&size=9990&page=1"


def craw_stock_list():
    to_date = date.today() - timedelta(days=365)
    from_date = to_date - timedelta(days=3650)

    to_date = to_date.isoformat()
    from_date = from_date.isoformat()

    print(to_date)
    print(from_date)
    stock_code = "VCB"

    response = requests.get(
        API_VNDIRECT.format(stock_code, from_date, to_date), headers=HEADERS, timeout=10)

    if response.status_code == 200:
        for i in range(1, 10):
            try:
                print("loading...")
                response = requests.get(
                    API_VNDIRECT.format(stock_code, from_date, to_date), headers=HEADERS, timeout=10)
                break
            except:
                print("Connection refused by the server..")
                time.sleep(5)
                print("loading...")
                continue

        response = requests.get(
            API_VNDIRECT.format(stock_code, from_date, to_date), headers=HEADERS, timeout=10)
        stock_price_df = pd.DataFrame(response.json()["data"])[["date", "basicPrice", "ceilingPrice", "floorPrice", "open", "high",
                                                                "low", "close", "average", "adOpen", "adHigh", "adLow", "adClose", "adAverage", "pctChange"]]
        stock_price_df = pd.concat(
            [stock_price_df, stock_price_df], ignore_index=True)
    else:
        print('Error', response.status_code)

    # delete duplicates
    stock_price_df.drop_duplicates(subset=None, inplace=True)
    # sorting DataFrame
    stock_price_df['date'] = stock_price_df['date'].apply(pd.to_datetime)
    stock_price_df = stock_price_df.sort_values(by='date')
    #standardize
    stock_price_df['date'] = pd.to_datetime(stock_price_df.date).dt.strftime('%d/%m/%Y')
    # Write the results to a different file
    stock_price_df.to_csv(
        'E:/PTKT/Stock_Crawl/data/{}_stock.csv'.format(stock_code), index=False)
    print("done")


craw_stock_list()
