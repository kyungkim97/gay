import requests


def get_doge():
    response = requests.get("https://crix-api-endpoint.upbit.com/v1/crix/candles/days/?code=CRIX.UPBIT.KRW-DOGE")
    return float(response.json()[0]['tradePrice'])


def get_bitcoin():
    response = requests.get("https://crix-api-endpoint.upbit.com/v1/crix/candles/days/?code=CRIX.UPBIT.KRW-BTC")
    return float(response.json()[0]['tradePrice'])


def get_ethereum():
    response = requests.get("https://crix-api-endpoint.upbit.com/v1/crix/candles/days/?code=CRIX.UPBIT.KRW-ETH")
    return float(response.json()[0]['tradePrice'])