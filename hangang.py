import requests


def get_temperature():
    response = requests.get("https://api.hangang.msub.kr/")
    return float(response.json()['temp'])
