# -*- coding: utf-8 -*-
"""Kiem tra chat luong du lieu: phat hien noi suy / smoothing artifact."""
import pandas as pd
import numpy as np

DATA_PATH = "../data/goc/gold_price_2015_2025_cleaned (1).csv"

df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
df = df.sort_values("Date").reset_index(drop=True)

print("Rows:", len(df))
print("Date range:", df.Date.min(), "->", df.Date.max())
print()

# 1. Kiem tra noi suy tuyen tinh: buoc tang/giam bang nhau lien tiep
d = df["Close"].diff()
same_step = (d.diff().abs() < 1e-6)
print("Ty le buoc co diff GIONG buoc truoc (dau hieu noi suy tuyen tinh): "
      f"{same_step.mean()*100:.2f}%")

# 2. Autocorrelation cua log-return (thuc te thi truong ~ 0)
r = np.log(df["Close"] / df["Close"].shift(1)).dropna()
print(f"Autocorr lag1 log-return: {r.autocorr(1):.4f}")
print(f"Autocorr lag2 log-return: {r.autocorr(2):.4f}")
print(f"Autocorr lag3 log-return: {r.autocorr(3):.4f}")
print(f"Ty le ngay UP: {(r > 0).mean()*100:.2f}%")
print()

# 3. Ngay trong tuan (du lieu that khong co T7/CN)
print("Phan bo ngay trong tuan (0=Mon .. 6=Sun):")
print(df.Date.dt.dayofweek.value_counts().sort_index())
print()

# 4. Kiem tra so ngay lien tiep khong co gap cuoi tuan
gaps = df.Date.diff().dt.days.value_counts().sort_index()
print("Phan bo khoang cach giua cac ngay (so ngay):")
print(gaps)
print()

# 5. Kiem tra OHLC hop le (High >= Close >= Low)
invalid = ((df.High < df.Close) | (df.Low > df.Close) |
           (df.High < df.Open) | (df.Low > df.Open)).sum()
print(f"So dong OHLC khong hop le: {invalid}")

# 6. In 25 gia Close dau de nhin bang mat
print()
print("25 gia Close dau va buoc nhay:")
head = df[["Date", "Close"]].head(25).copy()
head["step"] = head["Close"].diff()
print(head.to_string(index=False))
