# Indodax Supabase Trading

## Alur
1. **collector.py** ambil data harga Indodax tiap 5 menit via GitHub Actions.
2. Simpan data OHLC ke Supabase (Postgres), siap dipakai analisis/training AI.
3. Frontend bisa ambil data dari Supabase untuk visualisasi dan sinyal trading.

## Cara Pakai
1. Fork/clone repo ini
2. Edit file `.env` dan isi `SUPABASE_URL` serta `SUPABASE_KEY` sesuai akun Supabase kamu.
3. Buat tabel di Supabase: `ohlc_data` (kolom: symbol, time, open, high, low, close, volume)
4. Aktifkan GitHub Actions (otomatis jalan tiap 5 menit)
5. Web frontend bisa akses data dari Supabase

## Stack
- Data collector: Python di GitHub Actions
- Database: Supabase (Postgres)
- Frontend: HTML + Chart.js + Supabase client
- AI: Python (train model, bisa pakai Colab)

## Contoh Tabel Supabase

| symbol | time | open | high | low | close | volume |
|--------|------|------|------|-----|-------|--------|
| BTC/IDR| ...  | ...  | ...  | ... | ...   | ...    |

## Security Note
Jangan commit `.env` ke publik! Untuk GitHub Actions, simpan `SUPABASE_URL` dan `SUPABASE_KEY` di bagian **Secrets** repo.