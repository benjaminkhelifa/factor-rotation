import yfinance as yf
import pandas as pd
import numpy as np
from tqdm import tqdm
import re
from datetime import timedelta

# --- Fenêtre d'affichage (saisie utilisateur)
tickers = [
    "SPY",     # US - S&P 500 ETF
    "QQQ",     # US - Nasdaq 100 ETF
    "ORA.PA",  # EU - Orange (France)
    "SAP.DE",  # EU - SAP (Germany)
    "7203.T",  # JP - Toyota (Japan)
    "6758.T"   # JP - Sony (Japan)
    ]
start_display = pd.Timestamp("2020-01-01")
end_display   = pd.Timestamp("2024-10-22")
interval = "1wk"

# --- Fenêtres CT “indicatives” selon la fréquence (mêmes bases que ton code)
if "d" in interval.lower():
    base_window = 20
elif "wk" in interval.lower():
    base_window = 4
elif "mo" in interval.lower():
    base_window = 3
else:
    base_window = 4

def back_business_days(start_date, n_days):
    """
    Recule de n jours ouvrés (business days), exactement comme Yahoo.
    """
    dates = pd.bdate_range(end=start_date, periods=n_days+1)  # +1 pour inclure start_date
    return dates[0]

def infer_freq_from_interval(interval: str):
    # Exemples d’inputs possibles : "1d", "5d", "1wk", "2mo", "3y"
    m = re.match(r"(\d+)([a-zA-Z]+)", interval.lower().strip())
    if not m:
        return "W"  # fallback
    num, unit = int(m.group(1)), m.group(2)
    if unit in ["d", "day", "days"]:
        return f"{num}B"      # business days
    elif unit in ["wk", "w", "week", "weeks"]:
        return f"{num}W"
    elif unit in ["mo", "m", "month", "months"]:
        return f"{num}M"
    elif unit in ["y", "yr", "year", "years"]:
        return f"{num}Y"
    else:
        return "W"
    
freq = infer_freq_from_interval(interval)
n_points = len(pd.date_range(start_display, end_display, freq=freq))


window_momentum= max(3, min(int(n_points * 0.30), base_window * 4))  # tendance persistante
window_momentum_L = int(window_momentum * 5)

# --- Conversion dynamique en nombre de jours à reculer (selon interval)
if "wk" in interval.lower():
    delta = timedelta(weeks=window_momentum_L)
elif "mo" in interval.lower():
    # approx 30 jours par mois
    delta = timedelta(days=30 * window_momentum_L)
elif "y" in interval.lower():
    delta = timedelta(days=365 * window_momentum_L)
else:
    delta = timedelta(weeks=window_momentum_L)

if "d" in interval.lower():  # DAILY / BUSINESS DAILY
    start_analysis = back_business_days(start_display, window_momentum_L)
else:
    start_analysis = start_display - delta

print(f"Fenêtre d'analyse ajustée automatiquement : au lieu de {start_display.date()} : {start_analysis.date()} → {end_display.date()}")

# --- Téléchargement avec fenêtre étendue
df = yf.download(
    tickers= tickers,
    start=start_analysis,
    end=end_display,
    interval=interval,
    group_by="ticker",
    progress=False
)

# --- Fusion & sauvegarde parquet
data = {}
for ticker in tickers:
    df_ticker = df[ticker].copy()
    df_ticker["Ticker"] = ticker
    data[ticker] = df_ticker

df_all = pd.concat(data.values())

# --- Réalignement temporel selon les vraies dates du DataFrame
idx = df_all.index.unique().sort_values()

start_display_real = idx[idx.get_indexer([start_display], method="nearest")[0]]
end_display_real   = idx[idx.get_indexer([end_display],   method="nearest")[0]]



df_all.attrs["start_display"] = str(start_display_real.date())
df_all.attrs["end_display"] = str(end_display_real.date())
df_all.to_parquet("/Users/benjaminvissac/Documents/GitHub/factor-rotation/data/processed/sectors.parquet")
df_all.to_csv("/Users/benjaminvissac/Documents/GitHub/factor-rotation/data/processed/sectors.csv")
print(df_all.isna().mean().sort_values(ascending=False) * 100)
print(f"✅ Données téléchargées ({len(df_all)} lignes) avec extension automatique pour les indicateurs LT.")
# --- Vérification finale des fenêtres utilisées
print("\n🧭 Vérification des fenêtres avant sauvegarde @     :")
print(f"   📈 Fenêtre d’analyse choisie : {start_analysis.date()} → {end_display.date()}")
print(f"   👁️  Fenêtre d’observation réelle (Yahoo) : {df_all.attrs['start_display']} → {df_all.attrs['end_display']}")
print(f"   🧮 Intervalle utilisé : {interval}")
print(f"   💾 Fichier parquet sauvegardé avec {len(df_all):,} lignes\n")
# ============================================================
# 2️⃣ Volatility profiles (long vs short term) — yfinance-driven
# ============================================================

# ---------- Paramètres ----------
LOOKBACK_FULL = "1y"   # historique pour vol LT
SHORT_DAYS    = 63     # ~3 mois (21 j × 3) pour vol CT
MIN_OBS       = 30     # minimum d'observations pour considérer les vols "utilisables"

# ---------- Utilitaires ----------
def _to_scalar(x):
    """Convertit en float scalaire si possible, sinon NaN."""
    try:
        if isinstance(x, (pd.Series, pd.DataFrame, np.ndarray)):
            x = np.array(x).squeeze()
            if isinstance(x, (np.ndarray, list)) and len(np.atleast_1d(x)) == 1:
                x = x.item()
        return float(x)
    except Exception:
        return np.nan

def _now_iso():
    try:
        return pd.Timestamp.utcnow().strftime("%Y-%m-%d")
    except Exception:
        return ""

# ---------- Snapshot yfinance (type, mcap, adv10, beta, nom) ----------
def get_asset_snapshot(ticker: str):
    """
    Récupère depuis yfinance:
      - quoteType / market → Asset_Type
      - marketCap
      - averageDailyVolume10Day (ADV10)
      - beta
      - shortName/longName (pour détecter éventuellement un ETF levier)
    """
    asset_type = "unknown"
    market_cap = np.nan
    adv10      = np.nan
    beta       = np.nan
    short_name = ""
    long_name  = ""

    try:
        t = yf.Ticker(ticker)

        # .info contient beta, marketCap, averageDailyVolume10Day, quoteType, market, shortName/longName
        info = {}
        try:
            info = t.info or {}
        except Exception:
            info = {}

        # Asset type
        quote_type = str(info.get("quoteType", "")).lower()
        market     = str(info.get("market", "")).lower()

        if "crypto" in quote_type or "crypto" in market:
            asset_type = "crypto"
        elif "etf" in quote_type:
            asset_type = "etf"
        elif "index" in quote_type:
            asset_type = "index"
        elif "equity" in quote_type or "stock" in quote_type:
            asset_type = "stock"
        elif "mutualfund" in quote_type:
            asset_type = "mutual_fund"
        elif "commodity" in quote_type or "future" in quote_type:
            asset_type = "commodity"
        elif "currency" in quote_type or "forex" in market:
            asset_type = "forex"
        elif "bond" in quote_type or "fixedincome" in quote_type:
            asset_type = "bond"
        elif "fund" in quote_type:
            asset_type = "fund"
        else:
            asset_type = "unknown"

        # Market cap, ADV10, Beta
        market_cap = _to_scalar(info.get("marketCap"))
        adv10      = _to_scalar(info.get("averageDailyVolume10Day"))
        beta       = _to_scalar(info.get("beta"))

        short_name = str(info.get("shortName", "") or "")
        long_name  = str(info.get("longName", "") or "")

        # Si ADV10 absent → fallback calculé (moyenne $ sur 10 jours)
        if not np.isfinite(adv10):
            try:
                hist = yf.download(ticker, period="30d", interval="1d",
                                   auto_adjust=True, progress=False)
                if not hist.empty and "Close" in hist and "Volume" in hist:
                    dv = (hist["Close"] * hist["Volume"]).dropna()
                    adv10 = _to_scalar(dv.tail(10).mean())
            except Exception:
                pass

    except Exception:
        # on laisse les NaN / unknown
        pass

    return {
        "asset_type": asset_type,
        "market_cap": market_cap,
        "adv10": adv10,
        "beta": beta,
        "short_name": short_name,
        "long_name": long_name
    }

def is_forex(ticker: str) -> bool:
    if not isinstance(ticker, str):
        return False
    
    t = ticker.upper().strip()

    # Structural rule: FX pairs = 6 letters + "=X"
    if t.endswith("=X") and len(t.replace("=X", "")) == 6:
        return True
    
    return False

def name_forex(t):
    if t.endswith("=X") and len(t) == 8:
        return t[:-2]
    return t

# ---------- Volatilités CT/LT (prix 1d, auto_adjust pour éviter les ruptures) ----------
def compute_vols_from_single_download(ticker: str):
    """
    Renvoie:
      - vol_long (% ann.)
      - vol_short (% ann.)
      - obs_full (# ret)
      - obs_short (# ret CT)
    """
    try:
        data = yf.download(ticker, period=LOOKBACK_FULL, interval="1d",
                           auto_adjust=True, progress=False)
        if data.empty or "Close" not in data:
            return np.nan, np.nan, 0, 0

        log_ret = np.log(data["Close"] / data["Close"].shift(1)).dropna()
        obs_full = int(log_ret.shape[0])
        if obs_full < MIN_OBS:
            return np.nan, np.nan, obs_full, 0

        vol_long = _to_scalar(log_ret.std() * np.sqrt(252) * 100)
        last_ct = log_ret.tail(SHORT_DAYS)
        vol_short = _to_scalar(last_ct.std() * np.sqrt(252) * 100)
        obs_short = int(last_ct.shape[0])

        return vol_long, vol_short, obs_full, obs_short
    except Exception:
        return np.nan, np.nan, 0, 0

# ---------- Classifications qualitatives ----------
# Seuils profil de volatilité selon Asset Type
VOL_THRESHOLDS = {
    "index":     [10, 20, 30],
    "etf":       [10, 20, 30],
    "stock":     [15, 25, 35],
    "crypto":    [40, 70, 100],
    "commodity": [12, 22, 32],
    "bond":      [5, 10, 15],
    "forex":     [3, 6, 9],
    "mutual_fund": [8, 15, 22],
    "fund":      [8, 15, 22],
    "unknown":   [15, 25, 35],
}
BENCHMARKS = {
    "stock": "SPY",          # actions US → marché global
    "etf": "SPY",            # ETF sectoriels → marché global
    "crypto": "BTC-USD",     # crypto → Bitcoin comme proxy du marché crypto
    "commodity": "DBC",      # matières premières → ETF broad commodity
    "bond": "IEF",           # obligations → Treasury 7-10Y
    "forex": "UUP",          # dollar index ETF
    "index": "SPY",          # indices généraux → benchmark global
    "mutual_fund": "SPY",
    "fund": "SPY",
    "unknown": None
}


    

def classify_profile(vol_long: float, asset_type: str = "stock") -> str:
    if not np.isfinite(vol_long):
        return "balanced"
    cuts = VOL_THRESHOLDS.get(asset_type, VOL_THRESHOLDS["unknown"])
    if vol_long < cuts[0]:
        return "defensive"
    elif vol_long < cuts[1]:
        return "balanced"
    elif vol_long < cuts[2]:
        return "dynamic"
    else:
        return "speculative"

def classify_regime(vol_short: float, vol_long: float) -> str:
    if not np.isfinite(vol_short) or not np.isfinite(vol_long) or vol_long <= 0:
        return "unknown"
    ratio = vol_short / vol_long
    if ratio < 0.75:
        return "subdued"
    elif ratio < 1.1:
        return "normal"
    elif ratio < 1.5:
        return "elevated"
    else:
        return "turbulent"

def classify_market_cap(mcap: float) -> str:
    if not np.isfinite(mcap):
        return "unknown"
    if mcap < 2e9:
        return "small"
    elif mcap < 10e9:
        return "mid"
    elif mcap < 200e9:
        return "large"
    else:
        return "mega"

def classify_liquidity(adv10_usd: float, market_cap_label: str = None) -> str:
    if not np.isfinite(adv10_usd):
        return "unknown"

    cap = (market_cap_label or "").lower()

    if cap in {"small"}:
        if adv10_usd < 0.5e6: return "illiquid"
        elif adv10_usd < 5e6: return "thin"
        elif adv10_usd < 2e7: return "liquid"
        else: return "very_liquid"

    elif cap in {"mid"}:
        if adv10_usd < 1e6: return "illiquid"
        elif adv10_usd < 2e7: return "thin"
        elif adv10_usd < 1e8: return "liquid"
        else: return "very_liquid"

    elif cap in {"large", "mega"}:
        if adv10_usd < 5e6: return "illiquid"
        elif adv10_usd < 5e7: return "thin"
        elif adv10_usd < 2e8: return "liquid"
        else: return "very_liquid"

    else:
        # fallback générique si MarketCap inconnu
        if adv10_usd < 1e6:
            return "illiquid"
        elif adv10_usd < 2e7:
            return "thin"
        elif adv10_usd < 1e8:
            return "liquid"
        else:
            return "very_liquid"

def classify_beta(beta: float) -> str:
    if not np.isfinite(beta):
        return "unknown"
    
    abs_beta = abs(beta)

    if abs_beta < 0.8:
        return "defensive"
    elif abs_beta < 1.2:
        return "market"
    elif abs_beta < 1.8:
        return "high-beta"
    else:
        return "very_high-beta"

def detect_leverage(asset_type: str, short_name: str, long_name: str) -> str:
    """
    Détection simple d'ETF levier via le nom (heuristique).
    """
    text = f"{short_name} {long_name}".lower()
    if asset_type == "etf" and any(k in text for k in ["2x", "3x", "ultra", "ultrapro", "leveraged", "x2", "x3"]):
        return "levered"
    return "unlevered"


def compute_beta_proxy(ticker: str, benchmark: str, period="1y") -> float:
    """Calcule le bêta du ticker vs. un benchmark sur une période donnée."""
    try:
        if benchmark is None:
            return np.nan

        data = yf.download([ticker, benchmark], period=period, interval="1d", progress=False)
        if data.empty or ("Close" not in data):
            return np.nan

        close = data["Close"].dropna()
        if ticker not in close.columns or benchmark not in close.columns:
            return np.nan

        r_asset = close[ticker].pct_change().dropna()
        r_bench = close[benchmark].pct_change().dropna()
        if len(r_asset) < 30 or len(r_bench) < 30:
            return np.nan

        beta = np.cov(r_asset, r_bench)[0, 1] / np.var(r_bench)
        return round(beta, 2)

    except Exception:
        return np.nan
# ---------- Construction du parquet ----------
records = []
for ticker in tqdm(tickers, desc="Building volatility profiles (yfinance)"):
    # 1) snapshot infos
    snap = get_asset_snapshot(ticker)
    asset_type = snap["asset_type"]
    mcap = snap["market_cap"]
    adv10 = snap["adv10"]
    beta_raw = snap["beta"]
    beta = round(beta_raw, 2) if np.isfinite(beta_raw) else np.nan
    leverage_label = detect_leverage(asset_type, snap["short_name"], snap["long_name"])

    if np.isnan(beta) and asset_type in BENCHMARKS:
        benchmark = BENCHMARKS[asset_type]
        beta = compute_beta_proxy(ticker, benchmark)

    # 2) vols CT/LT
    vol_long, vol_short, obs_full, obs_short = compute_vols_from_single_download(ticker)
    vol_ratio = np.nan
    if np.isfinite(vol_long) and vol_long > 0 and np.isfinite(vol_short):
        vol_ratio = round(vol_short / vol_long, 3)

    # 3) étiquettes
    market_cap_label = classify_market_cap(mcap)
    liquidity_label  = classify_liquidity(adv10, market_cap_label)
    profile          = classify_profile(vol_long, asset_type)
    regime           = classify_regime(vol_short, vol_long)
    usable           = (liquidity_label in {"liquid", "very_liquid"})


    # 4) enregistrement
    records.append({
        "Ticker": name_forex(ticker),
        "Asset_Type": asset_type,
        "Market_Cap": mcap,
        "Market_Cap_Label": market_cap_label,
        "ADV10_USD": np.nan if is_forex(ticker) else adv10,
        "Liquidity_Label": "very_liquid" if is_forex(ticker) else liquidity_label,
        "Usable": True if is_forex(ticker) else bool(usable),
        "Leverage_Label": leverage_label,
        "Beta": beta,
        "Beta_Label": classify_beta(beta),
        "Volatility_Profile": profile,
        "Regime": regime,
        "Volatility_Long(%)": round(vol_long, 2) if np.isfinite(vol_long) else np.nan,
        "Volatility_Short(%)": round(vol_short, 2) if np.isfinite(vol_short) else np.nan,
        "Volatility_Ratio": vol_ratio,
        "Obs_Full": int(obs_full),
        "Obs_Short": int(obs_short),
        "AsOf": _now_iso(),
    })


    
df_profiles = pd.DataFrame(records)

df_profiles.to_parquet("/Users/benjaminvissac/Documents/GitHub/factor-rotation/data/processed/vol_profiles.parquet",index=False)
print(df_profiles.isna().mean().sort_values(ascending=False) * 100)


df_profiles.to_csv(
    "/Users/benjaminvissac/Documents/GitHub/factor-rotation/data/processed/vol_profiles.csv",
    index=False
)