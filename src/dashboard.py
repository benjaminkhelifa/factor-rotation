# =====================================================
# === IMPORTS & INITIAL SETTINGS
# =====================================================
import os
import re
import time
from datetime import date, datetime
from textwrap import fill

import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Image,
    Table,
    TableStyle,
    KeepTogether,
    LongTable,
    Spacer,
)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
REPORT_DIR = os.path.join(BASE_DIR, "report", "outputs")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

plt.style.use("seaborn-v0_8")
start_time = time.time()

def normalize_fx_ticker(t):
    return t[:-2] if isinstance(t, str) and t.endswith("=X") else t

def apply_floor(x, min_val=0.1):
    try:
        x = float(x)
    except:
        return x
    if abs(x) < min_val:
        return np.sign(x) * min_val if x != 0 else min_val
    return x

def format_profile_text(sentences):
    coverage, biases, structural, others = [], [], [], []
    seen = set()

    for s in sentences:
        text = s.lower()
        if text in seen:
            continue

        if any(k in text for k in [
            "coverage", "diversification", "concentrated", "single-sector",
            "broad diversification", "broad balance", "multi-balanced"
        ]):
            coverage.append(s)

        elif "bias" in text:
            biases.append(s)

        elif any(k in text for k in [
            "tilt", "liquidity", "etf", "reit", "adr", "leverage", "beta",
            "volatility", "barbell", "size distribution", "concentration risk",
            "upper-tier", "dominant", "mid-cap", "small-cap", "large-cap", "mega-cap"
        ]):
            structural.append(s)

        else:
            others.append(s)

        seen.add(text)

    def block(title, lines):
        if not lines:
            return ""
        joined = "<br/>".join([f"• {line}" for line in lines])
        return f"<b>{title}</b><br/>{joined}<br/><br/>"

    html = ""
    html += block("Macro coverage", coverage)
    html += block("Sectorial biases", biases)
    html += block("Structural properties", structural)
    if others:
        html += block("Additional comments", others)

    return html

# =====================================================
# === MACRO PROFILE COMMENT FUNCTION
# =====================================================

def horizon_terms(freq_label: str):
    f = (freq_label or "").lower()
    if f.startswith("year"):   return {"adj":"yearly","unit":"year","plural":"years"}
    if f.startswith("month"):  return {"adj":"monthly","unit":"month","plural":"months"}
    if f.startswith("week"):   return {"adj":"weekly","unit":"week","plural":"weeks"}
    if f.startswith("business"):  # ← tester avant daily
        return {"adj":"business-daily","unit":"business day","plural":"business days"}
    if f.startswith("daily"):
        return {"adj":"daily","unit":"day","plural":"days"}
    if f.startswith("every"):
        m = re.findall(r"\d+", f); n = int(m[0]) if m else 1
        return {"adj":f"every-{n}-days","unit":f"{n}-day","plural":f"{n} days"}
    return {"adj":"periodic","unit":"period","plural":"periods"}



def format_window_label(freq_label: str,
                        window_return: int, window_momentum: int, window_vol: int,
                        window_return_L: int, window_momentum_L: int, window_vol_L: int):
    """Affiche les fenêtres court et long terme avec un saut de ligne clair."""
    h = horizon_terms(freq_label)
    return (
        f"<b>Short term:</b> {window_vol} {h['plural']} volatility, "
        f"{window_return} {h['plural']} return, "
        f"{window_momentum} {h['plural']} momentum"
        "<br/>"
        f"<b>Long term:</b> {window_vol_L} {h['plural']} volatility, "
        f"{window_return_L} {h['plural']} return, "
        f"{window_momentum_L} {h['plural']} momentum"
    )

def macro_profile_comment(meta_used, profiles_df=None):

    sentences = []

    # =========================
    # A. Diversification
    # =========================
    all_sectors = {
        "Communication Services", "Consumer Discretionary", "Consumer Staples", "Energy",
        "Financials", "Health Care", "Industrials", "Information Technology",
        "Materials", "Real Estate", "Utilities"
    }

    n = len(meta_used["GICS Sector"].unique())
    if n == 1:
        sentences.append(
            f"Single-sector portfolio ({meta_used['GICS Sector'].iloc[0]}): full dependence on sector-specific dynamics."
        )
    elif n <= 3:
        sentences.append("Highly concentrated structure: limited diversification and sensitivity to one macro driver.")
    elif n <= 5:
        sentences.append("Partial coverage: several macro themes remain unrepresented.")
    elif n <= 8:
        sentences.append("Balanced diversification: exposure to most macroeconomic drivers.")
    elif n <= 10:
        sentences.append("Broad diversification: structure close to a market-wide benchmark.")
    else:
        sentences.append("Full macro coverage: all 11 major economic sectors are represented (complete coverage confirmed).")

    defensive = {"Consumer Staples", "Health Care", "Utilities"}
    cyclical = {"Consumer Discretionary", "Industrials", "Materials", "Energy", "Financials"}
    rate_sensitive = {"Financials", "Real Estate", "Utilities"}
    growth = {"Information Technology", "Communication Services", "Health Care"}
    inflation = {"Energy", "Materials"}

    present = set(meta_used["GICS Sector"].unique())
    missing = all_sectors - present
    
    if len(missing) == 0:
        pass
    elif len(missing) > 3:
        sentences.append("Significant sector gaps: broad portions of the economy remain uncovered.")
    else:
        if defensive & missing:
            sentences.append("No exposure to defensive sectors — performance may weaken in downturns.")
        if cyclical & missing:
            sentences.append("Limited exposure to cyclical sectors — resilience during expansions may be lower.")
        if rate_sensitive & missing:
            sentences.append("Minimal rate-sensitive exposure — lower sensitivity to monetary policy shifts.")
        if growth & missing:
            sentences.append("Underweight in technology and innovation sectors.")
        if inflation & missing:
            sentences.append("No inflation hedge: absence of commodity-related sectors.")

    # Bias
    if {"Information Technology", "Communication Services", "Consumer Discretionary"} <= present:
        sentences.append("Growth-oriented bias: portfolio sensitive to long-duration assets.")
    if {"Energy", "Materials", "Financials", "Industrials"} <= present:
        sentences.append("Cyclical bias: tilted toward economic expansion and inflation.")
    if {"Health Care", "Consumer Staples", "Utilities"} <= present:
        sentences.append("Defensive bias: stable positioning with lower beta to the market.")
    if {"Real Estate", "Utilities", "Financials"} <= present:
        sentences.append("Rate-sensitive bias: exposure to yield curve dynamics.")
    if {"Energy", "Materials"} <= present:
        sentences.append("Inflation-sensitive bias: protection against rising prices but higher volatility.")

    # =========================
    # for vol_profiles.parquet
    # =========================
    dfp = None
    if profiles_df is not None and not profiles_df.empty:
        tickers = set(meta_used["Symbol"].astype(str).unique())
        dfp = profiles_df.copy()
        if "Ticker" in dfp.columns:
            dfp = dfp.set_index("Ticker")
        dfp = dfp.loc[dfp.index.intersection(tickers)]

    # =========================
    # Market Cap Tilt 
    # =========================
    if dfp is not None and "Market_Cap_Label" in dfp.columns:
        cap = dfp["Market_Cap_Label"].dropna().str.lower().value_counts(normalize=True)
        mega  = cap.get("mega", 0)
        large = cap.get("large", 0)
        mid   = cap.get("mid", 0)
        small = cap.get("small", 0)
        micro = cap.get("micro", 0)

        shares = {"mega": mega, "large": large, "mid": mid, "small": small, "micro": micro}
        max_share = max(shares.values()) if shares else 0
        dominant = max(shares, key=shares.get) if shares else None

        # 1 Extreme Concentration
        if max_share >= 0.65:
            if dominant == "mega":
                msg = "Concentration risk: portfolio heavily dominated by mega caps, with limited diversification."
            elif dominant == "large":
                msg = "Concentration risk: strong bias toward large caps, stability achieved at the cost of diversity."
            elif dominant == "mid":
                msg = "Concentration risk: mid-cap dominance suggests moderate cyclicality and limited diversification."
            elif dominant in {"small", "micro"}:
                msg = "Concentration risk: portfolio highly exposed to small-cap volatility and idiosyncratic risk."
            sentences.append(msg)

        # 2 Mono-dominant (tilt)
        elif max_share >= 0.50:
            if dominant in {"mega", "large"}:
                msg = "Large/mega-cap tilt: quality and stability prioritized over idiosyncratic risk."
            elif dominant == "mid":
                msg = "Mid-cap tilt: balanced exposure combining quality and residual growth convexity."
            elif dominant in {"small", "micro"}:
                msg = "Small/micro-cap tilt: higher idiosyncratic risk with stronger convexity to cycles."
            sentences.append(msg)

        # 3 Multi-balanced (>= 3 sizes >= 20 %)
        elif sum(v >= 0.20 for v in shares.values()) >= 3:
            sentences.append("Broad balance across market capitalizations: diversification achieved across the size spectrum.")

        # 4 Duo-dominant (barbell)
        elif sum(v >= 0.30 for v in shares.values()) == 2:
            combo = [k for k, v in shares.items() if v >= 0.30]
            if set(combo) == {"mega", "large"}:
                msg = "Upper-tier focus: dominance of global and blue-chip leaders."
            elif set(combo) == {"mega", "mid"}:
                msg = "Barbell between mega leaders and mid-caps: blend of stability and growth leverage."
            elif set(combo) == {"mega", "small"} or set(combo) == {"mega", "micro"}:
                msg = "Barbell between mega and small caps: exposure across scale extremes."
            elif set(combo) == {"large", "mid"}:
                msg = "Barbell between large and mid-caps: balanced exposure to quality and cyclicality."
            elif set(combo) == {"large", "small"} or set(combo) == {"large", "micro"}:
                msg = "Barbell between large and small caps: dual exposure to stability and growth optionality."
            elif set(combo) == {"mid", "small"} or set(combo) == {"mid", "micro"}:
                msg = "Barbell between mid and small caps: moderate cyclicality with growth convexity."
            else:
                msg = f"Barbell structure between {combo[0]} and {combo[1]} caps."
            sentences.append(msg)

        else:
            sentences.append("Size distribution neutral: no dominant capitalization pattern detected.")

    # =========================
    # Asset Type Mix
    # =========================
    if dfp is not None and "Asset_Type" in dfp.columns:
        at = dfp["Asset_Type"].dropna().str.lower().value_counts(normalize=True)
        shares = at.to_dict()
        max_share = max(shares.values()) if shares else 0
        dominant = max(shares, key=shares.get) if shares else None

        # 1 Concentration 
        if max_share >= 0.65:
            msg = f"Concentration risk: portfolio heavily exposed to {dominant.replace('_',' ')} instruments."
            sentences.append(msg)

        # 2 Tilt dominant
        elif max_share >= 0.50:
            msg = f"{dominant.replace('_',' ').capitalize()} tilt: exposure primarily driven by {dominant.replace('_',' ')} dynamics."
            sentences.append(msg)

        # 3 Multi-asset balanced
        elif sum(v >= 0.15 for v in shares.values()) >= 3:
            sentences.append("Multi-asset balance achieved: portfolio diversified across major asset classes.")

        # 4 Barbell
        elif sum(v >= 0.25 for v in shares.values()) == 2:
            combo = [k for k, v in shares.items() if v >= 0.25]
            if set(combo) == {"equity", "bond"} or set(combo) == {"stock", "bond"}:
                msg = "Classic equity–bond barbell: balance between growth and income."
            elif set(combo) == {"equity", "commodity"} or set(combo) == {"stock", "commodity"}:
                msg = "Barbell between growth assets and real assets: blend of cyclical and inflation-hedging exposures."
            elif set(combo) == {"equity", "crypto"}:
                msg = "High-convexity barbell: traditional equities paired with speculative digital assets."
            elif set(combo) == {"bond", "commodity"}:
                msg = "Barbell between yield and real assets: mix of defensiveness and inflation protection."
            elif set(combo) == {"forex", "equity"}:
                msg = "Barbell between equity risk and currency exposure: partial macro hedge structure."
            else:
                msg = f"Dual-structure exposure: balanced mix of {combo[0]} and {combo[1]} instruments."
            sentences.append(msg)


        else:
            sentences.append("Heterogeneous asset-type mix: no dominant class detected.")
    
    # -- Liquidity posture
    liq_note = []
    liquid = thin = 0.0
    if dfp is not None and "Liquidity_Label" in dfp.columns:
        ll = dfp["Liquidity_Label"].dropna().str.lower().value_counts(normalize=True)
        liquid = ll.get("very_liquid", 0) + ll.get("liquid", 0)
        thin   = ll.get("thin", 0) + ll.get("illiquid", 0)

    # Cas 1: nette domination de la liquidité
    if liquid >= 0.60 and thin <= 0.25:
        liq_note.append("ample trading liquidity overall")
    elif thin >= 0.40:
        liq_note.append("pockets of thin/illiquid names")
    elif 0.25 < thin < 0.40 and 0.25 < liquid < 0.60:
        liq_note.append("mixed liquidity conditions across holdings")
    else:
        liq_note.append("neutral liquidity conditions overall")
    if dfp is not None and "ADV10_USD" in dfp.columns:
        med_adv = pd.to_numeric(dfp["ADV10_USD"], errors="coerce").median()
        if pd.notna(med_adv):
            if med_adv >= 1e7:
                liq_note.append("robust median dollar volume")
            elif med_adv <= 2e6:
                liq_note.append("limited median dollar volume")
    if liq_note:
        sentences.append("Liquidity stance: " + "; ".join(liq_note) + ".")

    # -- Leverage / Beta / Vol profile (qualificatifs)
    if dfp is not None and "Leverage_Label" in dfp.columns and (dfp["Leverage_Label"].str.lower() == "levered").any():
        sentences.append("Leverage present on some lines — monitor gap risk and path dependency.")
    if dfp is not None and "Beta_Label" in dfp.columns:
        b = dfp["Beta_Label"].dropna().str.lower().str.replace("_", "-", regex=False).value_counts(normalize=True)

        if (b.get("very-high-beta", 0) + b.get("high-beta", 0)) >= 0.50:
            sentences.append("High-beta tilt: stronger sensitivity to market swings.")
        elif b.get("defensive", 0) >= 0.50:
            sentences.append("Defensive beta tilt: lower systematic risk profile.")
        elif b.get("market", 0) >= 0.50:
            sentences.append("Market-neutral beta exposure: close alignment with index dynamics.")
        else:
            sentences.append("Mixed beta structure: diversified sensitivity across holdings.")
    if dfp is not None and "Volatility_Profile" in dfp.columns:
        vp = dfp["Volatility_Profile"].dropna().str.lower().value_counts(normalize=True)

        if (vp.get("speculative", 0) + vp.get("dynamic", 0)) >= 0.50:
            sentences.append("Volatility profile skewed to dynamic/speculative names.")
        elif vp.get("defensive", 0) >= 0.50:
            sentences.append("Low-volatility bias: portfolio tilted toward defensive or stable assets.")
        elif vp.get("balanced", 0) >= 0.50:
            sentences.append("Balanced volatility structure: risk evenly distributed across holdings.")
        else:
            sentences.append("Heterogeneous volatility mix: no dominant risk profile detected.")
    return format_profile_text(sentences)



# =====================================================
# === KPI LABELING & INTERPRETATION
# =====================================================

def label_return(R, freq_label: str, asset_type: str):
    # --------------------------
    # 1) Normalisation des inputs
    # --------------------------
    f = (freq_label or "").lower()
    a = (asset_type or "unknown").lower()

    try:
        m = float(R)
    except Exception:
        m = 0.0

    # Mapping large → tous les types possibles
    if a in ("equity", "stock"):
        a = "stock"
    elif a in ("currency", "forex"):
        a = "forex"
    elif a in ("mutualfund", "fund"):
        a = "fund"
    elif a in ("index"):
        a = "index"
    # crypto, etf, commodity, bond, unknown restent inchangés

    # --------------------------
    # 2) Seuils par asset type
    # --------------------------
    CUTS_MAP = {
        "forex": {
            # FX = très faible directionnalité → bandes étroites
            "daily":  (-0.40, -0.20, -0.05, 0.05, 0.20, 0.40),
            "week":   (-1.20, -0.60, -0.15, 0.15, 0.60, 1.20),
            "month":  (-3.00, -1.50, -0.40, 0.40, 1.50, 3.00),
            "year":   (-8.00, -3.00, -1.00, 1.00, 3.00, 8.00),
        },

        "bond": {
            # Obligations : faible vol mais direction réelle → bandes modérées
            "daily":  (-0.25, -0.10, -0.03, 0.03, 0.10, 0.25),
            "week":   (-0.80, -0.30, -0.10, 0.10, 0.30, 0.80),
            "month":  (-2.50, -0.90, -0.30, 0.30, 0.90, 2.50),
            "year":   (-6.00, -2.00, -0.80, 0.80, 2.00, 6.00),
        },

        "stock": {
            # Actions : vol élevée → fenêtres plus larges
            "daily":  (-1.50, -0.80, -0.20, 0.20, 0.80, 1.50),
            "week":   (-4.50, -2.00, -0.60, 0.60, 2.00, 4.50),
            "month":  (-12.0, -4.00, -1.50, 1.50, 4.00, 12.0),
            "year":   (-35.0, -12.0, -4.00, 4.00, 12.0, 35.0),
        },

        "index": {
            # Indices : lissé → moins volatil que actions individuelles
            "daily":  (-1.00, -0.40, -0.10, 0.10, 0.40, 1.00),
            "week":   (-3.00, -1.20, -0.40, 0.40, 1.20, 3.00),
            "month":  (-8.00, -3.00, -1.00, 1.00, 3.00, 8.00),
            "year":   (-25.0, -8.00, -3.00, 3.00, 8.00, 25.0),
        },

        "etf": {
            # Très proche des indices
            "daily":  (-1.00, -0.40, -0.10, 0.10, 0.40, 1.00),
            "week":   (-3.00, -1.20, -0.40, 0.40, 1.20, 3.00),
            "month":  (-8.00, -3.00, -1.00, 1.00, 3.00, 8.00),
            "year":   (-25.0, -8.00, -3.00, 3.00, 8.00, 25.0),
        },

        "commodity": {
            # Commodities : très volatiles → seuils larges
            "daily":  (-2.50, -1.20, -0.30, 0.30, 1.20, 2.50),
            "week":   (-7.00, -3.00, -1.00, 1.00, 3.00, 7.00),
            "month":  (-20.0, -7.00, -2.50, 2.50, 7.00, 20.0),
            "year":   (-60.0, -25.0, -8.00, 8.00, 25.0, 60.0),
        },

        "crypto": {
            # Crypto = univers à part → amplitudes extrêmes
            "daily":  (-8.00, -3.00, -1.00, 1.00, 3.00, 8.00),
            "week":   (-20.0, -8.00, -2.50, 2.50, 8.00, 20.0),
            "month":  (-50.0, -18.0, -5.00, 5.00, 18.0, 50.0),
            "year":   (-150.0, -50.0, -15.0, 15.0, 50.0, 150.0),
        },

        "fund": {
            # Fonds : très smooth → bandes étroites
            "daily":  (-0.20, -0.08, -0.02, 0.02, 0.08, 0.20),
            "week":   (-0.70, -0.25, -0.08, 0.08, 0.25, 0.70),
            "month":  (-2.00, -0.70, -0.20, 0.20, 0.70, 2.00),
            "year":   (-6.00, -2.00, -0.60, 0.60, 2.00, 6.00),
        },

        "unknown": {},
    }

    DEFAULT_CUTS = {
        "daily":  (-0.60, -0.25, -0.08, 0.08, 0.25, 0.60),
        "week":   (-1.80, -0.70, -0.20, 0.20, 0.70, 1.80),
        "month":  (-5.00, -1.80, -0.50, 0.50, 1.80, 5.00),
        "year":   (-15.0, -5.00, -1.50, 1.50, 5.00, 15.0),
    }

    # --------------------------
    # 3) Sélection freq
    # --------------------------
    if "daily" in f:
        key = "daily"
    elif "week" in f:
        key = "week"
    elif "month" in f:
        key = "month"
    elif "year" in f:
        key = "year"
    else:
        key = "daily"

    # --------------------------
    # 4) Récupération des cuts
    # --------------------------
    cuts = CUTS_MAP.get(a, {}).get(key, DEFAULT_CUTS[key])

    # --------------------------
    # 6) Classification finale
    # --------------------------
# 7 niveaux de classification
    if m <= cuts[0]:
        return "strongly negative"
    if m <= cuts[1]:
        return "negative"
    if m <= cuts[2]:
        return "neutral-"
    if m <= cuts[3]:
        return "neutral"
    if m <= cuts[4]:
        return "neutral+"
    if m <= cuts[5]:
        return "moderately positive"
    return "strong"

def label_by_percentiles(value, series, cuts):
    q = series.quantile([c/100 for c in cuts]).values
    if value <= q[0]:         return 0
    elif value <= q[1]:       return 1
    elif value <= q[2]:       return 2
    elif value <= q[3]:       return 3
    else:                     return 4

def label_momentum(value, series, freq_label):
    """Adapt momentum thresholds based on frequency context."""
    f = freq_label.lower()
    
    # Ajustement des seuils selon la volatilité typique du momentum
    if "daily" in f:
        cuts = (40, 70, 90, 97)
    elif "weekly" in f:
        cuts = (35, 65, 85, 95)
    elif "month" in f:
        cuts = (25, 55, 80, 90)
    elif "year" in f:
        cuts = (20, 50, 75, 85)
    else:
        cuts = (35, 65, 85, 95)

    q = series.quantile([c / 100 for c in cuts]).values
    if value <= q[0]:   return "bearish"
    elif value <= q[1]: return "neutral"
    elif value <= q[2]: return "bullish"
    elif value <= q[3]: return "accelerating"
    else:               return "accelerating+"

def kpi_labels(summary, freq_label):
    df_profiles = pd.read_parquet(os.path.join(DATA_DIR, "vol_profiles.parquet")).set_index("Ticker")

    R_series = summary["AvgReturn(%)"]
    M_series = summary["Momentum(%)"]
    V_series = summary["Volatility(%)"]

    R_val = float(np.nan_to_num(R_series.median(), nan=0.0))
    M_val = float(np.nan_to_num(M_series.median(), nan=0.0))
    V_val = float(np.nan_to_num(V_series.median(), nan=0.0))

    # --- Trouver un ticker de référence ---
    ticker_ref = summary.index[0]

    asset_type = (
        df_profiles.loc[ticker_ref, "Asset_Type"]
        if ticker_ref in df_profiles.index
        else "unknown"
    )

    # --- Appels corrects ---
    R_lab = label_return(R_val, freq_label, asset_type)
    M_lab = label_momentum(M_val, M_series, freq_label)

    # --- Vol label: on prend le mode des régimes importés (subdued/normal/elevated/turbulent)
    if "V_regime" in summary.columns:
        s = summary["V_regime"].dropna().astype(str).str.lower()
        V_lab = s.mode().iat[0] if not s.empty else "normal"
    else:
        # Fallback ultra-simple sur percentiles si jamais V_label n'est pas là
        v = V_series.dropna()
        if v.empty:
            V_lab = "normal"
        else:
            q25, q60, q85, q95 = np.percentile(v, [25, 60, 85, 95])
            if   V_val <= q25: V_lab = "low"
            elif V_val <= q60: V_lab = "normal"
            elif V_val <= q85: V_lab = "high"
            else:              V_lab = "extreme"

    return R_val, M_val, V_val, R_lab, M_lab, V_lab

def horizon_intro(H):
    mapping = {
        "daily": "During the session,",
        "business-daily": "During the trading day,",
        "weekly": "Over the past week,",
        "monthly": "This month,",
        "yearly": "Year-to-date,"
    }
    return mapping.get(H, f"Over the {H} period,")

def effective_horizon_description(freq_label, window_return, window_momentum, window_vol):
    f = freq_label.lower()
    unit = ("day" if "daily" in f else
            "business day" if "business" in f else
            "week" if "week" in f else
            "month" if "month" in f else
            "year")
    return (f"based on {window_return}-{unit} return, "
            f"{window_momentum}-{unit} momentum and "
            f"{window_vol}-{unit} rolling volatility")

def generate_commentary(row):
    R = float(row.get("AvgReturn(%)", 0) or 0)
    M = float(row.get("Momentum(%)", 0) or 0)
    stab = (row.get("Signal_Stability_Label") or "").lower()
    regime = (row.get("V_regime") or "").lower()
    liq = (row.get("Liquidity_Label") or "").lower()
    

    # ---- Lecture générale ----
    if R > 0.5 and M > 0.5:
        trend = "positive performance with solid momentum"
    elif R < -0.5 and M < -0.5:
        trend = "weak performance with negative momentum"
    elif R > 0.5 and M < 0:
        trend = "positive returns but fading momentum"
    elif R < 0 and M > 0:
        trend = "recovering momentum despite recent losses"
    else:
        trend = "mixed short-term dynamics"

    # ---- Volatilité / Régime ----
    if regime == "turbulent":
        vol = "high volatility — market stress visible"
    elif regime == "elevated":
        vol = "rising volatility — tension building"
    elif regime == "subdued":
        vol = "low volatility — calm market tone"
    else:
        vol = "normal volatility regime"

    # ---- Signal / Liquidité ----
    if stab in ["strong reversal"]:
        sig = "strong reversal forming, short-term momentum fully diverging from long-term trend"
    elif stab in ["weak reversal"]:
        sig = "early reversal signs, short-term momentum starting to diverge"
    elif stab in ["neutral"]:
        sig = "signal unclear or in transition"
    elif stab in ["mildly coherent"]:
        sig = "signal remains coherent, but with limited conviction"
    elif stab in ["strongly coherent"]:
        sig = "signal remains strongly coherent with long-term momentum"
    else:
        sig = "signal condition undefined"

    if liq in {"thin", "illiquid"}:
        liq_txt = "under limited liquidity"
    elif liq in {"very_liquid", "liquid"}:
        liq_txt = "with ample liquidity"
    else:
        liq_txt = "liquidity moderate"

    # ---- Synthèse ----
    return f"{trend}, {sig}, {vol}, {liq_txt}."

def interpret_ratios(row):
    df_profiles = pd.read_parquet(os.path.join(DATA_DIR, "vol_profiles.parquet")).set_index("Ticker")
    asset = df_profiles.loc[ticker, "Asset_Type"] if ticker in df_profiles.index else "unknown"
    beta_label = df_profiles.loc[ticker, "Beta"] if ticker in df_profiles.index else "unknown"
    liq_label = df_profiles.loc[ticker, "Liquidity_Label"] if ticker in df_profiles.index else "unknown"
    dR = row.get("ΔReturn(pp)", 0)
    mR = row.get("Momentum_Ratio", 1)
    vR = row.get("Volatility_Ratio", 1)
    beta = row.get("Beta", 1)
    adv = row.get("ADV10_USD", 0)
    m   = row.get("Momentum(%)", 0)
    mLT = row.get("Momentum_LT(%)", 0)

    # --- 1. ΔReturn interpretation ---
    if asset == "crypto":
        if dR > 8:      
            perf = "strong acceleration in returns"
        elif dR > 3:    
            perf = "acceleration in returns"
        elif dR < -8:   
            perf = "sharp deterioration in returns"
        elif dR < -3:   
            perf = "loss of momentum in returns"
        else:
            perf = "stable performance"

    elif asset in {"equity", "etf", "index", "fund", "mutualfund"}:
        if dR > 3:      
            perf = "strong acceleration in returns"
        elif dR > 1:    
            perf = "acceleration in returns"
        elif dR < -3:   
            perf = "sharp deterioration in returns"
        elif dR < -1:   
            perf = "loss of momentum in returns"
        else:
            perf = "stable performance"

    elif asset == "commodity":
        if dR > 5:      
            perf = "strong acceleration in returns"
        elif dR > 2:    
            perf = "acceleration in returns"
        elif dR < -5:   
            perf = "sharp deterioration in returns"
        elif dR < -2:   
            perf = "loss of momentum in returns"
        else:
            perf = "stable performance"

    elif asset in {"forex", "currency"}:
        if dR > 0.40:   
            perf = "strong acceleration in returns"
        elif dR > 0.15: 
            perf = "acceleration in returns"
        elif dR < -0.40:
            perf = "sharp deterioration in returns"
        elif dR < -0.15:
            perf = "loss of momentum in returns"
        else:
            perf = "stable performance"

    elif asset == "bond":
        if dR > 0.25:   
            perf = "strong acceleration in returns"
        elif dR > 0.10:
            perf = "acceleration in returns"
        elif dR < -0.25:
            perf = "sharp deterioration in returns"
        elif dR < -0.10:
            perf = "loss of momentum in returns"
        else:
            perf = "stable performance"

    else:
        # Fallback universel
        if dR > 2:      
            perf = "strong acceleration in returns"
        elif dR > 0.5:  
            perf = "acceleration in returns"
        elif dR < -2:   
            perf = "sharp deterioration in returns"
        elif dR < -0.5:
            perf = "loss of momentum in returns"
        else:
            perf = "stable performance"

    # --- 2. Momentum ratio interpretation ---

    if asset == "crypto":
        # Crypto = marché explosif → seuils plus larges
        if mR > 2.0:
            mom = "momentum surging"
        elif mR > 1.4:
            mom = "momentum strengthening"
        elif mR < 0.4:
            mom = "momentum collapsing"
        elif mR < 0.8:
            mom = "momentum fading"
        else:
            mom = "momentum stable"

    elif asset in {"equity", "etf", "index", "fund", "mutualfund"}:
        if mR > 1.6:
            mom = "momentum surging"
        elif mR > 1.25:
            mom = "momentum strengthening"
        elif mR < 0.5:
            if (m <= 0) and (mLT <= 0):
                mom = "momentum collapsing"
            else:
                mom = "momentum fading"
        elif mR < 0.85:
            mom = "momentum fading"
        else:
            mom = "momentum stable"

    elif asset == "commodity":
        if mR > 1.8:
            mom = "momentum surging"
        elif mR > 1.3:
            mom = "momentum strengthening"
        elif mR < 0.45:
            mom = "momentum collapsing"
        elif mR < 0.75:
            mom = "momentum fading"
        else:
            mom = "momentum stable"

    elif asset in {"forex", "currency"}:
        if mR > 1.25:
            mom = "momentum surging"
        elif mR > 1.05:
            mom = "momentum strengthening"
        elif mR < 0.6:
            mom = "momentum collapsing"
        elif mR < 0.9:
            mom = "momentum fading"
        else:
            mom = "momentum stable"

    elif asset == "bond":
        if mR > 1.15:
            mom = "momentum surging"
        elif mR > 1.05:
            mom = "momentum strengthening"
        elif mR < 0.7:
            mom = "momentum collapsing"
        elif mR < 0.9:
            mom = "momentum fading"
        else:
            mom = "momentum stable"

    else:
        if mR > 1.5:
            mom = "momentum surging"
        elif mR > 1.2:
            mom = "momentum strengthening"
        elif mR < 0.5:
            mom = "momentum collapsing"
        elif mR < 0.8:
            mom = "momentum fading"
        else:
            mom = "momentum stable"

# --- 3. Volatility ratio interpretation ---

    if asset == "crypto":
        if vR > 2.0:
            vol = "volatility spiking"
        elif vR > 1.4:
            vol = "volatility expanding"
        elif vR < 0.4:
            vol = "volatility collapsing"
        elif vR < 0.8:
            vol = "volatility compressing"
        else:
            vol = "volatility normalizing"

    elif asset in {"equity", "etf", "index", "fund", "mutualfund"}:
        if vR > 1.6:
            vol = "volatility spiking"
        elif vR > 1.2:
            vol = "volatility expanding"
        elif vR < 0.55:
            vol = "volatility collapsing"
        elif vR < 0.85:
            vol = "volatility compressing"
        else:
            vol = "volatility normalizing"

    elif asset == "commodity":
        if vR > 1.8:
            vol = "volatility spiking"
        elif vR > 1.3:
            vol = "volatility expanding"
        elif vR < 0.45:
            vol = "volatility collapsing"
        elif vR < 0.75:
            vol = "volatility compressing"
        else:
            vol = "volatility normalizing"

    elif asset in {"forex", "currency"}:
        if vR > 1.20:
            vol = "volatility spiking"
        elif vR > 1.05:
            vol = "volatility expanding"
        elif vR < 0.70:
            vol = "volatility collapsing"
        elif vR < 0.90:
            vol = "volatility compressing"
        else:
            vol = "volatility normalizing"

    elif asset == "bond":
        if vR > 1.10:
            vol = "volatility spiking"
        elif vR > 1.03:
            vol = "volatility expanding"
        elif vR < 0.85:
            vol = "volatility collapsing"
        elif vR < 0.95:
            vol = "volatility compressing"
        else:
            vol = "volatility normalizing"

    else:
        if vR > 1.5:
            vol = "volatility spiking"
        elif vR > 1.2:
            vol = "volatility expanding"
        elif vR < 0.5:
            vol = "volatility collapsing"
        elif vR < 0.8:
            vol = "volatility compressing"
        else:
            vol = "volatility normalizing"

    # --- 4. Beta commentary ---
    if beta_label > 1.2:
        beta_comment = "amplifying market trends"
    elif beta_label < 0.6:
        beta_comment = "within defensive profile"
    else:
        beta_comment = "aligned with market dynamics"

# --- 5. Liquidity commentary ---

    # 1) Cas spéciaux où ADV10 ne veut rien dire
    if asset in {"forex", "currency"}:
        adv_comment = "extremely liquid market (FX), volume not comparable to ADV10"
    elif pd.isna(adv):
        adv_comment = "liquidity unavailable or not applicable"
        
    # 2) Crypto
    elif asset == "crypto":
        # crypto volumes explosent mais très hétérogènes
        if adv > 200_000_000:
            adv_comment = "high liquidity for a crypto asset"
        elif adv > 50_000_000:
            adv_comment = "moderate liquidity for a crypto asset"
        else:
            adv_comment = "low liquidity for a crypto asset"

    # 3) Bonds / bond ETFs 
    if liq_label == "illiquid":
        adv_comment = "under illiquid trading conditions"
    elif liq_label == "thin":
        adv_comment = "under thin liquidity regime"
    elif liq_label in {"liquid", "very_liquid"}:
        adv_comment = "under robust trading volume"
    else:
        adv_comment = "with moderate liquidity"

    # --- 6. Synthèse finale ---
    return f"{perf}, {mom}, {vol}, {beta_comment}, {adv_comment}."

def format_adv10(x):
    if pd.isna(x):
        return "—"
    elif x >= 1e9:        # milliards
        return f"{x/1e9:.2f} B"
    elif x >= 1e6:        # millions
        return f"{x/1e6:.2f} M"
    elif x >= 1e3:        # milliers
        return f"{x/1e3:.1f} K"
    else:
        return f"{x:.0f}"

def colorize_number(x, base_style):
    try:
        val = float(x)
    except:
        return Paragraph(str(x), base_style)
    
    # Copie du style pour éviter de modifier l'original
    s = ParagraphStyle(name=f"{base_style.name}_{val}", parent=base_style)
    
    # --- Règles de couleur ---
    if val > 0:
        s.textColor = colors.HexColor("#006400")  # vert foncé
    elif val < 0:
        s.textColor = colors.HexColor("#B22222")  # rouge brique
    else:
        s.textColor = colors.black
    
    return Paragraph(f"{val:.2f}", s)




# =====================================================
# === INITIALIZATION 
# =====================================================


pie_buffer = io.BytesIO()

report_name = f"financial_report_{date.today().isoformat()}.pdf"


df_all = pd.read_parquet(os.path.join(DATA_DIR, "sectors.parquet"))
df_all["Ticker"] = df_all["Ticker"].map(normalize_fx_ticker)

# ==============================
# === GARDE-FOU NA ABSOLU    ===
# ==============================

print("\nRunning RAW NA integrity check...")

# 1. Ratios globaux
na_global = df_all.isna().mean() * 100
print("Global NA (%):")
print(na_global)

# 2. Ratios par ticker
na_by_ticker = (
    df_all
    .set_index("Ticker")  
    .groupby(level=0)
    .apply(lambda g: g.isna().mean() * 100)
)
print("\nNA by ticker (%):")
print(na_by_ticker)

# 3. Cas critique : ticker totalement vide → erreur immédiate
critically_empty = na_by_ticker[na_by_ticker["Close"] == 100].index.tolist()
if critically_empty:
    raise ValueError(
        f"FATAL DATA ERROR: The following tickers have 100% missing data "
        f"for 'Close' and cannot be processed: {critically_empty}"
    )

# 4. Cas partiellement critique : NA > 60% → avertissement + possibilité d’arrêt
high_na = na_by_ticker[na_by_ticker["Close"] > 60].index.tolist()
if high_na:
    print(
        f"\nWARNING: These tickers have more than 60% missing 'Close' data: {high_na}.\n"
        f"This may affect long-term momentum / volatility reliability."
    )

print("RAW NA integrity check passed.\n")

# 1. Vérifie que l'index est bien Date-like
if not isinstance(df_all.index, pd.DatetimeIndex):
    raise ValueError("parquet file should have DatetimeIndex in index (Date).")

# 2. On remet Date en colonne pour la suite du code
df_all = df_all.reset_index().rename(columns={"index": "Date"})
# (note : si l’index s'appelle déjà 'Date', rename ne change rien)

# 3. Conversion stricte
df_all["Date"] = pd.to_datetime(df_all["Date"], errors="raise")

# 4. Tri propre
df_all = df_all.sort_values(["Ticker", "Date"]).reset_index(drop=True)



start_display = pd.Timestamp(df_all.attrs.get("start_display", pd.NaT))
end_display   = pd.Timestamp(df_all.attrs.get("end_display",   pd.NaT))
if not (pd.notna(start_display) and pd.notna(end_display) and start_display <= end_display):
    raise ValueError("Window display does not exist")
if start_display not in df_all["Date"].values or end_display not in df_all["Date"].values:
    raise ValueError("Display window boundaries not found in dataset")

mask_display = df_all["Date"].between(start_display, end_display, inclusive="both")
dates_display = sorted(pd.to_datetime(df_all.loc[mask_display, "Date"].unique()))
di = pd.DatetimeIndex(dates_display)
n_points_disp = len(dates_display)

# Rendements sur données triées
df_all["log_ret"] = np.log(df_all["Close"] / df_all.groupby("Ticker")["Close"].shift(1))
df_all["Return"]  = df_all["log_ret"] * 100




freq = pd.infer_freq(di) if len(di) >= 3 else None

if freq is None:
    deltas = pd.Series(pd.to_datetime(dates_display)[1:] - pd.to_datetime(dates_display)[:-1]).dt.days
    med = int(deltas.median()) if len(deltas) else None
    if med is None:
        freq_label = "Unknown interval"
    elif med == 1: 
        freq_label = "Daily"
    elif 5 <= med <= 9:
        freq_label = "Weekly"
    elif 25 <= med <= 35:
        freq_label = "Monthly"
    elif 360 <= med <= 370:  
        freq_label = "Yearly"
    else:
        freq_label = f"every {med} days"
else:
    # Normalisation lisible des alias Pandas
    if freq.startswith(("A-", "AS-", "Y", "YS")):   
        freq_label = "Yearly"
    elif freq in ("D", "B"):                       
        freq_label = "Daily" if freq == "D" else "Business daily"
    elif freq.startswith(("W-", "W")):
        freq_label = "Weekly"
    elif freq.startswith(("M", "MS")):
        freq_label = "Monthly"
    else:
        freq_label = freq.lower()

# =====================================================
# === CHECK DATA DEPTH (for CT warning & LT activation)
# =====================================================
def check_data_depth(freq_label, n_points_disp):
    """Assess if short-term and long-term indicators are meaningful."""
    f = freq_label.lower()

    # Seuils par fréquence
    if "daily" in f:
        min_ct, min_lt = 30, 60
    elif "week" in f:
        min_ct, min_lt = 12, 30
    elif "month" in f:
        min_ct, min_lt = 6, 12
    elif "year" in f:
        min_ct, min_lt = 5, 8
    else:
        min_ct, min_lt = 30, 60 

    ct_ok = n_points_disp >= min_ct
    lt_ok = n_points_disp >= min_lt

    return ct_ok, lt_ok

# --- Exécution du contrôle
ct_ok, lt_ok = check_data_depth(freq_label, n_points_disp)
# =====================================================
# === AUTO-ADAPT ROLLING WINDOW SIZE TO DATA FREQUENCY & SAMPLE DEPTH
# =====================================================

freq_l = freq_label.lower()

# Fenêtre de base selon la fréquence
if "daily" in freq_l:
    base_window = 20
elif "business" in freq_l:
    base_window = 21
elif "weekly" in freq_l:
    base_window = 4
elif "month" in freq_l:
    base_window = 3
else:
    base_window = 4


# === Fenêtres distinctes et économiquement cohérentes ===
window_vol     = max(3, min(int(n_points_disp * 0.10), base_window * 2))  
window_return  = max(3, min(int(n_points_disp * 0.20), base_window * 3))  
window_momentum= max(3, min(int(n_points_disp * 0.30), base_window * 4))  
# === Fenêtres long terme (plus lisses) ===
window_vol_L      = int(window_vol * 2.5)
window_return_L   = int(window_return * 2)
window_momentum_L = int(window_momentum * 3)


# =====================================================
# === ADAPTIVE MOMENTUM COMPUTATION (context-aware)
# =====================================================

def compute_adaptive_momentum(df, freq_label, window_momentum, suffix=""):
    f = freq_label.lower()
    if   "daily"    in f or "business" in f: k_base = 252
    elif "weekly"   in f:                    k_base = 52
    elif "month"    in f:                    k_base = 12
    elif "year"     in f:                    k_base = 1
    else:                                    k_base = 52  # fallback

    col_raw = f"Momentum_raw{suffix}(%)"
    col_tot = f"TotalRet_window{suffix}(%)"
    col_m   = f"Momentum{suffix}(%)"

    if window_momentum <= 4:
        df[col_raw] = (
            df.groupby("Ticker")["Return"]
              .rolling(window_momentum, min_periods=window_momentum)
              .sum()
              .reset_index(level=0, drop=True)
        )
        df[col_tot] = (
            df.groupby("Ticker")["Return"]
              .rolling(window_momentum, min_periods=window_momentum)
              .apply(lambda x: np.expm1(np.log1p(x/100).sum())*100, raw=False)
              .reset_index(level=0, drop=True)
        )
    else:
        close = df["Close"]
        ref   = df.groupby("Ticker")["Close"].shift(window_momentum)
        df[col_raw] = (close.div(ref) - 1.0) * 100
        df[col_tot] = df[col_raw]

    # Normalisation par période
    df[col_m] = df[col_raw] / window_momentum

    return df



# === Application ===
df_all = compute_adaptive_momentum(df_all, freq_label, window_momentum)

# === Momentum long terme ===
df_all = compute_adaptive_momentum(df_all, freq_label, window_momentum_L, suffix="_LT")

# === Volatilité long terme ===
df_all["Volatility_LT(%)"] = (
    df_all.groupby("Ticker")["Return"]
          .rolling(window_vol_L, min_periods=window_vol_L)
          .std()
          .reset_index(level=0, drop=True)
)

# === Return long terme (composé) ===
df_all["Return_window_total_LT(%)"] = (
    df_all.groupby("Ticker")["Return"]
          .rolling(window_return_L, min_periods=window_return_L)
          .apply(lambda x: np.expm1(np.log1p(x/100).sum()) * 100, raw=False)
          .reset_index(level=0, drop=True)
)
# moyenne géométrique par période (LT)
df_all["Return_window_LT(%)"] = (
    ((1 + df_all["Return_window_total_LT(%)"]/100).clip(lower=1e-12) ** (1 / window_return_L) - 1) * 100
)


horizon = horizon_terms(freq_label)
window_label = format_window_label(
    freq_label,
    window_return, window_momentum, window_vol,
    window_return_L, window_momentum_L, window_vol_L
)

# =====================================================
# === NORMALISATION DES INDICATEURS (corrige l'effet d'échelle du window)
# =====================================================

# === Volatility (log-return based, per period, not annualized) ===
df_all["Volatility(%)"] = (
    df_all.groupby("Ticker")["Return"]   # Return already = log-return * 100
          .rolling(window_vol, min_periods=window_vol)
          .std()
          .reset_index(level=0, drop=True)
)

# =====================================================
# === SHORT-TERM RETURN (composé sur fenêtre dédiée)
# =====================================================

# Somme des log-returns sur la fenêtre
df_all["log_sum_w"] = (
    df_all.groupby("Ticker")["log_ret"]
          .rolling(window_return, min_periods=window_return)
          .sum()
          .reset_index(level=0, drop=True)
)

# Moyenne géométrique par période (non annualisée), en %
df_all["Return_window(%)"] = (np.exp(df_all["log_sum_w"] / window_return) - 1) * 100

# === Fenêtre d'affichage appliquée après les calculs ===
df_display = df_all.loc[mask_display].copy()
df_all.to_parquet(os.path.join(DATA_DIR, "df_all.parquet"))

# Calculer le nombre de tickers présnts dans le parquet 
corr_tickers = df_display["Ticker"].unique()
print("% de NA pour df_all (si présence pas grave car fenêtre d'analyse)")
print(df_all.isna().mean() * 100)
print("% de NA dans df_display (garder une vigilance si présence de NA car fenêtre d'observation)")
print(df_display.isna().mean() * 100)

# === Contrôle de qualité sur les indicateurs calculés ===

# Colonnes à contrôler (ST toujours, LT seulement si lt_ok)
cols_ct = [
    "Return", 
    "Volatility(%)", 
    "Momentum(%)", 
    "Return_window(%)",
]

cols_lt = []
if lt_ok:
    cols_lt = [
        "Volatility_LT(%)",
        "Momentum_LT(%)",
        "Return_window_LT(%)",
    ]

cols_to_check = [c for c in (cols_ct + cols_lt) if c in df_display.columns]

na_threshold = 0.34
na_ratios = df_display[cols_to_check].isna().mean()
bad_cols = na_ratios[na_ratios > na_threshold]

if not bad_cols.empty:
    msg = (
        "❌ Data integrity check failed:\n"
        + bad_cols.to_string(float_format=lambda x: f"{x:.1%}")
        + "\n→ Too many missing values (exceeds 34%)."
    )
    raise ValueError(msg)

# === Contrôle NA par ticker sur la dernière observation ===
required_cols_ct = ["Return", "Volatility(%)", "Momentum(%)", "Return_window(%)"]
required_cols_lt = ["Volatility_LT(%)", "Momentum_LT(%)", "Return_window_LT(%)"] if lt_ok else []

required_cols = [c for c in (required_cols_ct + required_cols_lt) if c in df_display.columns]

bad_tickers = []

for ticker, sub in df_display.groupby("Ticker"):
    last_row = sub.iloc[-1]
    na_cols = [c for c in required_cols if pd.isna(last_row.get(c))]
    if na_cols:
        bad_tickers.append((ticker, na_cols))

if bad_tickers:
    details = "\n".join(
        f"{t} → {', '.join(cols)}" for t, cols in bad_tickers
    )
    raise ValueError(
        "❌ Some tickers have incomplete indicators on the last observation:\n"
        + details
        + "\n→ Check data depth or remove these tickers from the request."
    )


def correlation_comment(corr_matrix):

    # --- Sécurité
    if corr_matrix.empty:
        return "Correlation matrix could not be computed due to missing data."

    #  Corrige le problème d’index nommé
    corr_matrix = corr_matrix.copy()
    corr_matrix.index.name = None
    corr_matrix.columns.name = None

    # --- Statistiques globales
    avg_corr = corr_matrix.replace(1.0, np.nan).mean().mean()  
    min_corr = corr_matrix.min().min()
    max_corr = corr_matrix[corr_matrix < 1].max().max()
    spread = max_corr - min_corr

    # --- Trouver les paires extrêmes
    stacked = corr_matrix.stack().reset_index()
    stacked.columns = ["Ticker1", "Ticker2", "Correlation"]
    stacked = stacked[stacked["Ticker1"] != stacked["Ticker2"]]
    top_pair = stacked.loc[stacked["Correlation"].idxmax()]
    bottom_pair = stacked.loc[stacked["Correlation"].idxmin()]

    # --- Lecture qualitative du niveau moyen
    if avg_corr < 0.1:
        insight = "very strong diversification — sectors move largely independently."
    elif avg_corr < 0.3:
        insight = "moderate diversification — some co-movement exists but remains limited."
    elif avg_corr < 0.6:
        insight = "elevated co-movement — diversification benefits are partially reduced."
    else:
        insight = "very high correlation — sectors behave almost as a single macro block."

    # --- Lecture de la dispersion
    if spread > 0.8:
        spread_note = "Correlation dispersion is wide, showing sharp contrasts between sectors."
    elif spread > 0.5:
        spread_note = "Correlation dispersion remains meaningful, indicating both tightly and weakly linked sectors."
    else:
        spread_note = "Correlation dispersion is narrow, suggesting similar risk dynamics across sectors."

    # --- Lecture des paires extrêmes
    pair_note = (
        f"Strongest co-movement between {top_pair['Ticker1']} and {top_pair['Ticker2']} "
        f"({top_pair['Correlation']:.2f}); weakest between "
        f"{bottom_pair['Ticker1']} and {bottom_pair['Ticker2']} "
        f"({bottom_pair['Correlation']:.2f})."
    )

    # --- Détection de régime global
    if avg_corr > 0.6:
        regime_note = "Market-driven regime: macro factors dominate individual sector dynamics."
    elif avg_corr < 0.2:
        regime_note = "Idiosyncratic regime: sector movements remain largely uncorrelated."
    else:
        regime_note = "Mixed regime: both market-wide and sector-specific forces are at play."

    # --- Texte final
    text = (
        f"Overall, average cross-sector correlation was {avg_corr:.2f}, "
        f"ranging from {min_corr:.2f} to {max_corr:.2f}. "
        f"This suggests {insight} {spread_note} {pair_note} {regime_note}"
    )

    return text



# =====================================================
# === SYNTHESIS TABLE (fenêtre + annualisation cohérente)
# =====================================================
def last_valid(x: pd.Series):
    x = x.dropna()
    return x.iloc[-1] if not x.empty else np.nan

summary = (
    df_display.groupby("Ticker").agg({
        "Return_window(%)":             last_valid,  
        "Volatility(%)":                last_valid,  
        "Momentum(%)":                  last_valid,  
        "Return_window_LT(%)":          last_valid,
        "Volatility_LT(%)":             last_valid,
        "Momentum_LT(%)":               last_valid,       
    })
)

# Appliquer aux long-term only
summary["Momentum_LT(%)"]   = summary["Momentum_LT(%)"].apply(lambda v: apply_floor(v, 0.1))
summary["Volatility_LT(%)"] = summary["Volatility_LT(%)"].apply(lambda v: apply_floor(v, 0.1))
summary["Return_window_LT(%)"] = summary["Return_window_LT(%)"].apply(lambda v: apply_floor(v, 0.1))

summary["Risk_Adjusted_return"] = (summary["Return_window(%)"] / summary["Volatility(%)"]).replace([np.inf, -np.inf], np.nan).round(3)
summary[["Return_window(%)","Volatility(%)","Momentum(%)"]] = summary[["Return_window(%)","Volatility(%)","Momentum(%)"]].round(2)

summary.rename(columns={
    "Return_window(%)":            "AvgReturn(%)",
    "Return_window_LT(%)":         "AvgReturn_LT(%)",
    "Momentum_LT(%)":              "Momentum_LT(%)"
}, inplace=True)



# =====================================================
# === VOLATILITY PROFILES IMPORT (from parquet)
# =====================================================
profiles_path = os.path.join(DATA_DIR, "vol_profiles.parquet")
# Lecture du parquet généré dans data.py
df_profiles = pd.read_parquet(profiles_path).set_index("Ticker")
df_profiles.index = df_profiles.index.map(normalize_fx_ticker)
# Jointure des informations de volatilité sur le tableau principal
summary = summary.join(df_profiles[["Volatility_Profile", "Regime",  "ADV10_USD", "Beta", "Beta_Label", "Liquidity_Label"]], how="left")

# Harmonisation des noms pour le reste du code
summary.rename(columns={
    "Volatility_Profile": "V_profile",   # defensive / balanced / dynamic / speculative
    "Regime":             "V_regime"     # subdued / normal / elevated / turbulent / unknown
}, inplace=True)

# Création des colonnes de labels (en minuscules pour la cohérence)
summary["V_regime"] = summary["V_regime"].fillna("unknown").str.lower()
summary["V_profile"] = summary["V_profile"].fillna("balanced").str.lower()


eps = 1e-6
summary["Signal_Stability"] = (
    (summary["Momentum(%)"] * summary["Momentum_LT(%)"]) /
    (abs(summary["Momentum_LT(%)"]) + abs(summary["Momentum(%)"]) + 1e-6)
).round(3)

def label_signal_stability(x):
    if x >= 0.6:
        return "strongly coherent"
    elif 0.2 <= x < 0.6:
        return "mildly coherent"
    elif -0.2 < x < 0.2:
        return "neutral"
    elif -0.6 < x <= -0.2:
        return "weak reversal"
    else:  # x <= -0.6
        return "strong reversal"

summary["Signal_Stability_Label"] = summary["Signal_Stability"].apply(label_signal_stability)

summary["Commentary"] = summary.apply(generate_commentary, axis=1)


summary["ΔReturn(pp)"] = (summary["AvgReturn(%)"] - summary["AvgReturn_LT(%)"]).round(2)
summary["Momentum_Ratio"] = (summary["Momentum(%)"] / summary["Momentum_LT(%)"]).round(2)
summary["Volatility_Ratio"] = (summary["Volatility(%)"] / summary["Volatility_LT(%)"]).round(2)
summary["Interpretation"] = summary.apply(interpret_ratios, axis=1)
summary["ADV10_Display"] = summary["ADV10_USD"].apply(format_adv10)

# ================================
# === CT SCENARIO ENGINE (full) ==
# ================================

def _ct_attach_profiles(summary: pd.DataFrame, profiles: pd.DataFrame) -> pd.DataFrame:
    s = summary.copy()
    if "Ticker" in s.columns:
        s = s.set_index("Ticker")
    want = [
        "Volatility_Profile","Regime","Asset_Type","Market_Cap_Label",
        "Liquidity_Label","Usable","Leverage_Label","Beta_Label"
    ]
    to_add = [c for c in want if c in profiles.columns and c not in s.columns]
    if to_add:
        s = s.join(profiles[to_add], how="left")
    return s

def _ct_label_momentum_abs(M, freq_label: str, asset_type: str):

    # --------------------------
    # 1) Normalisation des inputs
    # --------------------------
    f = (freq_label or "").lower()
    a = (asset_type or "unknown").lower()
    try:
        m = float(M)
    except Exception:
        m = 0.0

    # Mapping large → tous les types possibles
    if a in ("equity", "stock"):
        a = "stock"
    elif a in ("currency", "forex"):
        a = "forex"
    elif a in ("mutualfund", "fund"):
        a = "fund"
    elif a in ("index"):
        a = "index"
    # crypto, etf, commodity, bond, unknown restent inchangés

    # --------------------------
    # 2) Seuils par asset type
    # --------------------------
    CUTS_MAP = {
        "forex": {
            "daily":  (-0.20, -0.10, -0.03, 0.03, 0.10, 0.20),
            "week":   (-0.60, -0.30, -0.10, 0.10, 0.30, 0.60),
            "month":  (-2.00, -1.00, -0.30, 0.30, 1.00, 2.00),
            "year":   (-6.0,  -3.0,  -1.0, 1.0, 3.0, 6.0),
        },

        "bond": {
            "daily":  (-0.10, -0.05, -0.02, 0.02, 0.05, 0.10),
            "week":   (-0.30, -0.15, -0.05, 0.05, 0.15, 0.30),
            "month":  (-1.00, -0.40, -0.10, 0.10, 0.40, 1.00),
            "year":   (-4.0,  -2.0,  -1.0, 1.0, 2.0, 4.0),
        },

        "stock": {
            "daily":  (-1.50, -0.80, -0.30, 0.30, 0.80, 1.50),
            "week":   (-4.00, -2.00, -0.50, 0.50, 2.00, 4.00),
            "month":  (-12.0, -5.0, -1.5, 1.5, 5.0, 12.0),
            "year":   (-30.0, -12.0, -4.0, 4.0, 12.0, 30.0),
        },

        "index": {
            "daily":  (-1.00, -0.50, -0.15, 0.15, 0.50, 1.00),
            "week":   (-3.00, -1.20, -0.40, 0.40, 1.20, 3.00),
            "month":  (-8.00, -3.00, -1.00, 1.00, 3.00, 8.00),
            "year":   (-20.0, -8.0,  -3.0, 3.0, 8.0, 20.0),
        },

        "etf": {
            "daily":  (-1.20, -0.60, -0.20, 0.20, 0.60, 1.20),
            "week":   (-3.50, -1.50, -0.50, 0.50, 1.50, 3.50),
            "month":  (-8.00, -3.00, -1.00, 1.00, 3.00, 8.00),
            "year":   (-20.0, -8.0,  -3.0, 3.0, 8.0, 20.0),
        },

        "commodity": {
            "daily":  (-2.50, -1.20, -0.40, 0.40, 1.20, 2.50),
            "week":   (-8.00, -3.00, -1.00, 1.00, 3.00, 8.00),
            "month":  (-20.0, -8.0, -3.0, 3.0, 8.0, 20.0),
            "year":   (-50.0, -20.0, -8.0, 8.0, 20.0, 50.0),
        },

        "crypto": {
            "daily":  (-8.0, -4.0, -1.0, 1.0, 4.0, 8.0),
            "week":   (-20.0, -8.0, -2.0, 2.0, 8.0, 20.0),
            "month":  (-50.0, -20.0, -6.0, 6.0, 20.0, 50.0),
            "year":   (-150.0, -50.0, -15.0, 15.0, 50.0, 150.0),
        },

        "fund": {
            "daily":  (-0.20, -0.10, -0.03, 0.03, 0.10, 0.20),
            "week":   (-0.60, -0.30, -0.10, 0.10, 0.30, 0.60),
            "month":  (-2.00, -0.80, -0.30, 0.30, 0.80, 2.00),
            "year":   (-6.00, -2.50, -1.00, 1.00, 2.50, 6.00),
        },

        "unknown": {},
    }

    DEFAULT_CUTS = {
        "daily":  (-0.30, -0.15, -0.05, 0.05, 0.15, 0.30),
        "week":   (-1.00, -0.40, -0.10, 0.10, 0.40, 1.00),
        "month":  (-3.00, -1.00, -0.30, 0.30, 1.00, 3.00),
        "year":   (-10.0, -4.0,  -1.5, 1.5, 4.0, 10.0),
    }

    # --------------------------
    # 3) Sélection freq
    # --------------------------
    if "daily" in f:
        key = "daily"
    elif "week" in f:
        key = "week"
    elif "month" in f:
        key = "month"
    elif "year" in f:
        key = "year"
    else:
        key = "daily"

    # --------------------------
    # 4) Récupération des cuts
    # --------------------------
    cuts = CUTS_MAP.get(a, {}).get(key, DEFAULT_CUTS[key])
    # --------------------------
    # DEBUG TEMPORAIRE
    # --------------------------
    print("DEBUG:", "asset_type:", a, "| freq:", key)
    print("DEBUG cuts:", cuts)
    print("DEBUG value:", M)
    # --------------------------
    # 6) Classification finale
    # --------------------------

    if m <= cuts[0]:
        return "bearish_strong"
    if m <= cuts[1]:
        return "bearish"
    if m <= cuts[2]:
        return "neutral-"
    if m <= cuts[3]:
        return "neutral"
    if m <= cuts[4]:
        return "neutral+"
    if m <= cuts[5]:
        return "bullish"
    return "bullish_strong"

def _ct_add_labels(s: pd.DataFrame, freq_label: str) -> pd.DataFrame:
    df_profiles = pd.read_parquet(os.path.join(DATA_DIR, "vol_profiles.parquet")).set_index("Ticker")
    s = s.copy()
    for col in ["AvgReturn(%)","Momentum(%)","Volatility(%)"]:
        if col not in s:
            s[col] = np.nan

    # Return label
    s["R_label"] = s.apply(
        lambda row: label_return(
            float(row["AvgReturn(%)"]) if pd.notna(row["AvgReturn(%)"]) else 0.0,
            freq_label,
            df_profiles.loc[row.name, "Asset_Type"]
                if row.name in df_profiles.index else "unknown"
        ),
        axis=1
    )

    # Momentum label (multi-actif correct)
    s["M_label"] = s.apply(
        lambda row: _ct_label_momentum_abs(
            float(row["Momentum(%)"]) if pd.notna(row["Momentum(%)"]) else 0.0,
            freq_label,
            df_profiles.loc[row.name, "Asset_Type"]
                if row.name in df_profiles.index else "unknown"
        ),
        axis=1
    )

    # Vol regime
    base = "V_regime" if "V_regime" in s.columns else (
        "Regime" if "Regime" in s.columns else None
    )
    s["V_regime"] = s[base].fillna("unknown").str.lower() if base else "unknown"

    # Vol profile
    prof = "V_profile" if "V_profile" in s.columns else (
        "Volatility_Profile" if "Volatility_Profile" in s.columns else None
    )
    s["V_profile"] = s[prof].fillna("balanced").str.lower() if prof else "balanced"

    return s



def _ct_adjust_bucket(base_bucket: str, row: pd.Series) -> str:
    b = base_bucket
    liq = (row.get("Liquidity_Label") or "").lower()
    if liq in {"illiquid","thin"}:
        if b == "🔴":
            b = "🟠"
    if (row.get("Leverage_Label") or "").lower() == "levered":
        if b == "🟠": b = "🔴"
        if b == "🟢": b = "🟠"
    beta_lab = (row.get("Beta_Label") or "").lower()
    if beta_lab in {"very_high-beta","high-beta"}:
        if b == "🟠": b = "🔴"
    elif beta_lab == "defensive":
        if b == "🔴": b = "🟠"
    return b

_CT_SCENARIOS = {
    "capitulation": ("Capitulation phase", "🔴", "sharp losses with turbulent volatility — risk management first"),
    "stress":       ("Stress phase",       "🔴", "declining returns in an elevated volatility regime"),
    "squeeze":      ("Momentum squeeze",   "🔴", "exceptional momentum under elevated volatility — prone to whipsaws"),
    "rally_tense":  ("Rally under tension","🔴", "strong gains while volatility remains high — vulnerable to pullbacks"),
    "uptrend":      ("Regular uptrend",    "🟠", "robust performance with supportive momentum and contained volatility"),
    "loss_mom":     ("Loss of momentum",   "🟠", "positive returns but weakening momentum — risk of consolidation"),
    "tech_rebound": ("Technical rebound",  "🟠", "improving momentum while returns are still limited"),
    "gradual_down": ("Gradual decline",    "🟠", "soft deterioration without panic — pressure may persist"),
    "vol_compress": ("Volatility compression","🟢","subdued volatility; a breakout setup may be forming"),
    "vol_expand":   ("Volatility expansion","🟠","regime shift with more erratic swings; selectivity is key"),
    "stabilizing":  ("Stabilization after shock","🟠","volatility normalizes; confirmation still needed"),
    "distribution": ("Distribution",       "🟠", "positive returns but momentum erodes — risk of trend fatigue"),
    "range":        ("Range / noise",      "🟢", "no clear direction; rotating momentum and mid-range volatility"),
}

def _ct_payload(row: pd.Series):
    """Retourne des valeurs NUMÉRIQUES (pas des labels) pour l'agrégation."""
    return (
        row.get("AvgReturn(%)",  np.nan),
        row.get("Momentum(%)",   np.nan),
        row.get("Volatility(%)", np.nan),
    )

def _ct_decide_scenario(row: pd.Series):
    R = (row.get("R_label") or "").lower()
    M = (row.get("M_label") or "").lower()
    V = (row.get("V_regime") or "").lower()

    # -------------------------------
    # 1) Groupes de labels
    # -------------------------------
    BEAR = {"bearish"}
    NEUT = {"neutral–", "neutral", "neutral+"}
    BULL = {"bullish"}
    ACC  = {"accelerating", "accelerating+"}

    # -------------------------------
    # 2) Scores pour logique robuste
    # -------------------------------
    MOM_SCORE = (
        -2 if M in BEAR else
        -1 if M in {"neutral–"} else
         0 if M in {"neutral"} else
         1 if M in {"neutral+"} else
         2 if M in BULL else
         3 if M in ACC else 0
    )

    RET_SCORE = (
        -2 if R == "strongly negative" else
        -1 if R == "negative" else
         0 if R in {"neutral"} else
         1 if R == "moderately positive" else
         2 if R == "strong" else
         3 if R == "very strong" else 0
    )

    VOL = V  # déjà normalisé

    # -------------------------------
    # 3) Priorités scénarios
    # -------------------------------

    # Capitulation
    if RET_SCORE <= -2 and VOL == "turbulent" and MOM_SCORE <= -1:
        return "capitulation", *_ct_payload(row)

    # Stress
    if RET_SCORE <= -1 and VOL in {"elevated", "turbulent"}:
        return "stress", *_ct_payload(row)

    # Squeeze
    if RET_SCORE >= 3 and MOM_SCORE >= 3 and VOL in {"elevated", "turbulent"}:
        return "squeeze", *_ct_payload(row)

    # Rally tendu
    if RET_SCORE >= 2 and VOL in {"elevated", "turbulent"}:
        return "rally_tense", *_ct_payload(row)

    # Uptrend propre
    if RET_SCORE >= 1 and MOM_SCORE >= 2 and VOL in {"subdued", "normal"}:
        return "uptrend", *_ct_payload(row)

    # Perte de momentum
    if MOM_SCORE <= -1 and RET_SCORE >= 0 and VOL in {"normal", "elevated"}:
        return "loss_mom", *_ct_payload(row)

    # Tech rebound : momentum fort mais retours encore faibles
    if MOM_SCORE >= 2 and RET_SCORE <= 0:
        return "tech_rebound", *_ct_payload(row)

    # Baisse graduelle
    if RET_SCORE == -1 and VOL in {"subdued", "normal"} and MOM_SCORE <= -1:
        return "gradual_down", *_ct_payload(row)

    # Compression de volatilité
    if VOL == "subdued" and MOM_SCORE >= 0 and RET_SCORE >= 0:
        return "vol_compress", *_ct_payload(row)

    # Expansion de volatilité
    if VOL in {"elevated", "turbulent"} and abs(float(row.get("AvgReturn(%)", 0))) < 0.2 and MOM_SCORE == 0:
        return "vol_expand", *_ct_payload(row)

    # Stabilisation
    if VOL == "elevated" and RET_SCORE == 0 and MOM_SCORE >= 0:
        return "stabilizing", *_ct_payload(row)

    # Distribution
    if RET_SCORE >= 1 and MOM_SCORE <= -1 and VOL in {"normal","elevated"}:
        return "distribution", *_ct_payload(row)

    # Fallback
    return "range", *_ct_payload(row)

def _ct_render_sections(buckets: dict, style_header, style_text):
    order = [("🔴","High-impact observations"),
             ("🟠","Moderate-impact observations"),
             ("🟢","Light-impact observations")]
    blocks = []
    for icon, title in order:
        scenarios = buckets.get(icon, {})
        if not scenarios:
            continue
        blocks.append(Paragraph(f"{icon} <b>{title}</b>", style_header))
        lines = []
        for key, group in scenarios.items():
            title_s, _, desc = _CT_SCENARIOS[key]
            def _fmt_pct(x, nd=1):
                try:    return f"{float(x):.{nd}f}%"
                except: return "n/a"
            def _mean_safe(xs):
                s = pd.to_numeric(pd.Series(xs), errors="coerce").dropna()
                return float(s.mean()) if not s.empty else np.nan
            tickers = ", ".join(map(str, group["tickers"]))
            avgR = _fmt_pct(_mean_safe(group["R_ann"]))
            avgM = _fmt_pct(_mean_safe(group["M_ann"]))
            avgV = _fmt_pct(_mean_safe(group["V_ann"]))
            lines.append(
                f"For <b>{tickers}</b>: <i>{title_s}</i> — {desc}. "
                f"(avg ann. return {avgR}, momentum {avgM}, vol {avgV})"
            )
        blocks.append(Paragraph("<br/>".join(lines), style_text))
    return blocks

def build_ct_commentary(summary: pd.DataFrame,
                        freq_label: str,
                        style_header,
                        style_text,
                        profiles_df: pd.DataFrame = None):
    S = _ct_attach_profiles(summary, profiles_df) if profiles_df is not None else summary
    S = _ct_add_labels(S, freq_label)
    S.to_csv(os.path.join(DATA_DIR, "scenario.csv"), index=False)
    buckets = {"🔴": {}, "🟠": {}, "🟢": {}}
    for ticker, row in S.iterrows():
        key, R_ann, M_ann, V_ann = _ct_decide_scenario(row)
        base_bucket = _CT_SCENARIOS[key][1]
        final_bucket = _ct_adjust_bucket(base_bucket, row)
        if key not in buckets[final_bucket]:
            buckets[final_bucket][key] = {"tickers": [], "R_ann": [], "M_ann": [], "V_ann": []}
        buckets[final_bucket][key]["tickers"].append(ticker)
        buckets[final_bucket][key]["R_ann"].append(R_ann)
        buckets[final_bucket][key]["M_ann"].append(M_ann)
        buckets[final_bucket][key]["V_ann"].append(V_ann)
    return _ct_render_sections(buckets, style_header, style_text)





if len(corr_tickers) < 2:
    corr_matrix = None
    avg_corr = None
    min_corr = None
    max_corr = None
else:
    df_display = df_display.reset_index()
    pivot_returns = df_display.pivot(index="Date", columns="Ticker", values= "Return")
    corr_matrix = pivot_returns.corr().round(2)
    mask = ~np.eye(corr_matrix.shape[0], dtype=bool)
    avg_corr = corr_matrix.where(mask).stack().mean().round(2)
    min_corr = corr_matrix.where(mask).stack().min().round(2)
    max_corr = corr_matrix.where(mask).stack().max().round(2)
        # === Build correlation pairs ===
    pairs = []
    cols = corr_matrix.columns
    for i in range(len(cols)):
        for j in range(i+1, len(cols)):
            pairs.append((cols[i], cols[j], corr_matrix.iloc[i, j]))

    df_pairs = pd.DataFrame(pairs, columns=["A", "B", "corr"])
    df_pos = df_pairs[df_pairs["corr"] >= 0.25].sort_values("corr", ascending=False)
    df_neutral = df_pairs[(df_pairs["corr"] > -0.25) & (df_pairs["corr"] < 0.25)].sort_values("corr", key=lambda x: abs(x))
    df_neg = df_pairs[df_pairs["corr"] <= -0.25].sort_values("corr")
    top_n = 10 if len(summary) > 25 else 5




best_return = summary["AvgReturn(%)"].idxmax()
best_return_val = summary["AvgReturn(%)"].max()
most_volatile = summary["Volatility(%)"].idxmax()
most_volatile_value = summary["Volatility(%)"].max()
best_momentum = summary["Momentum(%)"].idxmax()
best_momentum_value = summary["Momentum(%)"].max()

R_val, M_val, V_val, R_lab, M_lab, V_lab = kpi_labels(summary, freq_label)




meta = pd.read_csv(os.path.join(RAW_DIR, "constituents.csv"))
tickers_used = list(summary.index.astype(str))
tickers_used.sort()
tickers_str = ", ".join(tickers_used)
meta_used = meta[meta["Symbol"].isin(tickers_used)][["Symbol", "Security", "GICS Sector"]]

#  VÉRIFICATION : tous les tickers sont bien dans constituents.csv 
missing_meta = set(summary.index.astype(str)) - set(meta["Symbol"].astype(str).unique())
if missing_meta:
    raise ValueError(
        "❌ Some tickers are missing from constituents.csv:\n"
        + ", ".join(sorted(missing_meta))
        + "\n→ Please update the metadata file."
    )

sector_counts = meta_used["GICS Sector"].value_counts().sort_values(ascending=False)
sector_pct = ( sector_counts / sector_counts.sum() * 100).round(1)
top_returns = summary.sort_values("AvgReturn(%)", ascending=False)[["AvgReturn(%)"]]
top_vol = summary.sort_values("Volatility(%)", ascending=False)[["Volatility(%)"]]
top_mom = summary.sort_values("Momentum(%)", ascending=False)[["Momentum(%)"]]
bottom_returns = summary.sort_values("AvgReturn(%)", ascending=True)[["AvgReturn(%)"]]
bottom_vol = summary.sort_values("Volatility(%)", ascending=True)[["Volatility(%)"]]
bottom_mom = summary.sort_values("Momentum(%)", ascending=True)[["Momentum(%)"]]

show_bottom = len(summary) > 5

def df_to_list(df, label):
    return [[ "Ticker", label ]] + df.reset_index().values.tolist()

def df_pairs_to_list(df, label="Correlation"):
    if df.empty:
        return [["Pair", label], ["—", "—"]]

    rows = [["Pair", label]]
    for _, row in df.iterrows():
        pair = f"{row['A']} / {row['B']}"
        corr = round(float(row['corr']), 2) 
        rows.append([pair, corr])
    return rows

top_n = 5

list_top_returns = df_to_list(top_returns.head(top_n), "AvgReturn(%)")
list_top_vol = df_to_list(top_vol.head(top_n), "Volatility(%)")
list_top_mom = df_to_list(top_mom.head(top_n), "Momentum(%)")

if show_bottom:
    list_bottom_returns = df_to_list(bottom_returns.head(top_n), "AvgReturn(%)")
    list_bottom_vol = df_to_list(bottom_vol.head(top_n), "Volatility(%)")
    list_bottom_mom = df_to_list(bottom_mom.head(top_n), "Momentum(%)")






fmt = "%Y-%m-%d" 
start_str = start_display.strftime(fmt)
end_str   = end_display.strftime(fmt)


kpi_text = (
    f"On a {horizon['adj']} basis, {best_return} shows the highest average return "
    f"({best_return_val:.2f}%). "
    f"The most volatile ticker is {most_volatile} "
    f"(over a {window_vol} {horizon['plural']} rolling window), suggesting higher risk of drawdowns. "
    f"{best_momentum} leads on short-term momentum "
    f"(computed over {window_momentum} {horizon['plural']})."
)

if corr_matrix is not None:
    viz_text = correlation_comment(corr_matrix)

# Création de la liste brute des tickers formatés
tickers_html = [
    f"• <u>{row.Symbol}</u> ({row.Security} — {row['GICS Sector']})"
    for _, row in meta_used.iterrows()
]

# Division en deux colonnes
mid = len(tickers_html) // 2
col1 = "<br/>".join(tickers_html[:mid])
col2 = "<br/>".join(tickers_html[mid:])



n_tickers = len(summary)

if n_tickers <= 5:
    w, h, w_m, i_m1, i_m2 = 11*cm, 5*cm, 7*cm, 17.5*cm, 11.5*cm
elif n_tickers <= 10:
    w, h, w_m, i_m1, i_m2  = 13*cm, 6*cm, 10*cm, 19.5*cm, 13.5*cm
elif n_tickers <= 20:
    w, h, w_m, i_m1, i_m2  = 18.5*cm, 8.5*cm, 15*cm, 15*cm, 9*cm
else:
    w, h, w_m, i_m1, i_m2  = 18.5*cm, 8.5*cm, 18.5*cm, 15*cm, 9*cm

#Creation de la figure
threshold = 12
if n_tickers <= threshold:
    buffer = io.BytesIO()

    if corr_matrix is None:

        fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
        axes = axes.ravel()
        axes[3].remove()   
    else:
        fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
        axes = axes.ravel()

    fig.suptitle("Sector Performance Dashboard", fontsize=14, fontweight="bold")

    # === 2) Graphiques standard ===
    axes[0].bar(summary.index, summary["AvgReturn(%)"], color="olive")
    axes[0].tick_params(axis='x', labelrotation=45)
    axes[0].set_title(f"Return ({window_return} {horizon['plural']})")
    axes[0].axhline(0, color="black", linestyle="--", linewidth=1.5, alpha=0.6)

    axes[1].bar(summary.index, summary["Volatility(%)"], color="purple")
    axes[1].tick_params(axis='x', labelrotation=45)
    axes[1].set_title(f"Volatility ({window_vol} {horizon['plural']})")

    axes[2].bar(summary.index, summary["Momentum(%)"], color="darkred")
    axes[2].tick_params(axis='x', labelrotation=45)
    axes[2].set_title(f"Momentum ({window_momentum} {horizon['plural']})")
    axes[2].axhline(0, color="black", linestyle="--", linewidth=1.5, alpha=0.6)

    # === 3) Correlation Matrix only if relevant ===
    if corr_matrix is not None:
        im = axes[3].imshow(corr_matrix, cmap="RdBu_r", interpolation="nearest",vmin=-1, vmax=1)
        axes[3].set_title("Correlation Matrix")
        axes[3].set_xticks(range(len(corr_matrix.columns)))
        axes[3].set_yticks(range(len(corr_matrix.columns)))
        axes[3].set_xticklabels(corr_matrix.columns, rotation=45, ha="right")
        axes[3].set_yticklabels(corr_matrix.columns)
        axes[3].grid(False)
        fig.colorbar(im, ax=axes[3], fraction=0.046, pad=0.04)

    # === 4) Sauvegarde ===
    fig.savefig(buffer, format="png", dpi=200, bbox_inches="tight")
    buffer.seek(0)

    img = Image(buffer, width=i_m1, height=i_m2)
    img.hAlign = "CENTER"
else:

    buf_return = io.BytesIO()
    fig, ax = plt.subplots(figsize=(12, 8), constrained_layout=True)
    ax.bar(summary.index, summary["AvgReturn(%)"], color="olive")
    ax.set_title(f"Average {horizon['unit'].capitalize()} Returns by Sector")
    ax.set_ylabel("Return (%)")
    ax.axhline(0, color='black', linewidth=1.5, linestyle='--', alpha=0.6)
    ax.tick_params(axis='x', labelrotation=75, labelsize=8)
    fig.savefig(buf_return, format="png", dpi=200, bbox_inches="tight")
    buf_return.seek(0)

    # === Figure 2 : Volatility ===
    buf_vol = io.BytesIO()
    fig, ax = plt.subplots(figsize=(12, 8), constrained_layout=True)
    ax.bar(summary.index, summary["Volatility(%)"], color="purple")
    ax.set_title(f"Volatility ({window_vol} {horizon['plural']} rolling std)")
    ax.set_ylabel("Volatility (%)")
    ax.tick_params(axis='x', labelrotation=75, labelsize=8)
    fig.savefig(buf_vol, format="png", dpi=200, bbox_inches="tight")
    buf_vol.seek(0)

    # === Figure 3 : Momentum ===
    buf_mom = io.BytesIO()
    fig, ax = plt.subplots(figsize=(12, 8), constrained_layout=True)
    ax.bar(summary.index, summary["Momentum(%)"], color="darkred")
    ax.set_title(f"Momentum (window: {window_momentum} {horizon['plural']})")
    ax.set_ylabel("Momentum (%)")
    ax.axhline(0, color='black', linewidth=1.5, linestyle='--', alpha=0.6)
    ax.tick_params(axis='x', labelrotation=75, labelsize=8)
    fig.savefig(buf_mom, format="png", dpi=200, bbox_inches="tight")
    buf_mom.seek(0)

    # === Figure 4 : Correlation Matrix ===
    if corr_matrix is not None:
        buf_corr = io.BytesIO()
        fig, ax = plt.subplots(figsize=(12, 8), constrained_layout=True)
        im = ax.imshow(corr_matrix, cmap="RdBu_r", interpolation="nearest", vmin=-1, vmax=1)
        ax.grid(False)
        ax.set_title("Correlation Matrix between Sectors")
        ax.set_xticks(range(len(corr_matrix.columns)))
        ax.set_yticks(range(len(corr_matrix.columns)))
        ax.set_xticklabels(corr_matrix.columns, rotation=45, ha="right")
        ax.set_yticklabels(corr_matrix.columns)
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        fig.savefig(buf_corr, format="png", dpi=200, bbox_inches="tight")
        buf_corr.seek(0)

    img_return = Image(buf_return, width= w, height=h)
    img_return.hAlign = "CENTER"
    img_vol = Image(buf_vol, width=w, height=h)
    img_vol.hAlign = "CENTER"
    img_mom = Image(buf_mom, width=w, height=h)
    img_mom.hAlign = "CENTER"

    if corr_matrix is not None:
        img_corr = Image(buf_corr, width=w_m, height=w_m)
        img_corr.hAlign = "CENTER"





fig_pie, ax_pie = plt.subplots(figsize=(10, 5))

n = len(sector_pct)
palette = plt.colormaps.get_cmap("tab20")(np.linspace(0, 1, n))  

# On affiche les pourcentages à l’intérieur du camembert
wedges, texts, autotexts = ax_pie.pie(
    sector_pct,
    autopct="%1.1f%%",     
    startangle=90,
    colors=palette,
    textprops={"fontsize": 12, "color": "white"} 
)

# Légende à droite
ax_pie.legend(
    wedges,
    [f"{s} ({p}%)" for s, p in zip(sector_pct.index, sector_pct.values)],
    loc="center left",
    bbox_to_anchor=(1.05, 0.5),
    fontsize=12,
    frameon=False
)

# Titre et marges
ax_pie.set_title("Sector Allocation", fontsize=12, fontweight="bold")
fig_pie.subplots_adjust(left=0.05, right=0.8, top=0.9, bottom=0.1)

# Sauvegarde
fig_pie.savefig(pie_buffer, format="png", dpi=200, bbox_inches="tight")
pie_buffer.seek(0)

n_tickers = len(summary)

if n_tickers <= 5:
    i, p = 16*cm, 8*cm
elif n_tickers <= 10:
    i, p = 16*cm, 8*cm
elif n_tickers <= 20:
    i, p = 18*cm, 9*cm
else:
    i, p = 19.5*cm, 10.5*cm

img_pie = Image(pie_buffer, width=i, height=p)
img_pie.hAlign = "CENTER"



# --- Styles ---
wrap_style = ParagraphStyle(
    name="wrap_style",
    fontName="Helvetica",
    fontSize=8,
    leading=10,
    textColor=colors.black,
    alignment=0,
    wordWrap='LTR',
    spaceAfter=2
)

header_style = ParagraphStyle(
    name="header_style",
    fontName="Helvetica-Bold",
    fontSize=9,
    leading=11,
    alignment=1,  
    textColor=colors.black,
    wordWrap='LTR'
)

num_style = ParagraphStyle(
    name="num_style",
    fontName="Helvetica-Bold",
    fontSize=13,  
    leading=25,
    alignment=1,  
    textColor=colors.black
)

num_style_2 = ParagraphStyle(
    name="num_style_2",
    fontName="Helvetica-Bold",
    fontSize=10,   
    leading=25,
    alignment=1, 
    textColor=colors.black
)
# --- Sélection et renommage ---
summary_display = summary[[
    "AvgReturn(%)",
    "Volatility(%)",
    "Risk_Adjusted_return",
    "Momentum(%)",
    "Signal_Stability_Label",
    "V_regime",
    "Liquidity_Label",
    "Commentary"
]].copy()

summary_display = summary_display.rename(columns={
    "AvgReturn(%)": "R (%)",
    "Volatility(%)": "V (%)",
    "Risk_Adjusted_return": "RAR",
    "Momentum(%)": "M (%)",
    "Signal_Stability_Label": "Signal",
    "V_regime": "Regime",
    "Liquidity_Label": "Liquidity"
})

summary_display_LT = summary[[
    "ΔReturn(pp)",
    "Momentum_Ratio",
    "Signal_Stability",
    "Volatility_Ratio",
    "Beta",
    "ADV10_Display",
    "Interpretation"
]]

summary_display_LT = summary_display_LT.rename(columns={
    "Momentum_Ratio": "Momentum Ratio",
    "Signal_Stability": "Signal ",
    "Volatility_Ratio": "Volatility Ratio",
    "ADV10_Display": "ADV10 USD"
})



def style_table_cells(df):
    df_styled = df.copy()
    for col in df_styled.columns:
        if col in [
            "R (%)", "V (%)", "M (%)",
            "ΔReturn(pp)", "Momentum Ratio", "Volatility Ratio", "Beta"
        ]:
            df_styled[col] = df_styled[col].apply(lambda x: colorize_number(x, num_style))
        elif col in [
            "R (%)", "V (%)", "M (%)",
            "RAR", "ADV10 USD", "Signal "
        ]:
            df_styled[col] = df_styled[col].apply(lambda x: Paragraph(str(x), num_style_2))
    
        else:
            df_styled[col] = df_styled[col].apply(lambda x: Paragraph(str(x), wrap_style))
    return df_styled

styled_summary = style_table_cells(summary_display)
styled_summary_LT = style_table_cells(summary_display_LT)

summary_reset = styled_summary.reset_index()
summary_reset_LT = styled_summary_LT.reset_index()
headers_wrapped = [Paragraph(str(col), header_style) for col in summary_reset.columns]
headers_wrapped_LT = [Paragraph(str(col), header_style) for col in summary_reset_LT.columns]

list_summary = [headers_wrapped] + summary_reset.values.tolist()
list_summary_LT = [headers_wrapped_LT] + summary_reset_LT.values.tolist()



doc = SimpleDocTemplate(
    os.path.join(REPORT_DIR, report_name),
    pagesize=portrait(A4),
    leftMargin=1 * cm,
    rightMargin=1 * cm,
    topMargin=0.5 * cm,
    bottomMargin=0.5 * cm,
)

styles = getSampleStyleSheet()
styleTitre = ParagraphStyle(
    "TitreCentre",
    parent=styles["Title"],
    alignment=TA_CENTER,
    spaceAfter=12
)
styleNormal = ParagraphStyle(
    "BodyNice",
    parent=styles["BodyText"],
    leading=14,
    alignment=TA_JUSTIFY,
    spaceAfter=6
)

styleNormal_frequency = ParagraphStyle(
    "BodyNice",
    parent=styles["BodyText"],
    leading=13,
    fontSize=9,
    alignment=TA_JUSTIFY,
    spaceAfter=6
)
styleSection = ParagraphStyle(
    "SectionHeader",
    parent=styles["Heading2"],
    fontSize=13,
    leading=16,
    textColor=colors.HexColor("#004d80"),
    spaceBefore=18,
    spaceAfter=6
)
styleSubSection = ParagraphStyle(
    "SubSectionHeader",
    parent=styleSection,      
    fontSize=11.5,         
    leading=14,             
    textColor=colors.HexColor("#006699"), 
    spaceBefore=12,          
    spaceAfter=4,        
    leftIndent=0.3*cm,        
)
styleSubSection_page1 = ParagraphStyle(
    "SubSectionHeader",
    parent=styleSection,    
    fontSize=11.5,     
    leading=14,             
    textColor=colors.HexColor("#006699"), 
    spaceBefore=0,            
    spaceAfter=4,            
    leftIndent=0.3*cm,          
)
styleComment = ParagraphStyle(
    "Commentaire",
    parent=styles["BodyText"],
    fontSize=10.5,
    leading=14,
    textColor=colors.HexColor("#333333"),
    spaceBefore=12,
    leftIndent=0.5*cm
)
styleComment_Page1 = ParagraphStyle(
    "Commentaire",
    parent=styles["BodyText"],
    fontSize=10,
    leading=11,
    textColor=colors.HexColor("#333333"),
    spaceBefore=6,
    leftIndent=0.5*cm
)
ct_blocks = build_ct_commentary(
    summary, freq_label, styleSubSection, styleNormal, profiles_df=df_profiles
)

#  Définition du style de base sous forme de liste
base_style = [
    ('GRID', (0,0), (-1,-1), 0.25, colors.grey),
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#eaeaea")),  # en-tête
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]

#  Application du zébrage clair sur les lignes de données
for i in range(1, len(list_summary)):
    if i % 2 == 0:
        bg_color = colors.white
    else:
        bg_color = colors.HexColor("#f9f9f9")
    base_style.append(('BACKGROUND', (0, i), (-1, i), bg_color))

#  Création finale du TableStyle
table_style = TableStyle(base_style)
    
# Tableau sans bordures, deux colonnes équilibrées
tickers_table = Table(
    [[Paragraph(col1, styleNormal),"", Paragraph(col2, styleNormal)]],
    colWidths=[8*cm,1*cm, 8*cm],
    style=TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        # aucune ligne ni bordure
    ])
)

tickers_list = tickers_str.split(", ")
# Regrouper les tickers par groupes de 10
tickers_wrapped = "<br/>".join(
    [", ".join(tickers_list[i:i+10]) for i in range(0, len(tickers_list), 10)]
)
# =====================================================
# === METHOD TABLE (with dynamic frequency comment)
# =====================================================

# Message dynamique selon la profondeur des données
# Définition des bornes d'interprétation
min_req = {"daily": 40, "weekly": 12, "monthly": 8, "yearly": 5}.get(freq_label.lower(), 12)
max_rec = {"daily": 200, "weekly": 52, "monthly": 60, "yearly": 20}.get(freq_label.lower(), 200)

too_long = n_points_disp > max_rec
excess_ratio = (n_points_disp / max_rec) - 1
excess_pct = round(excess_ratio * 100, 1)

if not ct_ok:
    freq_comment = (
        f"<b>{freq_label}</b> — {n_points_disp} observations.<br/>"
        f"<font color='red'><b>Insufficient data.</b></font> "
        f"(minimum required: {min_req})."
    )

elif ct_ok and not lt_ok:
    freq_comment = (
        f"<b>{freq_label}</b> — {n_points_disp} observations.<br/>"
        "Short-term indicators: <font color='green'><b>OK</b></font>.<br/>"
        "Long-term indicators: <font color='red'><b>Unavailable</b></font> "
        "(insufficient historical depth)."
    )

else:
    freq_comment = (
        f"<b>{freq_label}</b> — {n_points_disp} observations.<br/>"
        "<font color='green'><b>Sufficient depth:</b></font> "
        "short- and long-term indicators are statistically reliable."
    )

# Warning pour fenêtre trop longue
if too_long:
    freq_comment += (
        "<br/><font color='#CC6600'><b>Warning:</b></font> "
        "the observation window exceeds the typical interpretability range for this frequency "
        f"(+{excess_pct}% above the recommended upper bound). "
        "Results may blend multiple market regimes, reducing economic signal clarity."
    )



method_rows = [
    ["Date of extraction", datetime.now().strftime("%Y-%m-%d %H:%M")],
    ["Data window", f"{start_str} → {end_str}"],
    ["Frequency",   Paragraph(freq_comment, styleNormal_frequency)],
    ["Tickers",     Paragraph(tickers_wrapped, styleNormal)],
    ["Indicators",  Paragraph(window_label, styleNormal)],
]
method_table = Table(method_rows, colWidths=[3.5*cm, 14.5*cm], style=TableStyle([
    ("BACKGROUND",(0,0),(0,-1), colors.HexColor("#f7f7f7")),
    ("ALIGN",(0,0),(-1,-1),"LEFT"),
    ("GRID",(0,0),(-1,-1),0.25, colors.HexColor("#dddddd")),
    ("FONTNAME",(0,0),(-1,-1),"Helvetica"),
    ("BOTTOMPADDING",(0,0),(-1,-1),4),
    ("TOPPADDING",(0,0),(-1,-1),4),
]))


table = LongTable(
    list_summary,
    colWidths=[1.7*cm, 1.5*cm, 1.5*cm, 1.6*cm, 1.5*cm, 1.6*cm, 1.6*cm, 2*cm, 6.5*cm],
    repeatRows=1,
    splitByRow=1,
    hAlign="CENTER",
    style=table_style
)

table_LT = LongTable(
    list_summary_LT,
    colWidths=[1.7*cm, 1.7*cm, 2.2*cm, 1.6*cm, 2*cm, 1.6*cm, 2*cm, 7.3*cm],
    repeatRows=1,
    splitByRow=1,
    hAlign="CENTER",
    style=table_style
)

table1 = Table(list_top_returns, colWidths=[3*cm]*len(list_top_returns[0]))
table2 = Table(list_top_vol, colWidths=[3*cm]*len(list_top_vol[0]))
table3 = Table(list_top_mom, colWidths=[3*cm]*len(list_top_mom[0]))

for t in (table1, table2, table3):
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#f2f2f2")),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.HexColor("#222222")),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("GRID", (0,0), (-1,-1), 0.25, colors.HexColor("#cccccc")),
        ("FONTSIZE", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ]))

for t in (table1, table2, table3):
    t._argW = [2.5*cm for _ in t._argW]

title_style = ParagraphStyle(
    "MiniHeader",
    parent=styleNormal,
    alignment=TA_CENTER,
    fontSize=9.5,
    textColor=colors.HexColor("#004d80"),
    spaceAfter=4,
    spaceBefore=4,
)


sub1 = Paragraph("<b>Top by Average Return</b>", title_style)
sub2 = Paragraph("<b>Top by Volatility</b>", title_style)
sub3 = Paragraph("<b>Top by Momentum</b>", title_style)

sub_1 = Paragraph("<b>Last by Average Return</b>", title_style)
sub_2 = Paragraph("<b>Last by Volatility</b>", title_style)
sub_3 = Paragraph("<b>Last by Momentum</b>", title_style)

combined_tables = Table(
    [
        [sub1, sub2, sub3],
        [table1, table2, table3]
    ],
    colWidths=[6*cm, 6*cm, 6*cm]
)

combined_tables.setStyle(TableStyle([
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 2),
    ("BOTTOMPADDING", (0,0), (-1,-1), 2),
]))


if show_bottom:
    b_table1 = Table(list_bottom_returns, colWidths=[3*cm]*len(list_top_returns[0]))
    b_table2 =Table(list_bottom_vol, colWidths=[3*cm]*len(list_top_vol[0]))
    b_table3 =Table(list_bottom_mom, colWidths=[3*cm]*len(list_top_mom[0]))

    for t in (b_table1, b_table2, b_table3):
        t.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#f2f2f2")),
            ("TEXTCOLOR",  (0,0), (-1,0), colors.HexColor("#222222")),
            ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("GRID", (0,0), (-1,-1), 0.25, colors.HexColor("#cccccc")),
            ("FONTSIZE", (0,0), (-1,-1), 8),
            ("TOPPADDING", (0,0), (-1,-1), 3),
            ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ]))

    for t in (b_table1, b_table2, b_table3):
        t._argW = [2.5*cm for _ in t._argW]

    combined_bottom = Table(
    [
        [sub_1, sub_2, sub_3],
        [b_table1, b_table2, b_table3]
    ],
    colWidths=[6*cm, 6*cm, 6*cm]
)

    combined_bottom.setStyle(TableStyle([
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 2),
    ("BOTTOMPADDING", (0,0), (-1,-1), 2),
]))


# ---------------------------------------
# ==========================
# 3.3 Top correlation tables
# ==========================
n_assets = len(corr_matrix.columns)
total_pairs = n_assets * (n_assets - 1) / 2


p_pos     = round(100 * len(df_pos)     / total_pairs, 1)
p_neutral = round(100 * len(df_neutral) / total_pairs, 1)
p_neg     = round(100 * len(df_neg)     / total_pairs, 1)


def _safe_pairs_list(df, top_n):
    if len(df) >= 1:
        return df_pairs_to_list(df.head(top_n))
    else:
        return [["Pair", "Correlation"], ["No data", ""]]



table_pos     = Table(_safe_pairs_list(df_pos,     top_n), colWidths=[3*cm, 2.5*cm])
table_neutral = Table(_safe_pairs_list(df_neutral, top_n), colWidths=[3*cm, 2.5*cm])
table_neg     = Table(_safe_pairs_list(df_neg,     top_n), colWidths=[3*cm, 2.5*cm])

for t in (table_pos, table_neutral, table_neg):
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#f2f2f2")),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.HexColor("#222222")),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("GRID", (0,0), (-1,-1), 0.25, colors.HexColor("#cccccc")),
        ("FONTSIZE", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ]))
    t._argW = [2.8*cm for _ in t._argW]



titles = []
tables = []

if len(df_pos) >= 1:
    titles.append(
        Paragraph(f"<b>Top Positive Correlations</b><br/>{p_pos}% of portfolio", title_style)
    )
    tables.append(table_pos)

if len(df_neutral) >= 1:
    titles.append(
        Paragraph(f"<b>Top Neutral Correlations</b><br/>{p_neutral}% of portfolio", title_style)
    )
    tables.append(table_neutral)

if len(df_neg) >= 1:
    titles.append(
        Paragraph(f"<b>Top Negative Correlations</b><br/>{p_neg}% of portfolio", title_style)
    )
    tables.append(table_neg)


if len(titles) == 0:
    titles = [Paragraph("<b>No correlation data available</b>", title_style)]
    tables = [Paragraph("Correlation matrix empty.", styleNormal)]



combined_corr_tables = Table(
    [titles, tables],
    colWidths=[6*cm] * len(titles)
)

combined_corr_tables.setStyle(TableStyle([
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 2),
    ("BOTTOMPADDING", (0,0), (-1,-1), 2),
]))

# =====================================================
# === KPI BLOCK ASSEMBLY (with conditional LT table)
# =====================================================
macro_profile_block = KeepTogether([
    Paragraph("Macro Profile Insight", styleSubSection_page1),
    Paragraph(macro_profile_comment(meta_used, profiles_df=df_profiles), styleComment_Page1)
])

corr_block = []

if len(summary) <= threshold:
    graphs_block = KeepTogether([
        Paragraph("2. Sector Performance Visualization", styleSection),
        Spacer(1, 0.2*cm),
        img,
        Spacer(1, 0.2*cm),
    ])
else:
    graphs_block = KeepTogether([
        Paragraph("2. Sector Performance Visualization", styleSection),
        Spacer(1, 0.5*cm),
        img_return,
        Spacer(1, 0.5*cm),
        img_vol,
        Spacer(1, 0.5*cm),
        img_mom,
        Spacer(1, 0.5*cm),
    ])
    if corr_matrix is not None:
        corr_block.append(img_corr)
        corr_block.append(Spacer(1, 0.3*cm))


if corr_matrix is not None:
    corr_block.append(Paragraph(viz_text, styleNormal))
    corr_block.append(Spacer(1, 0.3*cm))
    corr_block.append(KeepTogether(combined_corr_tables))

current_snapshot_block = KeepTogether([
    Paragraph("3. Key Performance Indicators", styleSection),
    Paragraph("3.a Current Regime Snapshot", styleSubSection),
    Spacer(1, 0.3*cm),
    table
])

if show_bottom:
    top_last_block = KeepTogether([
        Spacer(1, 0.5*cm),
        combined_tables,
        Spacer(1, 0.3*cm),
        combined_bottom,
        Spacer(1, 0.3*cm)
    ])
else:
    top_last_block = KeepTogether([
        Spacer(1, 0.5*cm),
        combined_tables
    ])

block_LT = []
if lt_ok:
    block_LT = KeepTogether([
        Paragraph("3.b Rotation & Stress Metrics", styleSubSection),
        Spacer(1, 0.5*cm),
        table_LT
    ])

ct_blocks_fixed = [KeepTogether(b) for b in ct_blocks]

kpi_block = [
    current_snapshot_block,
    top_last_block,
]

if block_LT:
    kpi_block.append(block_LT)

kpi_block += ct_blocks_fixed

story = [
    Paragraph("Portfolio rotation report", styleTitre),
    method_table,
    Paragraph("1. Portfolio Composition", styleSection),
    tickers_table,
    Spacer(1, 0.5*cm),
    img_pie,

    macro_profile_block,    

    graphs_block,              
    *corr_block,                  

    *kpi_block             
]

doc.build(story)

end_time = time.time()
print(f"⏱ Total time: {end_time - start_time:.2f} seconds")
