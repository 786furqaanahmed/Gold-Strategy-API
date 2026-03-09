import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# STRATEGY SETTINGS (Your Original Logic)
MAJOR_INTERVAL = 20
REACTION_ZONE = 3
RISK_REWARD = 3
API_KEY = os.getenv("TWELVE_DATA_KEY") # We'll set this in Step 2

@app.route('/signal')
def get_gold_signal():
    # 1. FETCH REAL-TIME PRICE (5,100+)
    url = f"https://api.twelvedata.com/price?symbol=XAU/USD&apikey={API_KEY}"
    price_data = requests.get(url).json()
    price = float(price_data['price'])

    # 2. GENERATE YOUR LEVEL GRID
    base_major = round(price / MAJOR_INTERVAL) * MAJOR_INTERVAL
    major_levels = [base_major + (i * MAJOR_INTERVAL) for i in range(-2, 3)]
    
    # 3. DETECT SIGNAL (Your exact ChatGPT Logic)
    # Note: In a live app, we'd pull 'trend' from a moving average. 
    # For now, we'll detect if price is ABOVE or BELOW the nearest level.
    signal = "WAIT"
    entry, sl, tp = 0, 0, 0

    for level in major_levels:
        if abs(price - level) <= REACTION_ZONE:
            if price > level: # UPTREND logic
                signal = "BUY"
                entry = price
                sl = level - REACTION_ZONE
                tp = entry + ((entry - sl) * RISK_REWARD)
            else: # DOWNTREND logic
                signal = "SELL"
                entry = price
                sl = level + REACTION_ZONE
                tp = entry - ((sl - entry) * RISK_REWARD)
            break

    return jsonify({
        "price": round(price, 2),
        "signal": signal,
        "entry": round(entry, 2) if entry != 0 else "---",
        "sl": round(sl, 2) if sl != 0 else "---",
        "tp": round(tp, 2) if tp != 0 else "---",
        "nearest_level": base_major
    })

if __name__ == "__main__":
    app.run()
