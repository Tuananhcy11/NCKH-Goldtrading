# -*- coding: utf-8 -*-
"""
Tai tao du lieu chi gom NGAY GIAO DICH THAT tu file da bi noi suy.

Van de goc: file 'cleaned' chua ca T7/CN (va ngay le), duoc dien bang noi suy
tuyen tinh giua hai ngay giao dich that => gia ngay cuoi tuan duoc tinh tu gia
TUONG LAI (thu 2). Dieu nay gay look-ahead leakage.

Cach nhan dien ngay noi suy:
- Trong mot doan noi suy tu ngay that A den ngay that B, buoc nhay (diff) cua
  moi ngay trong doan la HANG SO = (B - A) / k.
- Do do: mot ngay la NOI SUY neu buoc nhay cua no bang buoc nhay cua ngay
  KE TIEP (vi ngay cuoi doan la ngay that B, buoc cua no bang cac buoc truoc
  nhung buoc cua ngay sau B thi khac).
=> Ngay i la noi suy  <=>  step[i] == step[i+1]

Ket hop them dieu kien lich: T7/CN chac chan khong giao dich.
"""
import numpy as np
import pandas as pd

IN_PATH = "gold_price_2015_2025_cleaned (1).csv"
OUT_PATH = "gold_real_trading_days.csv"
TOL = 1e-6

df = pd.read_csv(IN_PATH, parse_dates=["Date"])
df = df.sort_values("Date").reset_index(drop=True)
print(f"Input: {len(df)} dong ({df.Date.min().date()} -> {df.Date.max().date()})")

step = df["Close"].diff()
# step[i] == step[i+1]  => ngay i nam trong doan noi suy (khong phai diem cuoi)
is_interp = (step - step.shift(-1)).abs() < TOL
is_interp = is_interp.fillna(False)

is_weekend = df["Date"].dt.dayofweek.isin([5, 6])

# Mot ngay bi loai neu la cuoi tuan, HOAC bi phat hien la diem noi suy giua doan
drop_mask = is_weekend | is_interp

print(f"  - Ngay cuoi tuan:                 {is_weekend.sum()}")
print(f"  - Ngay bi phat hien noi suy:      {is_interp.sum()}")
print(f"  - Tong bi loai (hop):             {drop_mask.sum()}")

clean = df.loc[~drop_mask].copy().reset_index(drop=True)
print(f"\nOutput: {len(clean)} ngay giao dich that")
print(f"  ~ {len(clean) / ((clean.Date.max() - clean.Date.min()).days / 365.25):.1f} ngay/nam "
      f"(thuc te thi truong ~252)")

# ---- Kiem tra lai chat luong sau khi lam sach ----
s2 = clean["Close"].diff()
same2 = (s2.diff().abs() < TOL)
r = np.log(clean["Close"] / clean["Close"].shift(1)).dropna()

print("\n=== KIEM TRA SAU KHI LAM SACH ===")
print(f"Ty le buoc trung buoc truoc: {same2.mean()*100:.2f}%  (truoc: 76.07%)")
print(f"Autocorr lag1 log-return:    {r.autocorr(1):.4f}")
print(f"Ty le ngay UP:               {(r > 0).mean()*100:.2f}%  (truoc: 66.13%)")
print("\nPhan bo ngay trong tuan (0=Mon..4=Fri):")
print(clean.Date.dt.dayofweek.value_counts().sort_index())

clean.to_csv(OUT_PATH, index=False)
print(f"\nDa luu: {OUT_PATH}")
