import os
import google.generativeai as genai
import pandas as pd
from datetime import datetime

# Setup Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def get_signal(symbol):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Analisis XAUUSD dan {symbol}. Berikan sinyal BUY, SELL, atau WAIT. Balas hanya 1 kata."
        response = model.generate_content(prompt)
        res = response.text.strip().upper()
        return res if res in ["BUY", "SELL", "WAIT"] else "WAIT"
    except:
        return "WAIT"

# Update CSV
symbols = ["XAUUSD", "EURUSD", "GBPUSD"]
file_path = "ai_signal.csv" # Pastikan nama file sesuai dengan yang ada di folder Anda

data = []
for sym in symbols:
    sig = get_signal(sym)
    data.append({
        "symbol": sym,
        "timeframe": "M15",
        "signal": sig,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M"),
        "expiry_minutes": 60,
        "ea": "SmartProV7"
    })

df = pd.DataFrame(data)
df.to_csv(file_path, index=False)
print("Sinyal Berhasil Diperbarui!")

