import time, schedule, json, os
import re


from shared.utils import log, send_telegram
from data_sources.binance_rest import get_ohlcv, get_open_interest
from data_sources.sentiment_sources import get_cryptopanic_sentiment, get_finnhub_sentiment, get_fred_macro
from analysis.gpt_summary import summarize_signals
from analysis.gpt_confirm import confirm_trade


import re, json

def safe_json_parse(text):
    # Remove code fences like ```json ... ```
    cleaned = re.sub(r"^```json\s*|```$", "", text.strip(), flags=re.MULTILINE)
    # Extract only the first JSON object
    match = re.search(r"\{.*?\}", cleaned, flags=re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in text")
    return json.loads(match.group(0))

COINS = ["BTCUSDT","ETHUSDT","SOLUSDT","XRPUSDT","BNBUSDT",
         "LTCUSDT","AVAXUSDT","LINKUSDT","ADAUSDT","DOGEUSDT"]

last_oi = {}

FRED_API = os.getenv("FRED_API_KEY")
FINNHUB_API = os.getenv("FINNHUB_API_KEY")
CRYPTOPANIC_TOKEN = os.getenv("CRYPTOPANIC_TOKEN")

def run_scan():
    log("Running Crypto Bot scan...")

    news_score = get_cryptopanic_sentiment(CRYPTOPANIC_TOKEN)
    finnhub_sent = get_finnhub_sentiment(FINNHUB_API)
    macro_data = get_fred_macro(FRED_API)

    for coin in COINS:
        candles = get_ohlcv(coin)
        current_oi = get_open_interest(coin)
        prev_oi = last_oi.get(coin, current_oi)
        oi_change = ((current_oi - prev_oi) / prev_oi) * 100 if prev_oi else 0
        last_oi[coin] = current_oi

        summary = summarize_signals(coin, candles, oi_change, news_score, finnhub_sent, macro_data)
        log(f"Summary: {summary}")

        try:
            summary_json = safe_json_parse(summary)
            conf = summary_json.get("confidence", 0)

            if conf >= 65:
                decision = confirm_trade(summary_json)
                log(f"TRADE SIGNAL: {decision}")

                try:
                    decision_json = safe_json_parse(decision)
                    msg = f"""
🔥 Crypto Trade Signal 🔥

🪙 Symbol: {coin}
⏱️ Timeframe: 15m
📊 Setup: {summary_json.get('pattern')}
📉 Trend: {summary_json.get('trend')}
📊 OI Change (1h): {summary_json.get('oi_change')} %
📰 News Score: {summary_json.get('news_sentiment')}
🌍 Dollar Index: {summary_json.get('macro_dxy')}
✅ Confidence: {conf}%

💰 Trade Plan:
   ➡️ Entry: {decision_json.get('entry')}
   ❌ Stop Loss: {decision_json.get('stop_loss')}
   🎯 Target 1: {decision_json.get('target1')}
   🎯 Target 2: {decision_json.get('target2')}
   🎯 Target 3: {decision_json.get('target3')}

⚠️ Risk/Reward: {decision_json.get('risk_reward')}
"""
                    send_telegram(msg.strip())
                except Exception as e:
                    log(f"Decision JSON parse error: {e}")
            else:
                log(f"{coin}: Confidence low ({conf}) → skip")
        except Exception as e:
            log(f"Summary JSON parse error: {e}")

schedule.every(15).minutes.do(run_scan)

if __name__ == "__main__":
    log("Crypto Bot with GPT-4 mini + GPT-5 mini + Sentiment started...")
    send_telegram("✅ Crypto Bot Started (Candles+OI+Sentiment+Macro integrated)")
    run_scan()
    while True:
        schedule.run_pending()
        time.sleep(10)