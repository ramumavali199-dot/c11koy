from openai import OpenAI
from shared.utils import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def summarize_signals(symbol, candles, oi_change, news_score, finnhub_sent, macro_data):
    candle_str = "\n".join([",".join(map(str,c)) for c in candles])

    prompt = f"""
    You are a crypto analyst.
    Input data for {symbol}:

    Candlesticks (OHLCV last 6, 15m):
    {candle_str}

    Open Interest Change (last 1h): {oi_change:.2f} %

    News Sentiment (CryptoPanic score): {news_score}
    Finnhub Sentiment: {finnhub_sent}
    Macro (Dollar Index): {macro_data}

    Task:
    1. Identify candlestick/chart pattern
    2. Trend direction (Bullish/Bearish/Sideways)
    3. Key Support/Resistance
    4. Fake breakout/fakeout risk
    5. Use OI + Sentiment + Macro to validate strength of move
    6. Confidence (0–100) whether a trade setup exists

    Output strictly in JSON:
    {{
      "symbol": "{symbol}",
      "pattern": "...",
      "trend": "...",
      "support": ...,
      "resistance": ...,
      "oi_change": {oi_change:.2f},
      "news_sentiment": {news_score},
      "macro_dxy": {macro_data},
      "confidence": ...
    }}
    """

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role":"user","content":prompt}],
        max_completion_tokens=300
    )
    return resp.choices[0].message.content
