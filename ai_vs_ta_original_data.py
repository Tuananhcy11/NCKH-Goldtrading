# -*- coding: utf-8 -*-
"""
================================================================================
SO SANH CHIEN LUOC GIAO DICH VANG: AI-BASED (XGBoost) vs SIGNAL-BASED (KY THUAT)
Chay tren BO DATASET GOC: gold_price_2015_2025_cleaned (1).csv
File dataset chi duoc DOC, KHONG chinh sua, KHONG thay the.
================================================================================

CO SO LY LUAN CUA THIET KE THUC NGHIEM — xem chi tiet tai CO_SO_LY_LUAN.md

Cau truc chuong trinh:
  Chuong 1. Nap du lieu goc
  Chuong 2. Xay dung bien muc tieu (target)
  Chuong 3. Xay dung tap dac trung (4 nhom)
  Chuong 4. Kiem dinh chat luong du lieu (bat buoc bao cao)
  Chuong 5. Huan luyen walk-forward (chong look-ahead bias)
  Chuong 6. Ablation study — do luong dong gop tung nhom dac trung
  Chuong 7. Xay dung vi the cac chien luoc
  Chuong 8. Backtest & do luong hieu qua
  Chuong 9. Kiem dinh tinh on dinh
  Chuong 10. Dien giai mo hinh (Feature Importance + SHAP)
  Chuong 11. Truc quan hoa
"""
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from xgboost import XGBClassifier
from sklearn.metrics import (accuracy_score, f1_score, roc_auc_score,
                             classification_report, confusion_matrix)
import shap

# ================== THAM SO CAU HINH ==================
DATA_PATH = "gold_price_2015_2025_cleaned (1).csv"   # DATASET GOC — chi doc

# CO SO LY LUAN: dataset goc chua ca T7/CN => 1 nam co ~365 quan sat, khong phai
# 252 nhu du lieu phien giao dich thuc. He so quy doi nam (annualization factor)
# phai khop voi tan so quan sat that cua chuoi, neu khong Sharpe se bi lech
# theo ty le sqrt(365/252) ~ 1.20 (tuc phong dai ~20%).
PERIODS_PER_YEAR = 365

COST_BPS = 2.0          # Chi phi giao dich 1 chieu (2 bps = 0.02%)
INITIAL_TRAIN = 1825    # ~5 nam dau lam tap huan luyen ban dau
RETRAIN_EVERY = 365     # Tai huan luyen dinh ky ~1 nam
PROB_THRESHOLD = 0.50   # Nguong xac suat de vao vi the Long
RANDOM_STATE = 42

SUFFIX = "_original"    # hau to file ket qua, tranh ghi de ket qua cu


# ==========================================================
# CHUONG 1. NAP DU LIEU GOC
# ==========================================================
print("=" * 80)
print("CHUONG 1. NAP DU LIEU GOC")
print("=" * 80)

df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
df = df.sort_values("Date").reset_index(drop=True)
print(f"Nguon: {DATA_PATH}  (chi doc, khong chinh sua)")
print(f"Kich thuoc: {df.shape[0]} dong x {df.shape[1]} cot")
print(f"Khoang thoi gian: {df.Date.min().date()} -> {df.Date.max().date()}")
print(f"Cac cot: {list(df.columns)}")
print(f"Gia tri thieu:\n{df.isnull().sum().to_string()}")


# ==========================================================
# CHUONG 2. XAY DUNG BIEN MUC TIEU
# ==========================================================
# CO SO LY LUAN:
# (1) Dung log-return thay vi chenh lech gia tuyet doi vi log-return co tinh
#     cong don theo thoi gian (time-additive) va on dinh phuong sai hon.
# (2) Dung phan loai nhi phan thay vi hoi quy: trong giao dich, quyet dinh
#     Long/Flat chi phu thuoc DAU cua loi nhuan ky vong, khong phu thuoc do lon.
#     Hoi quy toi thieu hoa MSE se uu tien du bao dung cac cu bien dong lon,
#     trong khi muc tieu giao dich la du bao dung HUONG o da so phien.
# (3) target[t] = 1 neu log-return[t+1] > 0. Nhan tai thoi diem t mo ta tuong
#     lai t+1 => khi huan luyen phai dam bao dac trung tai t khong chua thong
#     tin sau t (xem Chuong 5).
# ==========================================================
print("\n" + "=" * 80)
print("CHUONG 2. XAY DUNG BIEN MUC TIEU")
print("=" * 80)

df["log_return"] = np.log(df["Close"] / df["Close"].shift(1))
df["target"] = (df["log_return"].shift(-1) > 0).astype(float)
df.loc[df["log_return"].shift(-1).isna(), "target"] = np.nan

print("target = 1 neu log_return(t+1) > 0, nguoc lai 0")
print(f"Phan bo target:\n{df['target'].value_counts(normalize=True).to_string()}")


# ==========================================================
# CHUONG 3. XAY DUNG TAP DAC TRUNG (4 NHOM)
# ==========================================================
# CO SO LY LUAN TUNG NHOM:
#
# NHOM 1 — XU HUONG (Trend): MA(10/30/50), EMA(12/26) va chenh lech
#   Ly thuyet Dow: gia van dong theo xu huong co quan tinh. Trung binh dong
#   lam tron nhieu ngan han de boc tach thanh phan xu huong. EMA gan trong so
#   cao hon cho quan sat gan => phan ung nhanh hon MA voi thay doi che do.
#   QUAN TRONG: dua vao mo hinh CHENH LECH TUONG DOI (%) giua cac duong, khong
#   dua gia tri tuyet doi. Ly do: (a) cay quyet dinh chia theo nguong tuyet doi,
#   ma muc gia vang 2015 (~1200) va 2025 (~4000) khac nhau ba lan => nguong hoc
#   tu qua khu vo nghia o tuong lai (concept drift); (b) chenh lech MA ngan -
#   MA dai chinh la dinh nghia toan hoc cua tin hieu giao cat, giup mo hinh
#   khong phai tu hoc quan he tuong tac nay.
#
# NHOM 2 — DONG LUONG / DAO DONG (Momentum & Oscillator): RSI(14), MACD
#   RSI chuan hoa ve [0,100], do suc manh tuong doi cua luc mua/ban =>
#   nhan dien vung qua mua/qua ban (co so cua gia thuyet hoi quy ve trung binh).
#   MACD do khoang cach hai EMA => bieu dien gia toc cua xu huong; histogram
#   (MACD - Signal) la dao ham bac hai cua gia, phat hien phan ky som.
#
# NHOM 3 — DO BIEN DONG (Volatility): Bollinger Bands, rolling std, volume
#   Ly thuyet che do thi truong (regime): quan he giua dac trung va huong gia
#   KHONG on dinh ma phu thuoc trang thai bien dong. Cung mot tin hieu MACD
#   duong co y nghia khac nhau trong che do bien dong thap va cao. Vi cay
#   quyet dinh chia khong gian dac trung theo tung vung, viec cung cap bien
#   bien dong cho phep mo hinh hoc quy tac CO DIEU KIEN theo che do — day la
#   dieu mo hinh tuyen tinh khong lam duoc.
#   Volatility clustering (Mandelbrot, ARCH) bao dam bien nay co tinh du bao.
#
# NHOM 4 — DAC TRUNG TRE (Lag): log-return tre 1, 2, 3 ngay
#   Nam bat cau truc tu tuong quan trong chuoi loi suat. Ly thuyet thi truong
#   hieu qua dang yeu du doan tu tuong quan ~ 0; do do do lon he so nay chinh
#   la thuoc do muc do KHONG hieu qua cua thi truong. Neu nhom nay co Gain
#   ap dao trong mo hinh, can kiem tra lai xem do la tin hieu that hay la
#   hien tuong nhan tao do xu ly du lieu (xem Chuong 4).
# ==========================================================
print("\n" + "=" * 80)
print("CHUONG 3. XAY DUNG TAP DAC TRUNG")
print("=" * 80)

# --- Nhom 1: Xu huong ---
df["MA10"] = df["Close"].rolling(10).mean()
df["MA30"] = df["Close"].rolling(30).mean()
df["MA50"] = df["Close"].rolling(50).mean()
df["EMA12"] = df["Close"].ewm(span=12, adjust=False).mean()
df["EMA26"] = df["Close"].ewm(span=26, adjust=False).mean()

df["MA10_MA30_diff"] = (df["MA10"] - df["MA30"]) / df["MA30"]
df["MA30_MA50_diff"] = (df["MA30"] - df["MA50"]) / df["MA50"]
df["EMA12_EMA26_diff"] = (df["EMA12"] - df["EMA26"]) / df["EMA26"]
df["price_MA10_dist"] = (df["Close"] - df["MA10"]) / df["MA10"]

# --- Nhom 2: Dong luong / dao dong ---
delta = df["Close"].diff()
avg_gain = delta.clip(lower=0).rolling(14).mean()
avg_loss = (-delta.clip(upper=0)).rolling(14).mean()
df["RSI14"] = 100 - 100 / (1 + avg_gain / avg_loss)

df["MACD"] = df["EMA12"] - df["EMA26"]
df["MACD_signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
df["MACD_hist"] = df["MACD"] - df["MACD_signal"]
# Chuan hoa MACD theo gia de so sanh duoc giua cac muc gia khac nhau
df["MACD_norm"] = df["MACD"] / df["Close"]
df["MACD_hist_norm"] = df["MACD_hist"] / df["Close"]

# --- Nhom 3: Do bien dong ---
bb_mid = df["Close"].rolling(20).mean()
bb_std = df["Close"].rolling(20).std()
df["BB_width"] = (4 * bb_std) / bb_mid          # do rong dai tuong doi
df["BB_pctB"] = (df["Close"] - (bb_mid - 2 * bb_std)) / (4 * bb_std)
df["volatility_20d"] = df["log_return"].rolling(20).std()
df["volume_ratio"] = df["Volume"] / df["Volume"].rolling(20).mean()

# --- Nhom 4: Dac trung tre ---
for lag in [1, 2, 3]:
    df[f"log_return_lag{lag}"] = df["log_return"].shift(lag)

FEATURES_TREND = ["MA10_MA30_diff", "MA30_MA50_diff", "EMA12_EMA26_diff",
                  "price_MA10_dist"]
FEATURES_MOMENTUM = ["RSI14", "MACD_norm", "MACD_hist_norm"]
FEATURES_VOLATILITY = ["BB_width", "BB_pctB", "volatility_20d", "volume_ratio"]
FEATURES_LAG = ["log_return_lag1", "log_return_lag2", "log_return_lag3"]
ALL_FEATURES = FEATURES_TREND + FEATURES_MOMENTUM + FEATURES_VOLATILITY + FEATURES_LAG

FEATURE_GROUPS = {
    "M1_XuHuong": FEATURES_TREND,
    "M2_+DongLuong": FEATURES_TREND + FEATURES_MOMENTUM,
    "M3_+BienDong": FEATURES_TREND + FEATURES_MOMENTUM + FEATURES_VOLATILITY,
    "M4_Full(+Tre)": ALL_FEATURES,
}

for g, f in FEATURE_GROUPS.items():
    print(f"  {g:<16} : {len(f)} dac trung")

# Loai bo cac dong khong day du (do rolling window va do shift(-1) o dong cuoi).
# CO SO LY LUAN: khong dung imputation cho chuoi thoi gian tai vung khoi dong
# vi moi gia tri thay the deu la thong tin bi bop meo; cat bo n dong dau
# (n = cua so dai nhat = 50) la cach xu ly trung thuc.
data = df.dropna(subset=ALL_FEATURES + ["target", "log_return"]).reset_index(drop=True)
print(f"\nSau khi loai NaN: {len(data)} quan sat "
      f"({data.Date.min().date()} -> {data.Date.max().date()})")
print(f"Ty le target UP: {data['target'].mean()*100:.2f}%")


# ==========================================================
# CHUONG 4. KIEM DINH CHAT LUONG DU LIEU
# ==========================================================
# CO SO LY LUAN: truoc khi dien giai bat ky ket qua du bao nao, phai kiem dinh
# xem cau truc du bao co nguon goc tu thi truong hay tu quy trinh xu ly du lieu.
# Ba phep kiem dinh chuan cho chuoi gia tai chinh:
#   (a) Ty le buoc gia trung lap: chuoi gia that gan nhu khong bao gio co hai
#       buoc nhay lien tiep bang nhau tuyet doi. Ty le cao => co noi suy.
#   (b) Tu tuong quan log-return: thi truong thanh khoan cao co |rho1| < 0.05.
#   (c) Phan bo ngay trong tuan: hop dong vang COMEX khong giao dich T7/CN.
# Ket qua duoc IN RA va PHAI duoc bao cao trong phan han che cua nghien cuu.
# ==========================================================
print("\n" + "=" * 80)
print("CHUONG 4. KIEM DINH CHAT LUONG DU LIEU (bat buoc bao cao)")
print("=" * 80)

_step = df["Close"].diff()
_dup_step = (_step.diff().abs() < 1e-6).mean() * 100
_r = df["log_return"].dropna()
_dow = df.Date.dt.dayofweek.value_counts().sort_index()
_weekend = int(_dow.reindex([5, 6]).fillna(0).sum())

print(f"(a) Ty le buoc gia trung buoc truoc : {_dup_step:.2f}%   [chuoi that ~0%]")
print(f"(b) Tu tuong quan log-return lag1   : {_r.autocorr(1):.4f}  [thi truong hieu qua ~0]")
print(f"    Tu tuong quan lag2               : {_r.autocorr(2):.4f}")
print(f"(c) So quan sat vao T7 + CN          : {_weekend}  [thi truong that = 0]")
print(f"    Ty le ngay UP                    : {(_r > 0).mean()*100:.2f}%  [vang ~52-53%]")

DATA_HAS_INTERPOLATION = (_dup_step > 5) or (_weekend > 0)
if DATA_HAS_INTERPOLATION:
    print("""
    >>> CANH BAO PHUONG PHAP LUAN <<<
    Du lieu chua dau hieu noi suy (interpolation) cac ngay khong giao dich.
    Gia tri ngay khong giao dich duoc suy ra tu gia cua ngay giao dich KE SAU,
    tuc la tu THONG TIN TUONG LAI. Hau qua: bien log_return_lag tro thanh bien
    du bao gan nhu hoan hao trong cac doan noi suy, lam Accuracy/AUC bi phong
    dai va KHONG phan anh nang luc du bao thuc te tren thi truong.
    Ket qua duoi day phai duoc dien giai kem han che nay.
    """)


# ==========================================================
# CHUONG 5. HUAN LUYEN WALK-FORWARD
# ==========================================================
# CO SO LY LUAN:
# (1) KHONG dung K-Fold Cross-Validation ngau nhien. Voi chuoi thoi gian,
#     tron ngau nhien khien tap huan luyen chua quan sat xay ra SAU tap kiem
#     dinh => look-ahead bias, ket qua bi phong dai mot cach he thong.
# (2) Dung walk-forward (rolling origin) voi cua so mo rong: huan luyen tren
#     [0, t), du bao [t, t+h), roi mo rong tap huan luyen. Mo phong dung dieu
#     kien thuc te: tai moi thoi diem quyet dinh, nha giao dich chi co du lieu
#     qua khu.
# (3) Tai huan luyen dinh ky (moi ~1 nam) de mo hinh thich nghi voi concept
#     drift — phu hop Gia thuyet Thi truong Thich nghi (Lo, 2004): quan he
#     giua tin hieu va loi nhuan thay doi theo thoi gian.
# (4) scale_pos_weight xu ly mat can bang lop; regularization (max_depth thap,
#     reg_lambda, min_child_weight) chong overfit tren du lieu nhieu cao.
# ==========================================================
print("\n" + "=" * 80)
print("CHUONG 5. HUAN LUYEN WALK-FORWARD")
print("=" * 80)


def walk_forward_predict(dataset, features, initial_train=INITIAL_TRAIN,
                         retrain_every=RETRAIN_EVERY, verbose=False):
    """Huan luyen tren qua khu, du bao khoi tiep theo. Khong dung du lieu tuong lai."""
    proba = pd.Series(np.nan, index=dataset.index, dtype=float)
    last_model = None
    start = initial_train
    n_fold = 0
    while start < len(dataset):
        end = min(start + retrain_every, len(dataset))
        train = dataset.iloc[:start]
        test = dataset.iloc[start:end]

        n_pos = int((train["target"] == 1).sum())
        n_neg = int((train["target"] == 0).sum())

        model = XGBClassifier(
            n_estimators=200,
            max_depth=3,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_lambda=1.0,
            min_child_weight=5,
            scale_pos_weight=(n_neg / n_pos) if n_pos else 1.0,
            eval_metric="logloss",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )
        model.fit(train[features], train["target"])
        proba.iloc[start:end] = model.predict_proba(test[features])[:, 1]

        n_fold += 1
        if verbose:
            print(f"   Fold {n_fold}: train n={len(train):>5} -> "
                  f"test {test.Date.iloc[0].date()}..{test.Date.iloc[-1].date()} "
                  f"(n={len(test)})")
        last_model, start = model, end
    return proba, last_model


print(f"Tap huan luyen ban dau: {INITIAL_TRAIN} quan sat | "
      f"Tai huan luyen moi {RETRAIN_EVERY} quan sat")
data["ai_proba"], final_model = walk_forward_predict(
    data, ALL_FEATURES, verbose=True)

oos = data.dropna(subset=["ai_proba"]).copy().reset_index(drop=True)
print(f"\nGiai doan out-of-sample: {oos.Date.min().date()} -> {oos.Date.max().date()}"
      f"  ({len(oos)} quan sat)")

ai_pred = (oos["ai_proba"] > PROB_THRESHOLD).astype(int)
acc = accuracy_score(oos["target"], ai_pred)
f1 = f1_score(oos["target"], ai_pred)
auc = roc_auc_score(oos["target"], oos["ai_proba"])
baseline = max(oos["target"].mean(), 1 - oos["target"].mean())

print("\n--- Chat luong du bao (out-of-sample) ---")
print(f"Accuracy : {acc:.4f}")
print(f"F1-score : {f1:.4f}")
print(f"AUC      : {auc:.4f}")
print(f"Baseline (luon doan lop da so): {baseline:.4f}")
print(f"\n{classification_report(oos['target'], ai_pred, target_names=['DOWN', 'UP'])}")


# ==========================================================
# CHUONG 6. ABLATION STUDY
# ==========================================================
# CO SO LY LUAN: Feature Importance noi bo cua XGBoost chi cho biet mo hinh DA
# DUNG bien nao nhieu, khong cho biet bien do co CAI THIEN nang luc du bao
# ngoai mau hay khong (mot bien nhieu van co Gain duong do overfit). Ablation
# study — huan luyen lai tu dau voi tung tap con dac trung va so sanh hieu nang
# out-of-sample — la thiet ke nhan qua dung de dinh luong dong gop bien.
# Ta cong don theo tung nhom de doc duoc "gia tri gia tang" cua moi nhom.
# ==========================================================
print("\n" + "=" * 80)
print("CHUONG 6. ABLATION STUDY — DONG GOP TUNG NHOM DAC TRUNG")
print("=" * 80)

ablation = {}
for gname, gfeats in FEATURE_GROUPS.items():
    p, _ = walk_forward_predict(data, gfeats)
    sub = data.dropna(subset=["ai_proba"]).copy()
    p_oos = p.loc[sub.index]
    pred = (p_oos > PROB_THRESHOLD).astype(int)
    ablation[gname] = {
        "n_features": len(gfeats),
        "Accuracy": accuracy_score(sub["target"], pred),
        "F1": f1_score(sub["target"], pred),
        "AUC": roc_auc_score(sub["target"], p_oos),
    }
    print(f"  {gname:<16} n={len(gfeats):>2} | "
          f"Acc={ablation[gname]['Accuracy']:.4f} | "
          f"F1={ablation[gname]['F1']:.4f} | AUC={ablation[gname]['AUC']:.4f}")

ablation_df = pd.DataFrame(ablation).T
ablation_df["AUC_gia_tang"] = ablation_df["AUC"].diff()
print(f"\n{ablation_df.round(4).to_string()}")
ablation_df.to_csv(f"ablation{SUFFIX}.csv")


# ==========================================================
# CHUONG 7. XAY DUNG VI THE CAC CHIEN LUOC
# ==========================================================
# CO SO LY LUAN VE QUY UOC THUC THI (rat quan trong cho tinh trung thuc):
#   Tin hieu tai ngay t duoc tinh tu thong tin den HET ngay t (gia dong cua t).
#   Vi the mo tai gia dong cua t va nam giu suot ngay t+1.
#   => Loi nhuan chien luoc: r_strat[t] = position[t-1] * log_return[t]
#   Neu dung position[t] * log_return[t] thi tin hieu se "biet truoc" loi nhuan
#   cung ky => look-ahead bias, ket qua backtest vo nghia.
#
# CO SO LY LUAN CAC CHIEN LUOC TIN HIEU KY THUAT (benchmark truyen thong):
#   - MA Crossover (MA10 vs MA30): dai dien truong phai THEO XU HUONG
#     (trend-following). Gia thuyet: xu huong co quan tinh (momentum).
#   - MACD Crossover: theo xu huong nhung phan ung nhanh hon nho dung EMA.
#   - RSI (30/70): dai dien truong phai HOI QUY VE TRUNG BINH
#     (mean-reversion). Gia thuyet: gia bi day qua xa se quay lai.
#   - Combined: yeu cau hai tin hieu doc lap cung xac nhan => giam tin hieu
#     gia (false signal), doi lai giam so co hoi.
#   Chon du ca hai truong phai doi lap de phep so sanh voi AI la cong bang.
#
#   - Buy & Hold: benchmark bat buoc. Neu mot chien luoc chu dong khong vuot
#     duoc Buy & Hold sau chi phi, no khong tao ra gia tri kinh te.
# ==========================================================
print("\n" + "=" * 80)
print("CHUONG 7. XAY DUNG VI THE CAC CHIEN LUOC")
print("=" * 80)

positions = pd.DataFrame(index=oos.index)
positions["BuyHold"] = 1.0
positions["TA_MA_Crossover"] = (oos["MA10"] > oos["MA30"]).astype(float)
positions["TA_MACD"] = (oos["MACD"] > oos["MACD_signal"]).astype(float)

# RSI mean-reversion: vao khi RSI<30, thoat khi RSI>70 (may trang thai)
_pos, _hold = [], 0.0
for v in oos["RSI14"].values:
    if _hold == 0.0 and v < 30:
        _hold = 1.0
    elif _hold == 1.0 and v > 70:
        _hold = 0.0
    _pos.append(_hold)
positions["TA_RSI"] = _pos

positions["TA_Combined"] = ((oos["MA10"] > oos["MA30"]) &
                            (oos["MACD"] > oos["MACD_signal"])).astype(float)
positions["AI_XGB_LongFlat"] = (oos["ai_proba"] > PROB_THRESHOLD).astype(float)
positions["AI_XGB_LongShort"] = np.where(oos["ai_proba"] > PROB_THRESHOLD, 1.0, -1.0)

# Bien the co bo loc do tin cay: chi giao dich khi mo hinh du tu tin.
# CO SO LY LUAN: voi xac suat gan 0.5, ky vong loi nhuan khong du bu chi phi
# giao dich. Loc theo do tin cay lam giam turnover => giam ma sat chi phi.
positions["AI_XGB_Conf60"] = np.where(oos["ai_proba"] > 0.60, 1.0, 0.0)

for c in positions.columns:
    print(f"  {c:<20} ty le thoi gian co vi the: "
          f"{(positions[c] != 0).mean()*100:5.1f}%")


# ==========================================================
# CHUONG 8. BACKTEST & DO LUONG HIEU QUA
# ==========================================================
# CO SO LY LUAN CAC CHI TIEU:
#   - Total Return / CAGR: do luong loi nhuan. CAGR chuan hoa theo thoi gian.
#   - Ann. Volatility: do luong rui ro tong the (do lech chuan loi suat).
#   - Sharpe Ratio = (E[r] - rf) / sigma(r) * sqrt(P): loi nhuan tren mot don vi
#     rui ro tong. Day la thuoc do hieu qua dieu chinh rui ro pho bien nhat.
#     Han che: phat ca bien dong tang (upside), gia dinh loi suat gan chuan.
#   - Sortino Ratio: chi phat bien dong GIAM (downside deviation). Phu hop hon
#     voi cam nhan rui ro thuc te cua nha dau tu (chi so lo, khong so lai).
#   - Max Drawdown: muc sut giam toi da tu dinh. Do luong rui ro DUOI DANG
#     TRAI NGHIEM — quyet dinh kha nang nha giao dich tru lai voi chien luoc.
#   - Calmar = CAGR / |MaxDD|: loi nhuan tren mot don vi rui ro sut giam.
#   - Win Rate, So lenh, Turnover: do dac tinh van hanh va ma sat chi phi.
#   Dung dong thoi nhieu chi tieu vi khong mot chi tieu nao du: mot chien luoc
#   co the co Sharpe cao nhung MaxDD khong the chap nhan duoc.
#
#   Chi phi giao dich: tinh theo |thay doi vi the| x COST_BPS. Bo qua chi phi
#   la loi pho bien nhat lam backtest sai — dac biet voi chien luoc AI co
#   turnover cao.
# ==========================================================
print("\n" + "=" * 80)
print("CHUONG 8. BACKTEST & DO LUONG HIEU QUA")
print("=" * 80)


def backtest(position, log_return, cost_bps=COST_BPS):
    """Tra ve chuoi log-return rong cua chien luoc va turnover."""
    pos = position.astype(float)
    gross = pos.shift(1) * log_return               # vi the t-1 an return t
    turnover = pos.diff().abs()
    turnover.iloc[0] = abs(pos.iloc[0])             # chi phi mo vi the ban dau
    cost = (turnover * cost_bps / 10000.0).shift(1)
    net = (gross - cost).fillna(0.0)
    return net, turnover


def compute_metrics(net_log, turnover, periods=PERIODS_PER_YEAR):
    simple = np.expm1(net_log)
    equity = np.exp(net_log.cumsum())
    n = len(net_log)

    total_ret = equity.iloc[-1] - 1
    cagr = equity.iloc[-1] ** (periods / n) - 1
    vol = simple.std() * np.sqrt(periods)
    sharpe = simple.mean() / simple.std() * np.sqrt(periods) if simple.std() > 0 else np.nan
    dstd = simple[simple < 0].std()
    sortino = simple.mean() / dstd * np.sqrt(periods) if dstd and dstd > 0 else np.nan

    dd = equity / equity.cummax() - 1
    mdd = dd.min()
    calmar = cagr / abs(mdd) if mdd < 0 else np.nan

    active = simple[net_log != 0]
    return {
        "Total_Return": total_ret,
        "CAGR": cagr,
        "Ann_Vol": vol,
        "Sharpe": sharpe,
        "Sortino": sortino,
        "Max_Drawdown": mdd,
        "Calmar": calmar,
        "Win_Rate": (active > 0).mean() if len(active) else np.nan,
        "N_Trades": int((turnover > 0).sum()),
        "Turnover_Yr": turnover.sum() / (n / periods),
    }, equity, dd


log_ret = oos["log_return"]
results, equities, drawdowns, net_returns = {}, {}, {}, {}
for name in positions.columns:
    net, tno = backtest(positions[name], log_ret)
    m, eq, dd = compute_metrics(net, tno)
    results[name], equities[name], drawdowns[name], net_returns[name] = m, eq, dd, net

res_df = pd.DataFrame(results).T
res_df = res_df[["Total_Return", "CAGR", "Ann_Vol", "Sharpe", "Sortino",
                 "Max_Drawdown", "Calmar", "Win_Rate", "N_Trades", "Turnover_Yr"]]

show = res_df.copy()
for c in ["Total_Return", "CAGR", "Ann_Vol", "Max_Drawdown", "Win_Rate"]:
    show[c] = (show[c] * 100).round(2).astype(str) + "%"
for c in ["Sharpe", "Sortino", "Calmar", "Turnover_Yr"]:
    show[c] = show[c].round(3)
show["N_Trades"] = show["N_Trades"].astype(int)

print(f"He so quy doi nam: {PERIODS_PER_YEAR} | Chi phi: {COST_BPS} bps/lan")
print(f"Giai doan: {oos.Date.min().date()} -> {oos.Date.max().date()}\n")
print(show.to_string())
res_df.to_csv(f"ket_qua_so_sanh{SUFFIX}.csv")


# ==========================================================
# CHUONG 9. KIEM DINH TINH ON DINH
# ==========================================================
# CO SO LY LUAN: mot chien luoc co the dat Sharpe cao toan ky nho mot vai giai
# doan bat thuong. Tinh on dinh (robustness) doi hoi hieu nang duong deu qua
# cac nam. Ta do bang: (a) loi nhuan tung nam; (b) do lech chuan loi nhuan nam;
# (c) ty le nam co lai. Day la tieu chi thu ba trong muc tieu de tai.
# ==========================================================
print("\n" + "=" * 80)
print("CHUONG 9. KIEM DINH TINH ON DINH")
print("=" * 80)

years = oos["Date"].dt.year.values
yearly = {}
for name, net in net_returns.items():
    tmp = pd.DataFrame({"y": years, "r": net.values})
    yearly[name] = tmp.groupby("y")["r"].sum().apply(np.expm1) * 100
yearly_df = pd.DataFrame(yearly).round(2)
print("Loi nhuan theo nam (%):")
print(yearly_df.to_string())

stab = pd.DataFrame({
    "DoLechChuan_LN_Nam": yearly_df.std(),
    "TyLe_Nam_Co_Lai_%": (yearly_df > 0).mean() * 100,
    "Nam_Xau_Nhat_%": yearly_df.min(),
}).round(2).sort_values("DoLechChuan_LN_Nam")
print(f"\nChi tieu on dinh:\n{stab.to_string()}")
yearly_df.to_csv(f"loi_nhuan_theo_nam{SUFFIX}.csv")
stab.to_csv(f"chi_tieu_on_dinh{SUFFIX}.csv")


# ==========================================================
# CHUONG 10. DIEN GIAI MO HINH
# ==========================================================
# CO SO LY LUAN: mo hinh du bao trong tai chinh phai giai thich duoc moi co gia
# tri khoa hoc. Ta dung hai lop cong cu bo tro nhau:
#   - Gain Importance: tong muc giam ham mat mat do bien do dong gop khi duoc
#     chon lam diem chia. Cho biet MUC DO quan trong, khong cho biet CHIEU.
#   - SHAP (SHapley Additive exPlanations): phan ra du bao thanh tong dong gop
#     cua tung bien theo ly thuyet gia tri Shapley trong ly thuyet tro choi
#     hop tac. Uu diem: co tinh cong (additive), nhat quan, va cho biet CHIEU
#     tac dong cua tung bien tren tung quan sat.
# ==========================================================
print("\n" + "=" * 80)
print("CHUONG 10. DIEN GIAI MO HINH")
print("=" * 80)

gain = pd.Series(final_model.get_booster().get_score(importance_type="gain"))
gain = (gain / gain.sum() * 100).sort_values(ascending=False)
print("Feature Importance (Gain, % dong gop):")
print(gain.round(2).to_string())

group_of = {}
for f in FEATURES_TREND:
    group_of[f] = "1_XuHuong"
for f in FEATURES_MOMENTUM:
    group_of[f] = "2_DongLuong"
for f in FEATURES_VOLATILITY:
    group_of[f] = "3_BienDong"
for f in FEATURES_LAG:
    group_of[f] = "4_Tre"
grp_gain = gain.groupby(gain.index.map(group_of)).sum().sort_values(ascending=False)
print(f"\nTong Gain theo nhom (%):\n{grp_gain.round(2).to_string()}")
gain.to_csv(f"feature_importance{SUFFIX}.csv")

print("\nDang tinh SHAP values...")
X_oos = oos[ALL_FEATURES]
explainer = shap.TreeExplainer(final_model)
shap_values = explainer.shap_values(X_oos)


# ==========================================================
# CHUONG 11. TRUC QUAN HOA
# ==========================================================
print("\n" + "=" * 80)
print("CHUONG 11. TRUC QUAN HOA")
print("=" * 80)

STYLE = {
    "BuyHold": dict(color="black", ls="--", lw=2.0),
    "AI_XGB_LongFlat": dict(color="crimson", lw=2.4),
    "AI_XGB_LongShort": dict(color="darkred", lw=1.5, ls=":"),
    "AI_XGB_Conf60": dict(color="orange", lw=1.8),
}
dates = oos["Date"].values

# --- Hinh 1: Equity + Drawdown ---
fig, ax = plt.subplots(2, 1, figsize=(14, 10), sharex=True,
                       gridspec_kw={"height_ratios": [2, 1]})
for name, eq in equities.items():
    ax[0].plot(dates, eq.values, label=name, **STYLE.get(name, dict(lw=1.3, alpha=.85)))
ax[0].set_title("Equity Curve — AI-based vs Signal-based (out-of-sample, net of costs)",
                fontsize=13, fontweight="bold")
ax[0].set_ylabel("Gia tri tich luy (khoi diem 1.0)")
ax[0].legend(loc="upper left", fontsize=9)
ax[0].grid(alpha=.3)
for name, dd in drawdowns.items():
    ax[1].plot(dates, dd.values * 100, label=name, **STYLE.get(name, dict(lw=1.3, alpha=.85)))
ax[1].set_title("Drawdown (%)", fontsize=12, fontweight="bold")
ax[1].set_ylabel("Drawdown (%)")
ax[1].grid(alpha=.3)
plt.tight_layout()
plt.savefig(f"hinh1_equity_drawdown{SUFFIX}.png", dpi=130)
print(f"  hinh1_equity_drawdown{SUFFIX}.png")

# --- Hinh 2: Sharpe vs MaxDD ---
fig, ax = plt.subplots(figsize=(10, 7))
for name in res_df.index:
    x, y = abs(res_df.loc[name, "Max_Drawdown"]) * 100, res_df.loc[name, "Sharpe"]
    c = "crimson" if name.startswith("AI") else ("black" if name == "BuyHold" else "steelblue")
    ax.scatter(x, y, s=160, color=c, zorder=3, edgecolor="white", linewidth=1.5)
    ax.annotate(name, (x, y), textcoords="offset points", xytext=(9, 7), fontsize=9)
ax.axhline(0, color="gray", lw=.8)
ax.set_xlabel("Max Drawdown (%)  — cang nho cang tot")
ax.set_ylabel("Sharpe Ratio  — cang cao cang tot")
ax.set_title("Danh doi Loi nhuan / Rui ro\nAI (do) — Ky thuat (xanh) — Buy&Hold (den)",
             fontsize=12, fontweight="bold")
ax.grid(alpha=.3)
plt.tight_layout()
plt.savefig(f"hinh2_risk_return{SUFFIX}.png", dpi=130)
print(f"  hinh2_risk_return{SUFFIX}.png")

# --- Hinh 3: Loi nhuan theo nam ---
fig, ax = plt.subplots(figsize=(14, 6))
yearly_df.plot(kind="bar", ax=ax, width=.85)
ax.axhline(0, color="black", lw=.9)
ax.set_title("Tinh on dinh — Loi nhuan theo tung nam (%)", fontsize=12, fontweight="bold")
ax.set_ylabel("Loi nhuan (%)")
ax.set_xlabel("Nam")
ax.legend(fontsize=8, ncol=2)
ax.grid(alpha=.3, axis="y")
plt.tight_layout()
plt.savefig(f"hinh3_loi_nhuan_nam{SUFFIX}.png", dpi=130)
print(f"  hinh3_loi_nhuan_nam{SUFFIX}.png")

# --- Hinh 4: Ablation study ---
fig, ax = plt.subplots(1, 2, figsize=(14, 5))
ablation_df[["Accuracy", "F1", "AUC"]].plot(kind="bar", ax=ax[0], width=.8)
ax[0].axhline(.5, color="red", ls="--", lw=1, label="Nguong ngau nhien (0.5)")
ax[0].set_title("Ablation Study — hieu nang theo nhom dac trung", fontweight="bold")
ax[0].set_ylabel("Score")
ax[0].legend(fontsize=8)
ax[0].grid(alpha=.3, axis="y")
ax[0].tick_params(axis="x", rotation=20)
grp_gain.plot(kind="barh", ax=ax[1], color="teal")
ax[1].set_title("Tong Gain Importance theo nhom (%)", fontweight="bold")
ax[1].set_xlabel("% dong gop")
ax[1].grid(alpha=.3, axis="x")
plt.tight_layout()
plt.savefig(f"hinh4_ablation{SUFFIX}.png", dpi=130)
print(f"  hinh4_ablation{SUFFIX}.png")

# --- Hinh 5: SHAP summary ---
plt.figure()
shap.summary_plot(shap_values, X_oos, show=False, max_display=len(ALL_FEATURES))
plt.title("SHAP Summary — chieu va do lon tac dong cua tung dac trung",
          fontsize=11, fontweight="bold")
plt.tight_layout()
plt.savefig(f"hinh5_shap{SUFFIX}.png", dpi=130)
print(f"  hinh5_shap{SUFFIX}.png")

# --- Hinh 6: Confusion matrix ---
fig, ax = plt.subplots(figsize=(6, 5))
cm = confusion_matrix(oos["target"], ai_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
            xticklabels=["DOWN", "UP"], yticklabels=["DOWN", "UP"], ax=ax)
ax.set_title(f"Confusion Matrix — AI XGBoost (Acc={acc:.3f}, AUC={auc:.3f})",
             fontweight="bold")
ax.set_xlabel("Du bao")
ax.set_ylabel("Thuc te")
plt.tight_layout()
plt.savefig(f"hinh6_confusion_matrix{SUFFIX}.png", dpi=130)
print(f"  hinh6_confusion_matrix{SUFFIX}.png")

# ==========================================================
# TONG KET
# ==========================================================
print("\n" + "=" * 80)
print("TONG KET")
print("=" * 80)
best_sharpe = res_df["Sharpe"].idxmax()
best_dd = res_df["Max_Drawdown"].idxmax()
print(f"Chien luoc co Sharpe cao nhat   : {best_sharpe} ({res_df.loc[best_sharpe,'Sharpe']:.3f})")
print(f"Chien luoc co MaxDD nho nhat    : {best_dd} ({res_df.loc[best_dd,'Max_Drawdown']*100:.2f}%)")
print(f"Chien luoc on dinh nhat         : {stab.index[0]} "
      f"(std LN nam = {stab.iloc[0,0]:.2f}%)")
if DATA_HAS_INTERPOLATION:
    print("\n*** LUU Y: du lieu co dau hieu noi suy (Chuong 4). Cac chi so du bao")
    print("    (Accuracy/AUC) va hieu qua chien luoc AI bi phong dai. Phai bao cao")
    print("    han che nay khi dien giai ket qua. ***")
print("\n=== HOAN TAT ===")
