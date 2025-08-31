
import json

def safe_json_parse(text):
    try:
        return json.loads(text)
    except Exception:
        import re
        match = re.search(r'\{.*\}', text, re.S)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                return None
        return None

from openai import OpenAI
from shared.utils import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def confirm_trade(summary_json):
    prompt = f"""
    You are a trading assistant.
    Given this analysis: {summary_json}

    Task:
    Suggest a trade plan if confidence ≥65.
    Provide:
    - Entry
    - Stop Loss
    - 3 Targets (T1, T2, T3)
    - Risk/Reward ratio
    - Final Confidence

    Output in JSON:
    {{
      "entry": ...,
      "stop_loss": ...,
      "target1": ...,
      "target2": ...,
      "target3": ...,
      "risk_reward": ...,
      "final_confidence": ...
    }}
    """

    resp = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role":"user","content":prompt}],
        max_completion_tokens=250
    )
    return resp.choices[0].message.content
