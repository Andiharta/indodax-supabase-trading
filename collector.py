import os
import requests
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def fetch_indodax():
url = "https://indodax.com/api/ticker"
response = requests.get(url)
data = response.json()
print("DEBUG Indodax response:", data)  # DEBUG: print response for troubleshooting

# Indodax ticker OHLC ada di dalam key 'ticker'  
if 'ticker' not in data:  
    raise KeyError("Key 'ticker' not found in Indodax response")  
ticker = data['ticker']  

# Pastikan semua key OHLC ada  
for k in ["open", "high", "low", "close"]:  
    if k not in ticker:  
        raise KeyError(f"Key '{k}' not found in ticker: {ticker}")  

ohlc = {  
    "open": float(ticker["open"]),  
    "high": float(ticker["high"]),  
    "low": float(ticker["low"]),  
    "close": float(ticker["close"]),  
    "vol": float(ticker.get("vol_btc", 0)),  
    "time": int(ticker.get("server_time", 0))  
}  
print("DEBUG ohlc:", ohlc)  
return ohlc

def save_to_supabase(data):
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
result = supabase.table("ohlc_data").insert(data).execute()
print("DEBUG Supabase insert result:", result)

if name == "main":
ohlc = fetch_indodax()
save_to_supabase(ohlc)

bantu modif script ini seperti nya ada error

