# -*- coding: utf-8 -*-
"""
SO SANH CHIEN LUOC GIAO DICH VANG: AI-BASED (XGBoost) vs SIGNAL-BASED (ky thuat)

Muc tieu de tai: danh gia hieu qua 2 cach tiep can qua loi nhuan, rui ro,
va tinh on dinh.

Nguyen tac chong leakage:
- Tin hieu tai ngay t chi dung thong tin den het ngay t.
- Vi the duoc mo tai gia dong cua ngay t, huong loi nhuan cua ngay t+1.
  => strat_ret[t] = position[t-1] * log_return[t]
- Mo hinh AI dung WALK-FORWARD: huan luyen tren qua khu, du bao tuong lai,
  tai huan luyen dinh ky. Khong bao gio thay du lieu tuong lai.
"""
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

DATA_PATH = "../data/doi_chung/gold_yfinance_daily.csv"
OUT_DIR = "../ket_qua/doi_chung/"
COST_BPS = 2.0            # chi phi giao dich moi lan doi vi the (0.02% = 2 bps)
TRADING_DAYS = 252
INITIAL_TRAIN = 1260      # ~5 nam dau lam tap huan luyen ban dau
RETRAIN_EVERY = 252       # tai huan luyen moi ~1 nam
PROB_THRESHOLD = 0.5

# ==========================================================
# 1. LOAD DATA
# ==========================================================
df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
df = df.sort_values("Date").reset_index(drop=True)
df = df[["Date", "Open", "High", "Low", "Close", "Volume"]].dropna().reset_index(drop=True)
print(f"Du lieu: {len(df)} ngay ({df.Date.min().date()} -> {df.Date.max().date()})")

# ==========================================================
# 2. FEATURE ENGINEERING
# ==========================================================
df["log_return"] = np.log(df["Close"] / df["Close"].shift(1))

# --- Nhom dac trung tre ---
for lag in [1, 2, 3]:
    df[f"log_return_lag{lag}"] = df["log_return"].shift(lag)

# --- Nhom xu huong ---
df["MA10"] = df["Close"].rolling(10).mean()
df["MA30"] = df["Close"].rolling(30).mean()
df["MA50"] = df["Close"].rolling(50).mean()
df["EMA12"] = df["Close"].ewm(span=12, adjust=False).mean()
df["EMA26"] = df["Close"].ewm(span=26, adjust=False).mean()
df["MA10_MA30_diff"] = (df["MA10"] - df["MA30"]) / df["MA30"]
df["MA30_MA50_diff"] = (df["MA30"] - df["MA50"]) / df["MA50"]
df["EMA12_EMA26_diff"] = (df["EMA12"] - df["EMA26"]) / df["EMA26"]
df["price_MA10_dist"] = (df["Close"] - df["MA10"]) / df["MA10"]

# --- Nhom dong luong / dao dong ---
delta = df["Close"].diff()
avg_gain = delta.clip(lower=0).rolling(14).mean()
avg_loss = (-delta.clip(upper=0)).rolling(14).mean()
df["RSI14"] = 100 - 100 / (1 + avg_gain / avg_loss)

df["MACD"] = df["EMA12"] - df["EMA26"]
df["MACD_signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
df["MACD_hist"] = df["MACD"] - df["MACD_signal"]

# --- Nhom bien dong ---
bb_mid = df["Close"].rolling(20).mean()
bb_std = df["Close"].rolling(20).std()
df["BB_width"] = (4 * bb_std) / bb_mid
df["BB_pctB"] = (df["Close"] - (bb_mid - 2 * bb_std)) / (4 * bb_std)
df["volatility_20d"] = df["log_return"].rolling(20).std()
df["volume_ratio"] = df["Volume"] / df["Volume"].rolling(20).mean()

# --- Target: huong gia ngay t+1 ---
df["target"] = (df["log_return"].shift(-1) > 0).astype(int)

FEATURES_TREND = ["MA10_MA30_diff", "MA30_MA50_diff", "EMA12_EMA26_diff", "price_MA10_dist"]
FEATURES_MOMENTUM = ["RSI14", "MACD", "MACD_signal", "MACD_hist"]
FEATURES_VOLATILITY = ["BB_width", "BB_pctB", "volatility_20d", "volume_ratio"]
FEATURES_LAG = ["log_return_lag1", "log_return_lag2", "log_return_lag3"]
ALL_FEATURES = FEATURES_TREND + FEATURES_MOMENTUM + FEATURES_VOLATILITY + FEATURES_LAG

# Giu lai cac dong day du feature. Dong CUOI co target = NaN (khong biet t+1)
# nen bi loai — dung cho backtest la hop ly.
data = df.dropna(subset=ALL_FEATURES + ["target", "log_return"]).reset_index(drop=True)
print(f"Sau feature engineering: {len(data)} ngay | Ty le UP: {data.target.mean()*100:.2f}%")

# ==========================================================
# 3. WALK-FORWARD PREDICTION (khong leakage)
# ==========================================================
def walk_forward_predict(data, features, initial_train=INITIAL_TRAIN,
                         retrain_every=RETRAIN_EVERY):
    """Huan luyen tren qua khu, du bao khoi tiep theo, lap lai."""
    proba = pd.Series(np.nan, index=data.index)
    start = initial_train
    while start < len(data):
        end = min(start + retrain_every, len(data))
        train = data.iloc[:start]
        test = data.iloc[start:end]

        pos = (train["target"] == 1).sum()
        neg = (train["target"] == 0).sum()

        model = XGBClassifier(
            n_estimators=200,
            max_depth=3,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_lambda=1.0,
            min_child_weight=5,
            scale_pos_weight=(neg / pos) if pos else 1.0,
            eval_metric="logloss",
            random_state=42,
            n_jobs=-1,
        )
        model.fit(train[features], train["target"], verbose=False)
        proba.iloc[start:end] = model.predict_proba(test[features])[:, 1]
        start = end
    return proba, model


print("\nDang chay walk-forward XGBoost...")
data["ai_proba"], last_model = walk_forward_predict(data, ALL_FEATURES)

oos = data.dropna(subset=["ai_proba"]).copy()
print(f"Giai doan out-of-sample: {oos.Date.min().date()} -> {oos.Date.max().date()} "
      f"({len(oos)} ngay)")

ai_pred = (oos["ai_proba"] > PROB_THRESHOLD).astype(int)
print("\n=== CHAT LUONG DU BAO AI (out-of-sample) ===")
print(f"Accuracy: {accuracy_score(oos.target, ai_pred):.4f}")
print(f"F1:       {f1_score(oos.target, ai_pred):.4f}")
print(f"AUC:      {roc_auc_score(oos.target, oos.ai_proba):.4f}")
print(f"(Baseline doan luon UP: {oos.target.mean():.4f})")

# ==========================================================
# 4. XAY DUNG VI THE CAC CHIEN LUOC
# ==========================================================
# Quy uoc: position[t] duoc quyet dinh tai gia dong cua ngay t,
#          huong loi nhuan cua ngay t+1.
positions = pd.DataFrame(index=oos.index)

# --- Benchmark: Buy & Hold ---
positions["Buy_and_Hold"] = 1.0

# --- Signal-based 1: MA crossover (MA10 vs MA30) ---
positions["TA_MA_Crossover"] = (oos["MA10"] > oos["MA30"]).astype(float)

# --- Signal-based 2: MACD crossover ---
positions["TA_MACD"] = (oos["MACD"] > oos["MACD_signal"]).astype(float)

# --- Signal-based 3: RSI mean-reversion (mua khi qua ban, thoat khi qua mua) ---
rsi_pos, holding = [], 0.0
for v in oos["RSI14"].values:
    if holding == 0.0 and v < 30:
        holding = 1.0
    elif holding == 1.0 and v > 70:
        holding = 0.0
    rsi_pos.append(holding)
positions["TA_RSI"] = rsi_pos

# --- Signal-based 4: ket hop (MA crossover VA MACD cung xac nhan) ---
positions["TA_Combined"] = (
    (oos["MA10"] > oos["MA30"]) & (oos["MACD"] > oos["MACD_signal"])
).astype(float)

# --- AI-based: long khi P(up) > nguong ---
positions["AI_XGBoost"] = (oos["ai_proba"] > PROB_THRESHOLD).astype(float)

# --- AI-based long/short ---
positions["AI_XGBoost_LS"] = np.where(oos["ai_proba"] > PROB_THRESHOLD, 1.0, -1.0)

# ==========================================================
# 5. BACKTEST & TINH CHI TIEU
# ==========================================================
def backtest(position, log_return, cost_bps=COST_BPS):
    """position[t] quyet dinh tai t, an return t+1 => shift(1)."""
    pos = position.astype(float)
    gross = pos.shift(1) * log_return
    turnover = pos.diff().abs().fillna(pos.abs())
    cost = (turnover * cost_bps / 10000.0).shift(1)
    net = (gross - cost).fillna(0.0)
    return net, turnover


def metrics(net_log_ret, turnover):
    simple = np.exp(net_log_ret) - 1
    equity = np.exp(net_log_ret.cumsum())
    n = len(net_log_ret)

    total_return = equity.iloc[-1] - 1
    cagr = equity.iloc[-1] ** (TRADING_DAYS / n) - 1
    ann_vol = simple.std() * np.sqrt(TRADING_DAYS)
    sharpe = (simple.mean() / simple.std() * np.sqrt(TRADING_DAYS)) if simple.std() > 0 else np.nan

    downside = simple[simple < 0].std()
    sortino = (simple.mean() / downside * np.sqrt(TRADING_DAYS)) if downside and downside > 0 else np.nan

    running_max = equity.cummax()
    drawdown = equity / running_max - 1
    max_dd = drawdown.min()
    calmar = cagr / abs(max_dd) if max_dd < 0 else np.nan

    active = simple[net_log_ret != 0]
    win_rate = (active > 0).mean() if len(active) else np.nan
    n_trades = int((turnover > 0).sum())

    return {
        "Total_Return": total_return,
        "CAGR": cagr,
        "Ann_Volatility": ann_vol,
        "Sharpe": sharpe,
        "Sortino": sortino,
        "Max_Drawdown": max_dd,
        "Calmar": calmar,
        "Win_Rate": win_rate,
        "N_Trades": n_trades,
    }, equity, drawdown


results, equities, drawdowns = {}, {}, {}
log_ret = oos["log_return"]

for name in positions.columns:
    net, turnover = backtest(positions[name], log_ret)
    m, eq, dd = metrics(net, turnover)
    results[name] = m
    equities[name] = eq
    drawdowns[name] = dd

results_df = pd.DataFrame(results).T
results_df = results_df[["Total_Return", "CAGR", "Ann_Volatility", "Sharpe",
                         "Sortino", "Max_Drawdown", "Calmar", "Win_Rate", "N_Trades"]]

print("\n" + "=" * 100)
print("BANG SO SANH HIEU QUA CHIEN LUOC (out-of-sample, da tru chi phi giao dich)")
print("=" * 100)
display_df = results_df.copy()
for c in ["Total_Return", "CAGR", "Ann_Volatility", "Max_Drawdown", "Win_Rate"]:
    display_df[c] = (display_df[c] * 100).round(2).astype(str) + "%"
for c in ["Sharpe", "Sortino", "Calmar"]:
    display_df[c] = display_df[c].round(3)
print(display_df.to_string())

results_df.to_csv(f"{OUT_DIR}strategy_comparison_results.csv")
print("\nDa luu: strategy_comparison_results.csv")

# ==========================================================
# 6. TINH ON DINH: hieu nang theo tung nam
# ==========================================================
print("\n" + "=" * 100)
print("TINH ON DINH — Loi nhuan theo tung nam (%)")
print("=" * 100)
yearly = {}
for name in positions.columns:
    net, _ = backtest(positions[name], log_ret)
    tmp = pd.DataFrame({"year": oos["Date"].dt.year.values, "r": net.values})
    yearly[name] = tmp.groupby("year")["r"].sum().apply(lambda x: (np.exp(x) - 1) * 100)
yearly_df = pd.DataFrame(yearly).round(2)
print(yearly_df.to_string())
yearly_df.to_csv(f"{OUT_DIR}strategy_yearly_returns.csv")

print("\nDo lech chuan loi nhuan nam (cang nho cang on dinh):")
print(yearly_df.std().round(2).sort_values().to_string())

# ==========================================================
# 7. BIEU DO
# ==========================================================
fig, axes = plt.subplots(2, 1, figsize=(13, 10), sharex=True,
                         gridspec_kw={"height_ratios": [2, 1]})

dates = oos["Date"].values
styles = {
    "Buy_and_Hold": dict(color="black", ls="--", lw=1.8),
    "AI_XGBoost": dict(color="crimson", lw=2.2),
    "AI_XGBoost_LS": dict(color="darkred", lw=1.6, ls=":"),
}
for name, eq in equities.items():
    axes[0].plot(dates, eq.values, label=name, **styles.get(name, dict(lw=1.3, alpha=0.8)))
axes[0].set_title("Equity Curve — AI-based vs Signal-based (out-of-sample, net of costs)",
                  fontsize=13, fontweight="bold")
axes[0].set_ylabel("Gia tri tich luy (khoi diem = 1.0)")
axes[0].legend(loc="upper left", fontsize=9)
axes[0].grid(alpha=0.3)

for name, dd in drawdowns.items():
    axes[1].plot(dates, dd.values * 100, label=name, **styles.get(name, dict(lw=1.3, alpha=0.8)))
axes[1].set_title("Drawdown (%)", fontsize=12, fontweight="bold")
axes[1].set_ylabel("Drawdown (%)")
axes[1].set_xlabel("Thoi gian")
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig(f"{OUT_DIR}strategy_comparison_equity.png", dpi=130)
print("\nDa luu: strategy_comparison_equity.png")

# Bieu do Sharpe vs MaxDD
fig, ax = plt.subplots(figsize=(9, 6))
for name in results_df.index:
    x = abs(results_df.loc[name, "Max_Drawdown"]) * 100
    y = results_df.loc[name, "Sharpe"]
    color = "crimson" if name.startswith("AI") else ("black" if name == "Buy_and_Hold" else "steelblue")
    ax.scatter(x, y, s=140, color=color, zorder=3)
    ax.annotate(name, (x, y), textcoords="offset points", xytext=(8, 6), fontsize=9)
ax.axhline(0, color="gray", lw=0.8)
ax.set_xlabel("Max Drawdown (%) — cang nho cang tot")
ax.set_ylabel("Sharpe Ratio — cang cao cang tot")
ax.set_title("Danh doi Loi nhuan/Rui ro: AI (do) vs Ky thuat (xanh) vs Buy&Hold (den)",
             fontsize=12, fontweight="bold")
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(f"{OUT_DIR}strategy_risk_return.png", dpi=130)
print("Da luu: strategy_risk_return.png")

# Bieu do loi nhuan theo nam
fig, ax = plt.subplots(figsize=(13, 6))
yearly_df.plot(kind="bar", ax=ax, width=0.85)
ax.axhline(0, color="black", lw=0.9)
ax.set_title("Tinh on dinh — Loi nhuan theo tung nam (%)", fontsize=12, fontweight="bold")
ax.set_ylabel("Loi nhuan (%)")
ax.set_xlabel("Nam")
ax.legend(fontsize=8, ncol=2)
ax.grid(alpha=0.3, axis="y")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}strategy_yearly_returns.png", dpi=130)
print("Da luu: strategy_yearly_returns.png")

print("\n=== HOAN TAT ===")
