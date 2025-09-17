import requests
import datetime
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TABLE_NAME = "ohlc_data"

# Validasi environment variable
if not SUPABASE_URL or not SUPABASE_KEY:
    print("SUPABASE_URL dan SUPABASE_KEY harus diset di .env")
    sys.exit(1)

# Endpoint Indodax
URL = "https://indodax.com/api/summaries"

def fetch_indodax():
    try:
        resp = requests.get(URL, timeout=10)
        resp.raise_for_status()
        tickers = resp.json().get("tickers", {})
        btc_idr = tickers.get("btc_idr")
        if btc_idr is None:
            raise Exception("btc_idr tidak ditemukan di response Indodax.")
        ohlc = {
            "symbol": "BTC/IDR",
            "time": datetime.datetime.utcnow().isoformat(),
            "open": float(btc_idr.get("open", 0)),
            "high": float(btc_idr.get("high", 0)),
            "low": float(btc_idr.get("low", 0)),
            "close": float(btc_idr.get("last", 0)),
            "volume": float(btc_idr.get("vol_idr", 0))
        }
        return ohlc
    except Exception as e:
        print(f"Error fetch Indodax: {e}")
        return None

def save_supabase(row):
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        res = supabase.table(TABLE_NAME).insert([row]).execute()
        if hasattr(res, "status_code") and res.status_code >= 400:
            print(f"Supabase error: {res}")
            return None
        return res
    except Exception as e:
        print(f"Error save to Supabase: {e}")
        return None

if __name__ == "__main__":
    ohlc = fetch_indodax()
    if ohlc:
        print("Fetched:", ohlc)
        resp = save_supabase(ohlc)
        print("Saved to Supabase:", resp)
    else:
        print("Gagal fetch data Indodax, tidak ada data yang disimpan ke Supabase.")
