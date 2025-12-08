import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf

# ------------------------
# 1. Petites fonctions utilitaires
# ------------------------

def base100(series):
    """
    Met une série en base 100 à partir de son premier point non-nul.
    """
    series = series.dropna()
    if series.empty:
        return series
    return series / series.iloc[0] * 100


def validate_R3_longterm(
    tickers,
    df_display,
    window=240,
    save_path="/Users/benjaminvissac/Documents/GitHub/factor-rotation/report/backtests_charts/R3_momentum_LT.png",
):
    """
    Test R3 (long terme) :
    Vérifier que la variation du momentum long terme suit qualitativement
    la dynamique réelle du prix, sur une fenêtre de `window` points.

    Utilise exclusivement df_display car il contient :
      - Close
      - Momentum_LT(%)
      - des dates parfaitement alignées pour les indicateurs LT.
    """

    # Trier les données
    df_display = df_display.sort_values(["Ticker", "Date"])

    # Mise en page 3x2 (5 tickers max → 1 case vide)
    n = len(tickers)
    rows, cols = 3, 2
    fig, axes = plt.subplots(rows, cols, figsize=(12, 10), dpi=150)
    axes = axes.flatten()

    for i, tic in enumerate(tickers):
        ax = axes[i]

        # Extraction des données pour ce ticker
        sub = (
            df_display[df_display["Ticker"] == tic]
            .sort_values("Date")[["Date", "Close", "Momentum_LT(%)"]]
            .dropna(subset=["Close", "Momentum_LT(%)"])
            .copy()
        )

        # Vérifications
        if sub.empty:
            ax.set_title(f"{tic} – no LT data available")
            ax.axis("off")
            continue

        if len(sub) < window:
            ax.set_title(f"{tic} – insufficient LT history (< {window})")
            ax.axis("off")
            continue

        # Garder les `window` dernières observations
        sub = sub.tail(window).copy()

        # Prix base 100
        sub["Price_b100"] = base100(sub["Close"])

        # ---- Plot prix (axe gauche) ----
        ax.plot(
            sub["Date"],
            sub["Price_b100"],
            lw=2,
            color="tab:blue",
            label="Price (base 100)"
        )
        ax.set_ylabel("Price (base 100)", fontsize=8)
        ax.tick_params(axis="y", labelsize=8)
        ax.tick_params(axis="x", labelsize=7, rotation=45)

        # ---- Plot momentum LT (axe droit) ----
        ax2 = ax.twinx()
        ax2.plot(
            sub["Date"],
            sub["Momentum_LT(%)"],
            lw=1.6,
            ls="--",
            color="tab:red",
            label="Momentum_LT(%)"
        )
        ax2.axhline(0, lw=0.7, ls=":", color="grey", alpha=0.7)
        ax2.set_ylabel("Momentum_LT(%)", fontsize=8)
        ax2.tick_params(axis="y", labelsize=8)

        # Titre + grille
        ax.set_title(tic, fontsize=11, fontweight="bold")
        ax.grid(True, alpha=0.25)

    # Cacher axes inutilisés
    if len(axes) > n:
        for j in range(n, len(axes)):
            axes[j].axis("off")

    # Titre global
    fig.suptitle(
        f"R3 – Long-Term Momentum Validation ({window}-point window)",
        fontsize=14,
        fontweight="bold",
        y=0.98,
    )

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"✅ R3 long-term momentum chart saved to:\n{save_path}")

def plot_R3_momentum(
    tickers,
    df_all,
    df_display,
    window_mom=8,
    save_path="/Users/benjaminvissac/Documents/GitHub/factor-rotation/report/backtests_charts/R3_momentum.png"
):
    """
    Test R3 : vérifier que la variation du momentum et son ratio
    suivent la dynamique réelle du prix.

    Pour chaque ticker :
      - on récupère Close (df_all)
      - on récupère Momentum(%) (df_display)
      - on merge sur Date
      - on garde les `window_mom` dernières observations
      - on trace Prix base 100 + Momentum(%) sur deux axes Y.
    """

    # --------- Figure 2x2 + 1 (soit 3x2 et on cache le dernier) ----------
    n = len(tickers)
    rows, cols = 3, 2   # 6 emplacements, on en utilise 5
    fig, axes = plt.subplots(rows, cols, figsize=(12, 10), dpi=150)
    axes = axes.flatten()

    for i, ticker in enumerate(tickers):
        ax = axes[i]

        # --- Prix (df_all) ---
        sub_price = (
            df_all[df_all["Ticker"] == ticker]
            .sort_values("Date")[["Date", "Close"]]
            .dropna()
        )

        # --- Momentum (df_display) ---
        sub_mom = (
            df_display[df_display["Ticker"] == ticker]
            .sort_values("Date")[["Date", "Momentum(%)"]]
            .dropna()
        )

        # Merge sur Date
        sub = pd.merge(sub_price, sub_mom, on="Date", how="inner")

        if len(sub) < window_mom:
            ax.set_title(f"{ticker} – insufficient data", fontsize=10)
            ax.axis("off")
            continue

        # On garde les `window_mom` dernières observations
        sub = sub.tail(window_mom).copy()

        # Prix base 100
        sub["Price_b100"] = base100(sub["Close"])

        # ----- Plot -----
        # Axe principal : prix base 100
        ax.plot(
            sub["Date"],
            sub["Price_b100"],
            label="Price (base 100)",
            lw=2
        )
        ax.set_ylabel("Price (base 100)", fontsize=8)
        ax.tick_params(axis="y", labelsize=8)
        ax.tick_params(axis="x", labelsize=7, rotation=45)

        # Axe secondaire : Momentum (%)
        ax2 = ax.twinx()
        ax2.plot(
            sub["Date"],
            sub["Momentum(%)"],
            label="Momentum (%)",
            lw=1.6,
            ls="--"
        )
        ax2.axhline(0, lw=0.7, ls=":", alpha=0.6)
        ax2.set_ylabel("Momentum (%)", fontsize=8)
        ax2.tick_params(axis="y", labelsize=8)

        # Titre
        ax.set_title(ticker, fontsize=11, fontweight="bold")

        # Petite grille
        ax.grid(True, alpha=0.25)

    # On masque le dernier subplot inutilisé (6e)
    if len(axes) > n:
        for j in range(n, len(axes)):
            axes[j].axis("off")

    # Titre global & layout
    fig.suptitle(
        "R3 – Momentum Validation (Price vs Momentum – 16-week window)",
        fontsize=14,
        fontweight="bold",
        y=0.98
    )
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    # Sauvegarde
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"✅ R3 momentum chart saved to:\n{save_path}")




def plot_price_vs_return_multi(df_all, tickers, window_return=12, window_long=30):
    fig, axes = plt.subplots(3, 1, figsize=(14, 18), sharex=False)
    fig.suptitle("R1 – Price vs Short-Term Return (12-week rolling)", fontsize=18, fontweight="bold")

    for ax, ticker in zip(axes, tickers):

        # ---------- 1) Extraire les données ----------
        df = df_all[df_all["Ticker"] == ticker].copy().sort_values("Date")

        # Prix base 100
        df["Price_Base100"] = df["Close"] / df["Close"].iloc[0] * 100

        # Rendement court terme (rolling sum log returns, 12w)
        df["ShortReturn"] = (
            df["log_ret"]
            .rolling(window_return, min_periods=1)
            .sum()
            * 100
        )

        # ---------- 2) Zones colorées ----------
        start_ST = df["Date"].iloc[-window_return]       # début zone court terme
        start_LT = df["Date"].iloc[window_long]         # début zone long terme

        ax.axvspan(start_ST, df["Date"].iloc[-1],
                   color="gray", alpha=0.12, label="Short-term window")

        ax.axvspan(start_LT, start_ST,
                   color="blue", alpha=0.06, label="Long-term window")

        # ---------- 3) Courbe prix ----------
        ax.plot(df["Date"], df["Price_Base100"],
                label="Price (base 100)", color="tab:blue", linewidth=2)

        # ---------- 4) Courbe rendement court terme ----------
        ax2 = ax.twinx()
        ax2.plot(df["Date"], df["ShortReturn"],
                 label="Short-term return (12w)", color="tab:red", linestyle="--", linewidth=2)

        # ---------- 5) Esthétique ----------
        ax.set_title(f"{ticker}", fontsize=14, fontweight="bold")
        ax.set_ylabel("Price (base 100)")
        ax2.set_ylabel("Short-term return (%)")

        ax.grid(True, linestyle="--", alpha=0.3)

    plt.tight_layout()
    plt.subplots_adjust(top=0.93)

    fig.savefig("/Users/benjaminvissac/Documents/GitHub/factor-rotation/report/backtests_charts/R1_price_vs_return.png", dpi=200, bbox_inches="tight")
    print("Figure saved: R1_price_vs_return.png")
# ------------------------
# 2. Exécution directe
# ------------------------
if __name__ == "__main__":

    # Chemins à adapter si besoin, mais normalement c'est bon pour ton projet
    df_all = pd.read_parquet(
        "/Users/benjaminvissac/Documents/GitHub/factor-rotation/data/processed/df_all.parquet"
    )
    df_display = pd.read_parquet(
        "/Users/benjaminvissac/Documents/GitHub/factor-rotation/data/processed/df_display.parquet"
    )

    tickers_R3 = [
    "SAP.DE",   # SAP SE
    "DTE.DE",   # Deutsche Telekom AG
    "BAYN.DE",  # Bayer AG
    "LIN.DE",   # Linde plc
    "HEN3.DE"   # Henkel AG & Co. KGaA
    ]

    plot_price_vs_return_multi(df_all, tickers_R3, 9, 18)
    validate_R3_longterm(
    tickers_R3,
    df_all,
    window=36,
    save_path="/Users/benjaminvissac/Documents/GitHub/factor-rotation/report/backtests_charts/R3_momentum_LT.png")
    #plot_R3_momentum(
    #tickers_R3,
    #df_all,
    #df_display,
    #window_mom=80,
    #save_path="/Users/benjaminvissac/Documents/GitHub/factor-rotation/report/backtests_charts/R3_momentum_CT.png")

def R8_test(df, tickers):
    # ======================================================
    # 1) Charger ton parquet modifié (S3_R8.parquet)
    # ======================================================
    df = pd.read_parquet(
        "/Users/benjaminvissac/Documents/GitHub/factor-rotation/data/processed/crash.parquet"
    )

    # Vérification (optionnelle)
    print(df.head())
    print(df["Ticker"].unique())

    # ======================================================
    # 2) Préparer figure : un subplot par ticker
    # ======================================================
    tickers = df["Ticker"].unique()
    n = len(tickers)

    fig, axes = plt.subplots(
        nrows=n,
        ncols=1,
        figsize=(12, 3 * n),
        sharex=True
    )

    # Si un seul ticker → axes n’est pas une liste
    if n == 1:
        axes = [axes]

    # ======================================================
    # 3) Tracer chaque ticker
    # ======================================================
    for ax, t in zip(axes, tickers):
        sub = df[df["Ticker"] == t].sort_index()
        
        ax.plot(sub.index, sub["Close"], linewidth=1.8)
        ax.set_title(f"{t} — Price evolution during crash simulation", fontsize=12, fontweight="bold")
        ax.set_ylabel("Price")
        ax.grid(True, alpha=0.2)

    axes[-1].set_xlabel("Date")

    plt.tight_layout()

    # ======================================================
    # 4) Sauvegarde en PNG
    # ======================================================
    output_path = "/Users/benjaminvissac/Documents/GitHub/factor-rotation/report/backtests_charts/S3_R8_crash_simulation.png"
    plt.savefig(output_path, dpi=300)

    print(f"✅ Figure saved at:\n{output_path}")
