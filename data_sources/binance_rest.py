
import requests

BASE_URL = "https://api.binance.com"

def get_price(symbol="BTCUSDT"):
    url = f"{BASE_URL}/api/v3/ticker/price"
    r = requests.get(url, params={"symbol": symbol})
    return r.json()

def get_klines(symbol="BTCUSDT", interval="15m", limit=100):
    url = f"{BASE_URL}/api/v3/klines"
    r = requests.get(url, params={"symbol": symbol, "interval": interval, "limit": limit})
    return r.json()

def get_exchange_info():
    url = f"{BASE_URL}/api/v3/exchangeInfo"
    r = requests.get(url)
    return r.json()

def get_open_interest(symbol="BTCUSDT"):
    url = f"https://fapi.binance.com/fapi/v1/openInterest"
    r = requests.get(url, params={"symbol": symbol})
    return r.json()
