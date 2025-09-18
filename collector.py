import os
import requests
from supabase import create_client, Client
import time

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def fetch_indodax_history(symbol: str, resolution: str, from_ts: int, to_ts: int):
    """
    Ambil data OHLC dari endpoint TradingView history di Indodax
    resolution: "1", "5", "15", "60", etc
    from_ts, to_ts: timestamp unix detik
    """
    url = "https://indodax.com/tradingview/history"
    params = {
        "symbol": symbol,   # contoh: "BTCIDR"
        "resolution": resolution,
        "from": from_ts,
        "to": to_ts
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    print("DEBUG history response:", data)

    # Perlu cek format data
    # Biasanya format: { "s":"ok", "t":[...], "o":[...], "h":[...], "l":[...], "c":[...], "v":[...] }
    if data.get("s") != "ok":
        raise ValueError(f"history API status not ok: {data}")

    # Gabungkan per candlestick ke list dict
    ohlc_list = []
    for i, ts in enumerate(data["t"]):
        o = data["o"][i]
        h = data["h"][i]
        l = data["l"][i]
        c = data["c"][i]
        v = data["v"][i] if "v" in data else None

        ohlc_list.append({
            "time": int(ts),
            "open": float(o),
            "high": float(h),
            "low": float(l),
            "close": float(c),
            "vol": float(v) if v is not None else 0
        })

    return ohlc_list

def save_list_to_supabase(ohlc_list):
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    # bisa insert list sekaligus kalau table mendukung bulk insert
    result = supabase.table("ohlc_history").insert(ohlc_list).execute()
    print("DEBUG Supabase insert result:", result)

if __name__ == "__main__":
    # contoh: ambil candlestick per menit selama 1 jam ke belakang
    now = int(time.time())
    one_hour_ago = now - 3600
    ohlc_data = fetch_indodax_history(symbol="BTCIDR", resolution="1", from_ts=one_hour_ago, to_ts=now)
    save_list_to_supabase(ohlc_data)
