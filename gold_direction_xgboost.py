# -*- coding: utf-8 -*-
"""
Dự báo hướng di chuyển giá vàng ngày tiếp theo (Binary Classification) bằng XGBoost.

Target: 1 nếu log-return(t+1) > 0, ngược lại 0.
Feature: nhóm xu hướng, động lượng, biến động, và lag log-return.
"""

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import (
    accuracy_score, f1_score, roc_auc_score,
    classification_report, confusion_matrix
)
from xgboost import XGBClassifier
import shap

DATA_PATH = "gold_price_2015_2025_cleaned (1).csv"

# ==========================================================
# CHƯƠNG 1: LOAD DATA
# ==========================================================
df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
df = df.sort_values("Date").reset_index(drop=True)
print("Shape:", df.shape)
print(df.head())

# ==========================================================
# CHƯƠNG 2: EDA NHANH
# ==========================================================
print(df.isnull().sum())
print(df.describe())

# ==========================================================
# CHƯƠNG 3: FEATURE ENGINEERING
# ==========================================================

# --- Log return & lag features ---
df["log_return"] = np.log(df["Close"] / df["Close"].shift(1))
for lag in [1, 2, 3]:
    df[f"log_return_lag{lag}"] = df["log_return"].shift(lag)

# --- Nhóm xu hướng: MA, EMA ---
df["MA10"] = df["Close"].rolling(10).mean()
df["MA30"] = df["Close"].rolling(30).mean()
df["MA50"] = df["Close"].rolling(50).mean()
df["EMA12"] = df["Close"].ewm(span=12, adjust=False).mean()
df["EMA26"] = df["Close"].ewm(span=26, adjust=False).mean()

# Chênh lệch dạng % để ổn định qua các mức giá khác nhau
df["MA10_MA30_diff"] = (df["MA10"] - df["MA30"]) / df["MA30"]
df["MA30_MA50_diff"] = (df["MA30"] - df["MA50"]) / df["MA50"]
df["EMA12_EMA26_diff"] = (df["EMA12"] - df["EMA26"]) / df["EMA26"]
df["price_MA10_dist"] = (df["Close"] - df["MA10"]) / df["MA10"]

# --- Nhóm động lượng/dao động: RSI, MACD ---
delta = df["Close"].diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)
avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()
rs = avg_gain / avg_loss
df["RSI14"] = 100 - (100 / (1 + rs))

df["MACD"] = df["EMA12"] - df["EMA26"]
df["MACD_signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
df["MACD_hist"] = df["MACD"] - df["MACD_signal"]

# --- Nhóm biến động: Bollinger Bands, rolling std, volume ---
bb_mid = df["Close"].rolling(20).mean()
bb_std = df["Close"].rolling(20).std()
df["BB_upper_dist"] = (df["Close"].rolling(20).mean() + 2 * bb_std - bb_mid) / bb_mid
df["BB_lower_dist"] = (bb_mid - (df["Close"].rolling(20).mean() - 2 * bb_std)) / bb_mid
df["BB_width"] = (4 * bb_std) / bb_mid
df["volatility_20d"] = df["log_return"].rolling(20).std()
df["volume"] = df["Volume"]

# ==========================================================
# CHƯƠNG 4: TẠO TARGET (không leakage — dùng return t+1)
# ==========================================================
df["log_return_next"] = np.log(df["Close"].shift(-1) / df["Close"])
df["target"] = (df["log_return_next"] > 0).astype(int)

# Loại bỏ NaN sinh ra từ rolling window (đầu chuỗi) và từ shift(-1) (cuối chuỗi)
df = df.dropna().reset_index(drop=True)
print("Sau khi loại NaN:", df.shape)
print(df["target"].value_counts(normalize=True))

# ==========================================================
# CHƯƠNG 5: ĐỊNH NGHĨA CÁC NHÓM FEATURE (dùng cho ablation study)
# ==========================================================
FEATURES_TREND = ["MA10_MA30_diff", "MA30_MA50_diff", "EMA12_EMA26_diff", "price_MA10_dist"]
FEATURES_MOMENTUM = ["RSI14", "MACD", "MACD_signal", "MACD_hist"]
FEATURES_VOLATILITY = ["BB_upper_dist", "BB_lower_dist", "BB_width", "volatility_20d", "volume"]
FEATURES_LAG = ["log_return_lag1", "log_return_lag2", "log_return_lag3"]

FEATURE_GROUPS = {
    "A_trend_only": FEATURES_TREND,
    "B_trend_momentum": FEATURES_TREND + FEATURES_MOMENTUM,
    "C_trend_momentum_vol": FEATURES_TREND + FEATURES_MOMENTUM + FEATURES_VOLATILITY,
    "D_full": FEATURES_TREND + FEATURES_MOMENTUM + FEATURES_VOLATILITY + FEATURES_LAG,
}

# ==========================================================
# CHƯƠNG 6: TRAIN/TEST SPLIT (Time-based, không shuffle)
# ==========================================================
n = len(df)
train_end = int(n * 0.70)
val_end = int(n * 0.85)

train_df = df.iloc[:train_end]
val_df = df.iloc[train_end:val_end]
test_df = df.iloc[val_end:]

print(f"Train: {len(train_df)} | Val: {len(val_df)} | Test: {len(test_df)}")

# ==========================================================
# CHƯƠNG 7: ABLATION STUDY — huấn luyện theo từng nhóm feature
# ==========================================================
results = {}
models = {}

for name, feats in FEATURE_GROUPS.items():
    X_train, y_train = train_df[feats], train_df["target"]
    X_val, y_val = val_df[feats], val_df["target"]
    X_test, y_test = test_df[feats], test_df["target"]

    pos = (y_train == 1).sum()
    neg = (y_train == 0).sum()
    scale_pos_weight = neg / pos if pos > 0 else 1.0

    model = XGBClassifier(
        n_estimators=300,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=scale_pos_weight,
        eval_metric="logloss",
        random_state=42,
    )
    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        verbose=False,
    )

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba)

    results[name] = {"accuracy": acc, "f1": f1, "auc": auc, "n_features": len(feats)}
    models[name] = model

    print(f"\n=== {name} ({len(feats)} features) ===")
    print(f"Accuracy: {acc:.4f} | F1: {f1:.4f} | AUC: {auc:.4f}")
    print(classification_report(y_test, y_pred, target_names=["DOWN", "UP"]))

# ==========================================================
# CHƯƠNG 8: BẢNG TỔNG HỢP ABLATION
# ==========================================================
results_df = pd.DataFrame(results).T
print("\n=== BẢNG TỔNG HỢP ABLATION STUDY ===")
print(results_df)

plt.figure(figsize=(8, 5))
results_df[["accuracy", "f1", "auc"]].plot(kind="bar")
plt.title("So sánh hiệu năng theo nhóm feature (Ablation Study)")
plt.ylabel("Score")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig("ablation_study_results.png")
print("\nĐã lưu biểu đồ ablation: ablation_study_results.png")

# ==========================================================
# CHƯƠNG 9: MODEL FULL — FEATURE IMPORTANCE & SHAP
# ==========================================================
best_model = models["D_full"]
best_feats = FEATURE_GROUPS["D_full"]
X_test_full = test_df[best_feats]

# Feature importance (gain)
importance = pd.Series(
    best_model.get_booster().get_score(importance_type="gain"),
    name="gain"
).sort_values(ascending=False)
print("\n=== Feature Importance (Gain) — Model Full ===")
print(importance)

plt.figure(figsize=(8, 6))
importance.plot(kind="barh")
plt.title("XGBoost Feature Importance (Gain) - Full Model")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("feature_importance_full.png")
print("Đã lưu: feature_importance_full.png")

# SHAP values
explainer = shap.TreeExplainer(best_model)
shap_values = explainer.shap_values(X_test_full)

plt.figure()
shap.summary_plot(shap_values, X_test_full, show=False)
plt.tight_layout()
plt.savefig("shap_summary_full.png")
print("Đã lưu: shap_summary_full.png")

# ==========================================================
# CHƯƠNG 10: CONFUSION MATRIX MODEL FULL
# ==========================================================
y_pred_full = best_model.predict(X_test_full)
cm = confusion_matrix(test_df["target"], y_pred_full)

plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["DOWN", "UP"], yticklabels=["DOWN", "UP"])
plt.title("Confusion Matrix — Model Full")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig("confusion_matrix_full.png")
print("Đã lưu: confusion_matrix_full.png")

print("\n=== HOÀN TẤT PIPELINE ===")
