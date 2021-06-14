import requests


def get_corona() -> tuple:
    response = requests.get("https://capi.msub.kr/")
    today_data = response.json()['today']
    return today_data['update'], today_data['confirmation'], today_data['isolation'], today_data['dead']