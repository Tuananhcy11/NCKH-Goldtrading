# -*- coding: utf-8 -*-
"""
PHAN TICH DAU RA XAC SUAT CUA MO HINH XGBOOST
Chay tren dataset goc: gold_price_2015_2025_cleaned (1).csv  (chi doc)

Muc dich: lam ro ba dai luong khac nhau ma nhieu bao cao hay nham lan:
  (1) P(up)        = xac suat GIA TANG          <- dau ra truc tiep cua XGBoost
  (2) Confidence   = xac suat DU BAO DUNG (ly thuyet, neu mo hinh hieu chuan tot)
  (3) Accuracy     = TY LE du bao dung (thuc nghiem, dem tren du lieu)
Va kiem dinh xem (2) co khop (3) hay khong => kiem dinh HIEU CHUAN (calibration).
"""
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from sklearn.metrics import (accuracy_score, roc_auc_score, log_loss,
                             brier_score_loss, confusion_matrix)

DATA_PATH = "gold_price_2015_2025_cleaned (1).csv"
INITIAL_TRAIN = 1825
RETRAIN_EVERY = 365
THRESHOLD = 0.50
RANDOM_STATE = 42

# ---------- 1. Nap du lieu & tao dac trung (giong ai_vs_ta_original_data.py) ----------
df = pd.read_csv(DATA_PATH, parse_dates=["Date"]).sort_values("Date").reset_index(drop=True)
df["log_return"] = np.log(df["Close"] / df["Close"].shift(1))
df["target"] = (df["log_return"].shift(-1) > 0).astype(float)
df.loc[df["log_return"].shift(-1).isna(), "target"] = np.nan

df["MA10"] = df["Close"].rolling(10).mean()
df["MA30"] = df["Close"].rolling(30).mean()
df["MA50"] = df["Close"].rolling(50).mean()
df["EMA12"] = df["Close"].ewm(span=12, adjust=False).mean()
df["EMA26"] = df["Close"].ewm(span=26, adjust=False).mean()
df["MA10_MA30_diff"] = (df["MA10"] - df["MA30"]) / df["MA30"]
df["MA30_MA50_diff"] = (df["MA30"] - df["MA50"]) / df["MA50"]
df["EMA12_EMA26_diff"] = (df["EMA12"] - df["EMA26"]) / df["EMA26"]
df["price_MA10_dist"] = (df["Close"] - df["MA10"]) / df["MA10"]

_d = df["Close"].diff()
_g = _d.clip(lower=0).rolling(14).mean()
_l = (-_d.clip(upper=0)).rolling(14).mean()
df["RSI14"] = 100 - 100 / (1 + _g / _l)
df["MACD"] = df["EMA12"] - df["EMA26"]
df["MACD_signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
df["MACD_norm"] = df["MACD"] / df["Close"]
df["MACD_hist_norm"] = (df["MACD"] - df["MACD_signal"]) / df["Close"]

_m = df["Close"].rolling(20).mean()
_s = df["Close"].rolling(20).std()
df["BB_width"] = 4 * _s / _m
df["BB_pctB"] = (df["Close"] - (_m - 2 * _s)) / (4 * _s)
df["volatility_20d"] = df["log_return"].rolling(20).std()
df["volume_ratio"] = df["Volume"] / df["Volume"].rolling(20).mean()
for lag in [1, 2, 3]:
    df[f"log_return_lag{lag}"] = df["log_return"].shift(lag)

FEATURES = ["MA10_MA30_diff", "MA30_MA50_diff", "EMA12_EMA26_diff", "price_MA10_dist",
            "RSI14", "MACD_norm", "MACD_hist_norm",
            "BB_width", "BB_pctB", "volatility_20d", "volume_ratio",
            "log_return_lag1", "log_return_lag2", "log_return_lag3"]

data = df.dropna(subset=FEATURES + ["target", "log_return"]).reset_index(drop=True)

# ---------- 2. Walk-forward: lay ca raw score va xac suat ----------
proba = pd.Series(np.nan, index=data.index, dtype=float)
raw = pd.Series(np.nan, index=data.index, dtype=float)

start = INITIAL_TRAIN
while start < len(data):
    end = min(start + RETRAIN_EVERY, len(data))
    tr, te = data.iloc[:start], data.iloc[start:end]
    npos, nneg = int((tr.target == 1).sum()), int((tr.target == 0).sum())
    m = XGBClassifier(n_estimators=200, max_depth=3, learning_rate=0.05,
                      subsample=0.8, colsample_bytree=0.8, reg_lambda=1.0,
                      min_child_weight=5,
                      scale_pos_weight=(nneg / npos) if npos else 1.0,
                      eval_metric="logloss", random_state=RANDOM_STATE, n_jobs=-1)
    m.fit(tr[FEATURES], tr["target"])
    proba.iloc[start:end] = m.predict_proba(te[FEATURES])[:, 1]
    raw.iloc[start:end] = m.predict(te[FEATURES], output_margin=True)
    start = end

oos = data.loc[proba.notna()].copy().reset_index(drop=True)
oos["raw_score"] = raw.dropna().values          # F(x) truoc sigmoid
oos["P_up"] = proba.dropna().values             # P(target=1)
oos["P_down"] = 1 - oos["P_up"]
oos["du_bao"] = (oos["P_up"] > THRESHOLD).astype(int)
oos["thuc_te"] = oos["target"].astype(int)
oos["dung"] = (oos["du_bao"] == oos["thuc_te"]).astype(int)
# Confidence = xac suat gan cho LOP DUOC CHON = xac suat du bao dung (ly thuyet)
oos["confidence"] = np.where(oos["du_bao"] == 1, oos["P_up"], oos["P_down"])

n = len(oos)
print("=" * 78)
print("A. KIEM TRA CONG THUC SIGMOID: P = 1 / (1 + e^-F(x))")
print("=" * 78)
check = 1 / (1 + np.exp(-oos["raw_score"]))
print(f"Sai so toi da giua sigmoid(raw_score) va P_up: {(check - oos['P_up']).abs().max():.2e}")
print(f"\nVi du 5 quan sat dau:")
print(oos[["Date", "raw_score", "P_up", "P_down", "du_bao", "thuc_te",
           "dung", "confidence"]].head().to_string(index=False))

print("\n" + "=" * 78)
print("B. BA DAI LUONG KHAC NHAU")
print("=" * 78)
acc = accuracy_score(oos.thuc_te, oos.du_bao)
print(f"(1) P(up) trung binh          : {oos['P_up'].mean():.4f}   <- xac suat GIA TANG")
print(f"(2) Confidence trung binh     : {oos['confidence'].mean():.4f}   <- xac suat du bao dung (ly thuyet)")
print(f"(3) Accuracy thuc nghiem      : {acc:.4f}   <- ty le du bao dung (dem thuc te)")
print(f"\n    Chenh lech (2) - (3)      : {oos['confidence'].mean() - acc:+.4f}")
print("    Neu ~0  => mo hinh hieu chuan tot (confidence dang tin cay)")
print("    Neu > 0 => mo hinh QUA TU TIN (overconfident)")
print("    Neu < 0 => mo hinh THIEU TU TIN (underconfident)")

print("\n" + "=" * 78)
print("C. CHI SO CHAT LUONG XAC SUAT (proper scoring rules)")
print("=" * 78)
ll = log_loss(oos.thuc_te, oos.P_up)
bs = brier_score_loss(oos.thuc_te, oos.P_up)
auc = roc_auc_score(oos.thuc_te, oos.P_up)
p_base = oos.thuc_te.mean()
print(f"Log Loss           : {ll:.4f}   (cang nho cang tot; doan buong 0.5 -> 0.6931)")
print(f"Brier Score        : {bs:.4f}   (cang nho cang tot; doan buong 0.5 -> 0.2500)")
print(f"Brier cua baseline : {np.mean((p_base - oos.thuc_te) ** 2):.4f}   (luon doan p = ty le co so)")
print(f"AUC                : {auc:.4f}")
print(f"Accuracy           : {acc:.4f}")
print(f"Baseline accuracy  : {max(p_base, 1 - p_base):.4f}   (luon doan lop da so)")

print("\n" + "=" * 78)
print("D. BANG HIEU CHUAN — 'khi mo hinh noi X%, thuc te dung bao nhieu %?'")
print("=" * 78)
bins = [0.0, 0.3, 0.4, 0.45, 0.5, 0.55, 0.6, 0.7, 1.0]
oos["bin"] = pd.cut(oos["P_up"], bins=bins, include_lowest=True)
cal = oos.groupby("bin", observed=True).agg(
    So_quan_sat=("P_up", "size"),
    P_up_TB=("P_up", "mean"),
    Ty_le_tang_thuc_te=("thuc_te", "mean"),
).reset_index()
cal["Sai_lech"] = cal["P_up_TB"] - cal["Ty_le_tang_thuc_te"]
print(cal.round(4).to_string(index=False))
print("\nCot P_up_TB vs Ty_le_tang_thuc_te: hai cot nay cang gan nhau")
print("=> mo hinh cang hieu chuan tot; P(up) cang dien giai duoc nhu xac suat that.")

print("\n" + "=" * 78)
print("E. DO CHINH XAC THEO MUC DO TU TIN")
print("=" * 78)
cbins = [0.5, 0.55, 0.6, 0.7, 0.8, 1.0]
oos["cbin"] = pd.cut(oos["confidence"], bins=cbins, include_lowest=True)
conf_tbl = oos.groupby("cbin", observed=True).agg(
    So_quan_sat=("dung", "size"),
    Confidence_TB=("confidence", "mean"),
    Accuracy_thuc_te=("dung", "mean"),
).reset_index()
conf_tbl["Sai_lech"] = conf_tbl["Confidence_TB"] - conf_tbl["Accuracy_thuc_te"]
print(conf_tbl.round(4).to_string(index=False))
print("\nY nghia thuc tien: neu Accuracy_thuc_te tang theo Confidence_TB thi co the")
print("dung nguong tin cay de LOC giao dich (co so cua chien luoc AI_XGB_Conf60).")

print("\n" + "=" * 78)
print("F. MA TRAN NHAM LAN & CAC TY LE DAN XUAT")
print("=" * 78)
cm = confusion_matrix(oos.thuc_te, oos.du_bao)
tn, fp, fn, tp = cm.ravel()
print(f"                  Du bao GIAM   Du bao TANG")
print(f"Thuc te GIAM   :      {tn:>6}        {fp:>6}")
print(f"Thuc te TANG   :      {fn:>6}        {tp:>6}")
print(f"\nTong quan sat        : {n}")
print(f"Du bao dung          : {tp + tn}  ({(tp+tn)/n*100:.2f}%)")
print(f"Du bao sai           : {fp + fn}  ({(fp+fn)/n*100:.2f}%)")
print(f"\nAccuracy  = (TP+TN)/N          = {(tp+tn)/n:.4f}")
print(f"Precision = TP/(TP+FP)         = {tp/(tp+fp):.4f}   (du bao TANG thi dung bao nhieu %)")
print(f"Recall    = TP/(TP+FN)         = {tp/(tp+fn):.4f}   (bat duoc bao nhieu % ngay TANG)")
print(f"Specificity = TN/(TN+FP)       = {tn/(tn+fp):.4f}   (bat duoc bao nhieu % ngay GIAM)")
print(f"F1        = 2PR/(P+R)          = {2*tp/(2*tp+fp+fn):.4f}")

# ---------- Xuat file ----------
out = oos[["Date", "Close", "raw_score", "P_up", "P_down", "confidence",
           "du_bao", "thuc_te", "dung"]].copy()
out.to_csv("chi_tiet_xac_suat_du_bao.csv", index=False)
cal.to_csv("bang_hieu_chuan.csv", index=False)
conf_tbl.to_csv("do_chinh_xac_theo_tu_tin.csv", index=False)
print("\nDa luu: chi_tiet_xac_suat_du_bao.csv, bang_hieu_chuan.csv, do_chinh_xac_theo_tu_tin.csv")

# ---------- Bieu do hieu chuan ----------
fig, ax = plt.subplots(1, 2, figsize=(14, 5.5))
ax[0].plot([0, 1], [0, 1], "k--", lw=1.2, label="Hieu chuan hoan hao")
ax[0].plot(cal["P_up_TB"], cal["Ty_le_tang_thuc_te"], "o-", color="crimson",
           lw=2, ms=8, label="Mo hinh XGBoost")
ax[0].set_xlabel("P(up) mo hinh du bao (trung binh moi bin)")
ax[0].set_ylabel("Ty le tang THUC TE")
ax[0].set_title("Duong hieu chuan (Reliability Curve)", fontweight="bold")
ax[0].legend(fontsize=9)
ax[0].grid(alpha=.3)

ax[1].hist(oos["P_up"], bins=40, color="steelblue", edgecolor="white")
ax[1].axvline(THRESHOLD, color="red", ls="--", lw=1.5, label=f"Nguong = {THRESHOLD}")
ax[1].set_xlabel("P(up)")
ax[1].set_ylabel("So quan sat")
ax[1].set_title("Phan bo xac suat du bao", fontweight="bold")
ax[1].legend(fontsize=9)
ax[1].grid(alpha=.3, axis="y")
plt.tight_layout()
plt.savefig("hinh7_hieu_chuan_xac_suat.png", dpi=130)
print("Da luu: hinh7_hieu_chuan_xac_suat.png")
print("\n=== HOAN TAT ===")
