import requests
from shared.utils import log

def get_cryptopanic_sentiment(token):
    try:
        url = f"https://cryptopanic.com/api/v1/posts/?auth_token={token}&public=true&currencies=BTC,ETH,SOL"
        r = requests.get(url, timeout=10)
        data = r.json()
        sentiments = [p.get("votes", {}) for p in data.get("results", [])]
        score = 0
        for s in sentiments:
            score += (s.get("positive",0) - s.get("negative",0))
        return round(score/len(sentiments),2) if sentiments else 0
    except Exception as e:
        log(f"CryptoPanic error: {e}")
        return 0

def get_finnhub_sentiment(api_key, symbol="BINANCE:BTCUSDT"):
    try:
        url = f"https://finnhub.io/api/v1/news-sentiment?symbol={symbol}&token={api_key}"
        r = requests.get(url, timeout=10)
        data = r.json()
        sentiment = data.get("sentiment",{})
        return {
            "positive": sentiment.get("positive",0),
            "negative": sentiment.get("negative",0),
            "neutral": sentiment.get("neutral",0)
        }
    except Exception as e:
        log(f"Finnhub error: {e}")
        return {"positive":0,"negative":0,"neutral":0}

def get_fred_macro(api_key, series_id="DTWEXBGS"):
    try:
        url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json"
        r = requests.get(url, timeout=10)
        data = r.json()
        latest = data.get("observations",[])[-1]
        return float(latest.get("value",0))
    except Exception as e:
        log(f"FRED error: {e}")
        return 0
