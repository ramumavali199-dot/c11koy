import requests

BASE_URL = "https://api.binance.com"

def get_price(symbol="BTCUSDT"):
    url = f"{BASE_URL}/api/v3/ticker/price"
    r = requests.get(url, params={"symbol": symbol})
    return r.json()

def get_ohlcv(symbol="BTCUSDT", interval="15m", limit=100):
    """
    Fetch OHLCV (Open, High, Low, Close, Volume) data.
    Returns list of dicts with keys: open_time, open, high, low, close, volume, close_time.
    """
    url = f"{BASE_URL}/api/v3/klines"
    r = requests.get(url, params={"symbol": symbol, "interval": interval, "limit": limit})
    data = r.json()
    ohlcv = []
    for k in data:
        ohlcv.append({
            "open_time": k[0],
            "open": float(k[1]),
            "high": float(k[2]),
            "low": float(k[3]),
            "close": float(k[4]),
            "volume": float(k[5]),
            "close_time": k[6],
        })
    return ohlcv

def get_exchange_info():
    url = f"{BASE_URL}/api/v3/exchangeInfo"
    r = requests.get(url)
    return r.json()

def get_open_interest(symbol="BTCUSDT"):
    url = "https://fapi.binance.com/fapi/v1/openInterest"
    r = requests.get(url, params={"symbol": symbol})
    return r.json()

