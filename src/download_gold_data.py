# -*- coding: utf-8 -*-
"""Tai du lieu vang THAT (daily OHLCV) tu Yahoo Finance."""
import numpy as np
import yfinance as yf

TICKER = "GC=F"          # Gold Futures (COMEX). Thay "XAUUSD=X" neu muon spot.
START = "2015-01-01"
END = "2025-12-31"
OUT = "../data/doi_chung/gold_yfinance_daily.csv"

df = yf.download(TICKER, start=START, end=END, progress=False, auto_adjust=False)

if isinstance(df.columns, __import__("pandas").MultiIndex):
    df.columns = df.columns.get_level_values(0)

df = df.reset_index()
print(f"Tai duoc: {len(df)} dong ({df.Date.min().date()} -> {df.Date.max().date()})")
print(f"~ {len(df) / ((df.Date.max() - df.Date.min()).days / 365.25):.1f} ngay/nam")

r = np.log(df["Close"] / df["Close"].shift(1)).dropna()
step = df["Close"].diff()
print(f"\nTy le buoc trung buoc truoc: {(step.diff().abs() < 1e-6).mean()*100:.2f}%")
print(f"Autocorr lag1:               {r.autocorr(1):.4f}")
print(f"Ty le ngay UP:               {(r > 0).mean()*100:.2f}%")
print("\nPhan bo ngay trong tuan (0=Mon..6=Sun):")
print(df.Date.dt.dayofweek.value_counts().sort_index())

df.to_csv(OUT, index=False)
print(f"\nDa luu: {OUT}")
