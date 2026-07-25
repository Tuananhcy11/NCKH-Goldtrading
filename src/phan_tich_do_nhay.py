# -*- coding: utf-8 -*-
"""
PHAN TICH DO NHAY THAM SO (Sensitivity Analysis)
Chay tren dataset goc: gold_price_2015_2025_cleaned (1).csv  (chi doc)

Muc dich: do luong tac dong THUC TE cua tung tham so len dau ra, va cung
cap can cu dinh luong de hieu chinh tham so.

Bon nhom thi nghiem:
  A. INITIAL_TRAIN  : 1095, 1460, 1825, 2190   (do dai tap huan luyen ban dau)
  B. RETRAIN_EVERY  : 90, 180, 365, 730, khong tai huan luyen
  C. THRESHOLD      : 0.45 -> 0.70             (khong can huan luyen lai)
  D. RANDOM_STATE   : 0, 1, 7, 42, 123         (kiem tra do on dinh)

NGUYEN TAC SO SANH CONG BANG (quan trong):
Khi INITIAL_TRAIN thay doi, giai doan out-of-sample cung thay doi => cac chi so
KHONG so sanh truc tiep duoc. Vi vay moi cau hinh deu duoc danh gia them tren
mot CUA SO CHUNG (common window) bat dau tu index = max(INITIAL_TRAIN) da thu,
tuc 2190. Chi cac so tren cua so chung moi dung de so sanh giua cac cau hinh.
"""
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from sklearn.metrics import (accuracy_score, f1_score, roc_auc_score,
                             precision_score, recall_score, log_loss,
                             brier_score_loss)

DATA_PATH = "../data/goc/gold_price_2015_2025_cleaned (1).csv"
OUT_DIR = "../ket_qua/goc/"

# --- Cau hinh goc (baseline) dang dung trong de tai ---
BASE_INITIAL_TRAIN = 1825
BASE_RETRAIN_EVERY = 365
BASE_THRESHOLD = 0.50
BASE_RANDOM_STATE = 42

PERIODS_PER_YEAR = 365
COST_BPS = 2.0

# Cua so chung de so sanh cong bang giua cac cau hinh
EVAL_START = 2190


# ==========================================================
# 1. NAP DU LIEU & XAY DUNG DAC TRUNG (giong pipeline chinh)
# ==========================================================
def build_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

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

    d = df["Close"].diff()
    ag = d.clip(lower=0).rolling(14).mean()
    al = (-d.clip(upper=0)).rolling(14).mean()
    df["RSI14"] = 100 - 100 / (1 + ag / al)
    df["MACD"] = df["EMA12"] - df["EMA26"]
    df["MACD_signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_norm"] = df["MACD"] / df["Close"]
    df["MACD_hist_norm"] = (df["MACD"] - df["MACD_signal"]) / df["Close"]

    m = df["Close"].rolling(20).mean()
    s = df["Close"].rolling(20).std()
    df["BB_width"] = 4 * s / m
    df["BB_pctB"] = (df["Close"] - (m - 2 * s)) / (4 * s)
    df["volatility_20d"] = df["log_return"].rolling(20).std()
    df["volume_ratio"] = df["Volume"] / df["Volume"].rolling(20).mean()

    for lag in [1, 2, 3]:
        df[f"log_return_lag{lag}"] = df["log_return"].shift(lag)

    feats = ["MA10_MA30_diff", "MA30_MA50_diff", "EMA12_EMA26_diff",
             "price_MA10_dist", "RSI14", "MACD_norm", "MACD_hist_norm",
             "BB_width", "BB_pctB", "volatility_20d", "volume_ratio",
             "log_return_lag1", "log_return_lag2", "log_return_lag3"]

    data = df.dropna(subset=feats + ["target", "log_return"]).reset_index(drop=True)
    return data, feats


# ==========================================================
# 2. WALK-FORWARD (tham so hoa)
# ==========================================================
def walk_forward(data, feats, initial_train, retrain_every, random_state):
    """Tra ve Series xac suat P_up, va so lan huan luyen (so fold)."""
    proba = pd.Series(np.nan, index=data.index, dtype=float)
    start, n_fold = initial_train, 0
    while start < len(data):
        end = min(start + retrain_every, len(data))
        tr, te = data.iloc[:start], data.iloc[start:end]
        npos = int((tr["target"] == 1).sum())
        nneg = int((tr["target"] == 0).sum())
        model = XGBClassifier(
            n_estimators=200, max_depth=3, learning_rate=0.05,
            subsample=0.8, colsample_bytree=0.8, reg_lambda=1.0,
            min_child_weight=5,
            scale_pos_weight=(nneg / npos) if npos else 1.0,
            eval_metric="logloss", random_state=random_state, n_jobs=-1,
        )
        model.fit(tr[feats], tr["target"])
        proba.iloc[start:end] = model.predict_proba(te[feats])[:, 1]
        start, n_fold = end, n_fold + 1
    return proba, n_fold


# ==========================================================
# 3. DO LUONG CHAT LUONG DU BAO + HIEU QUA CHIEN LUOC
# ==========================================================
def eval_prediction(y, p, threshold):
    pred = (p > threshold).astype(int)
    out = {
        "Accuracy": accuracy_score(y, pred),
        "AUC": roc_auc_score(y, p) if y.nunique() > 1 else np.nan,
        "F1": f1_score(y, pred, zero_division=0),
        "Precision": precision_score(y, pred, zero_division=0),
        "Recall": recall_score(y, pred, zero_division=0),
        "LogLoss": log_loss(y, p, labels=[0, 1]),
        "Brier": brier_score_loss(y, p),
        "Baseline": max(y.mean(), 1 - y.mean()),
    }
    out["Vuot_baseline"] = out["Accuracy"] - out["Baseline"]
    return out


def eval_strategy(log_ret, p, threshold, cost_bps=COST_BPS,
                  periods=PERIODS_PER_YEAR):
    """Chien luoc Long/Flat: vao vi the khi P_up > threshold."""
    pos = (p > threshold).astype(float)
    gross = pos.shift(1) * log_ret
    turnover = pos.diff().abs()
    turnover.iloc[0] = abs(pos.iloc[0])
    cost = (turnover * cost_bps / 10000.0).shift(1)
    net = (gross - cost).fillna(0.0)

    simple = np.expm1(net)
    equity = np.exp(net.cumsum())
    n = len(net)
    total = equity.iloc[-1] - 1
    cagr = equity.iloc[-1] ** (periods / n) - 1
    sharpe = (simple.mean() / simple.std() * np.sqrt(periods)
              if simple.std() > 0 else np.nan)
    dd = equity / equity.cummax() - 1
    mdd = dd.min()
    return {
        "Tong_LN": total,
        "CAGR": cagr,
        "Sharpe": sharpe,
        "MaxDD": mdd,
        "Calmar": cagr / abs(mdd) if mdd < 0 else np.nan,
        "So_lenh": int((turnover > 0).sum()),
        "Turnover_nam": turnover.sum() / (n / periods),
        "Ty_le_co_vi_the": (pos != 0).mean(),
    }


def run_case(data, feats, initial_train, retrain_every, threshold,
             random_state, label):
    """Chay mot cau hinh, tra ve ket qua tren OOS day du VA tren cua so chung."""
    proba, n_fold = walk_forward(data, feats, initial_train, retrain_every,
                                 random_state)

    res = {"Cau_hinh": label, "INITIAL_TRAIN": initial_train,
           "RETRAIN_EVERY": retrain_every, "THRESHOLD": threshold,
           "RANDOM_STATE": random_state, "So_fold": n_fold}

    # --- OOS day du cua cau hinh nay ---
    mask_full = proba.notna()
    sub = data.loc[mask_full]
    res["n_OOS_day_du"] = int(mask_full.sum())
    m = eval_prediction(sub["target"], proba[mask_full], threshold)
    res.update({f"full_{k}": v for k, v in m.items()})

    # --- Cua so chung (de so sanh cong bang giua cac cau hinh) ---
    mask_common = mask_full & (data.index >= EVAL_START)
    sub_c = data.loc[mask_common]
    res["n_cua_so_chung"] = int(mask_common.sum())
    mc = eval_prediction(sub_c["target"], proba[mask_common], threshold)
    res.update({f"chung_{k}": v for k, v in mc.items()})

    sc = eval_strategy(sub_c["log_return"].reset_index(drop=True),
                       proba[mask_common].reset_index(drop=True), threshold)
    res.update({f"chung_{k}": v for k, v in sc.items()})

    return res, proba


# ==========================================================
# MAIN
# ==========================================================
def main():
    data, feats = build_data()
    print("=" * 78)
    print("PHAN TICH DO NHAY THAM SO")
    print("=" * 78)
    print(f"Tong quan sat sau xu ly : {len(data)}")
    print(f"Khoang thoi gian        : {data.Date.min().date()} -> {data.Date.max().date()}")
    print(f"Cua so chung de so sanh : tu index {EVAL_START} "
          f"({data.Date.iloc[EVAL_START].date()} -> {data.Date.iloc[-1].date()}, "
          f"n={len(data) - EVAL_START})")
    print()

    all_rows = []

    # ---------- A. INITIAL_TRAIN ----------
    print("-" * 78)
    print("A. TAC DONG CUA INITIAL_TRAIN (do dai tap huan luyen ban dau)")
    print("-" * 78)
    for it in [1095, 1460, 1825, 2190]:
        r, _ = run_case(data, feats, it, BASE_RETRAIN_EVERY, BASE_THRESHOLD,
                        BASE_RANDOM_STATE, f"A_INITIAL_TRAIN={it}")
        r["Nhom"] = "A_INITIAL_TRAIN"
        all_rows.append(r)
        print(f"  INITIAL_TRAIN={it:5} (~{it/365:.1f} nam) | fold={r['So_fold']:3} | "
              f"cua so chung: Acc={r['chung_Accuracy']:.4f} AUC={r['chung_AUC']:.4f} "
              f"Sharpe={r['chung_Sharpe']:.3f} MaxDD={r['chung_MaxDD']*100:6.2f}%")

    # ---------- B. RETRAIN_EVERY ----------
    print()
    print("-" * 78)
    print("B. TAC DONG CUA RETRAIN_EVERY (chu ky tai huan luyen)")
    print("-" * 78)
    for re_ in [90, 180, 365, 730, 10 ** 9]:
        lab = "khong tai HL" if re_ == 10 ** 9 else str(re_)
        r, _ = run_case(data, feats, BASE_INITIAL_TRAIN, re_, BASE_THRESHOLD,
                        BASE_RANDOM_STATE, f"B_RETRAIN_EVERY={lab}")
        r["Nhom"] = "B_RETRAIN_EVERY"
        all_rows.append(r)
        print(f"  RETRAIN_EVERY={lab:12} | fold={r['So_fold']:3} | "
              f"cua so chung: Acc={r['chung_Accuracy']:.4f} AUC={r['chung_AUC']:.4f} "
              f"Sharpe={r['chung_Sharpe']:.3f} MaxDD={r['chung_MaxDD']*100:6.2f}%")

    # ---------- C. THRESHOLD (khong can huan luyen lai) ----------
    print()
    print("-" * 78)
    print("C. TAC DONG CUA THRESHOLD (hau xu ly, KHONG huan luyen lai)")
    print("-" * 78)
    proba_base, _ = walk_forward(data, feats, BASE_INITIAL_TRAIN,
                                 BASE_RETRAIN_EVERY, BASE_RANDOM_STATE)
    mask_c = proba_base.notna() & (data.index >= EVAL_START)
    sub_c = data.loc[mask_c]
    p_c = proba_base[mask_c]
    for th in [0.45, 0.50, 0.55, 0.60, 0.65, 0.70]:
        m = eval_prediction(sub_c["target"], p_c, th)
        s = eval_strategy(sub_c["log_return"].reset_index(drop=True),
                          p_c.reset_index(drop=True), th)
        row = {"Nhom": "C_THRESHOLD", "Cau_hinh": f"C_THRESHOLD={th}",
               "INITIAL_TRAIN": BASE_INITIAL_TRAIN,
               "RETRAIN_EVERY": BASE_RETRAIN_EVERY, "THRESHOLD": th,
               "RANDOM_STATE": BASE_RANDOM_STATE, "So_fold": np.nan,
               "n_cua_so_chung": int(mask_c.sum())}
        row.update({f"chung_{k}": v for k, v in m.items()})
        row.update({f"chung_{k}": v for k, v in s.items()})
        all_rows.append(row)
        print(f"  THRESHOLD={th:.2f} | Acc={m['Accuracy']:.4f} "
              f"Prec={m['Precision']:.4f} Rec={m['Recall']:.4f} | "
              f"Sharpe={s['Sharpe']:.3f} MaxDD={s['MaxDD']*100:6.2f}% "
              f"lenh={s['So_lenh']:4} vi_the={s['Ty_le_co_vi_the']*100:5.1f}%")

    # ---------- D. RANDOM_STATE ----------
    print()
    print("-" * 78)
    print("D. TAC DONG CUA RANDOM_STATE (kiem tra do on dinh cua mo hinh)")
    print("-" * 78)
    for rs in [0, 1, 7, 42, 123]:
        r, _ = run_case(data, feats, BASE_INITIAL_TRAIN, BASE_RETRAIN_EVERY,
                        BASE_THRESHOLD, rs, f"D_RANDOM_STATE={rs}")
        r["Nhom"] = "D_RANDOM_STATE"
        all_rows.append(r)
        print(f"  RANDOM_STATE={rs:4} | cua so chung: Acc={r['chung_Accuracy']:.4f} "
              f"AUC={r['chung_AUC']:.4f} Sharpe={r['chung_Sharpe']:.3f} "
              f"MaxDD={r['chung_MaxDD']*100:6.2f}%")

    df_res = pd.DataFrame(all_rows)
    df_res.to_csv(OUT_DIR + "phan_tich_do_nhay.csv", index=False)
    print()
    print(f"Da luu chi tiet: {OUT_DIR}phan_tich_do_nhay.csv")

    # ---------- Tong hop do on dinh nhom D ----------
    d = df_res[df_res.Nhom == "D_RANDOM_STATE"]
    print()
    print("-" * 78)
    print("TONG HOP DO ON DINH THEO RANDOM_STATE (nhom D)")
    print("-" * 78)
    for col, name in [("chung_Accuracy", "Accuracy"), ("chung_AUC", "AUC"),
                      ("chung_Sharpe", "Sharpe"), ("chung_MaxDD", "MaxDD")]:
        v = d[col]
        print(f"  {name:9}: min={v.min():.4f}  max={v.max():.4f}  "
              f"TB={v.mean():.4f}  do lech chuan={v.std():.4f}  "
              f"bien do={v.max()-v.min():.4f}")

    # ---------- Bieu do ----------
    fig, ax = plt.subplots(2, 2, figsize=(15, 10))

    a = df_res[df_res.Nhom == "A_INITIAL_TRAIN"]
    ax[0, 0].plot(a.INITIAL_TRAIN, a.chung_Accuracy, "o-", label="Accuracy")
    ax[0, 0].plot(a.INITIAL_TRAIN, a.chung_AUC, "s-", label="AUC")
    ax[0, 0].set_title("A. Tac dong cua INITIAL_TRAIN", fontweight="bold")
    ax[0, 0].set_xlabel("INITIAL_TRAIN (so quan sat)")
    ax[0, 0].legend(); ax[0, 0].grid(alpha=.3)

    b = df_res[df_res.Nhom == "B_RETRAIN_EVERY"].copy()
    b["lab"] = b.Cau_hinh.str.replace("B_RETRAIN_EVERY=", "")
    ax[0, 1].bar(b["lab"], b.chung_Sharpe, color="steelblue")
    ax[0, 1].set_title("B. Tac dong cua RETRAIN_EVERY len Sharpe",
                       fontweight="bold")
    ax[0, 1].set_ylabel("Sharpe"); ax[0, 1].grid(alpha=.3, axis="y")
    ax[0, 1].tick_params(axis="x", rotation=20)

    c = df_res[df_res.Nhom == "C_THRESHOLD"]
    ax[1, 0].plot(c.THRESHOLD, c.chung_Precision, "o-", label="Precision")
    ax[1, 0].plot(c.THRESHOLD, c.chung_Recall, "s-", label="Recall")
    ax[1, 0].plot(c.THRESHOLD, c.chung_Accuracy, "^-", label="Accuracy")
    ax[1, 0].set_title("C. THRESHOLD: danh doi Precision - Recall",
                       fontweight="bold")
    ax[1, 0].set_xlabel("THRESHOLD"); ax[1, 0].legend(); ax[1, 0].grid(alpha=.3)

    ax2 = ax[1, 1]
    ax2.plot(c.THRESHOLD, c.chung_Sharpe, "o-", color="crimson", label="Sharpe")
    ax2.set_xlabel("THRESHOLD"); ax2.set_ylabel("Sharpe", color="crimson")
    ax2.grid(alpha=.3)
    ax3 = ax2.twinx()
    ax3.plot(c.THRESHOLD, c.chung_MaxDD * 100, "s--", color="navy",
             label="MaxDD (%)")
    ax3.set_ylabel("MaxDD (%)", color="navy")
    ax2.set_title("C. THRESHOLD: Sharpe va MaxDD", fontweight="bold")

    plt.tight_layout()
    plt.savefig(OUT_DIR + "hinh8_phan_tich_do_nhay.png", dpi=130)
    print(f"Da luu bieu do: {OUT_DIR}hinh8_phan_tich_do_nhay.png")
    print()
    print("=== HOAN TAT ===")


if __name__ == "__main__":
    main()
