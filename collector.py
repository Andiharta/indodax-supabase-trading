import requests
import datetime
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TABLE_NAME = "ohlc_data"

# Endpoint Indodax
URL = "https://indodax.com/api/summaries"

def fetch_indodax():
    resp = requests.get(URL)
    resp.raise_for_status()
    data = resp.json()["tickers"]["btc_idr"]  # contoh: ambil BTC/IDR
    ohlc = {
        "symbol": "BTC/IDR",
        "time": datetime.datetime.utcnow().isoformat(),
        "open": float(data["open"]),
        "high": float(data["high"]),
        "low": float(data["low"]),
        "close": float(data["last"]),
        "volume": float(data["vol_idr"])
    }
    return ohlc

def save_supabase(row):
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    res = supabase.table(TABLE_NAME).insert([row]).execute()
    return res

if __name__ == "__main__":
    ohlc = fetch_indodax()
    print("Fetched:", ohlc)
    resp = save_supabase(ohlc)
    print("Saved to Supabase:", resp)