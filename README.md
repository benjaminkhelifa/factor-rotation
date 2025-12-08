# **Portfolio Rotation Engine**
**Dynamic Cross-Asset Analysis • Multi-Frequency Signals • Automated Financial Reporting (PDF)**

The **Portfolio Rotation Engine** is a dynamic, adaptive analytics system designed to evaluate assets across equities, ETFs, crypto, and forex through a unified multi-layer signal-processing pipeline.

Unlike traditional sector-rotation backtests, this engine produces **context-aware diagnostics**, **risk assessments**, **momentum structures**, and **volatility regime detection** at any frequency (daily, weekly, monthly).

It automatically generates a full financial report (PDF) including metrics, visualizations, interpretations, and scenario-based insights.

---

## **Core Objectives**

The engine is built to:

- Process heterogeneous asset classes (stocks, ETFs, crypto, forex).
- Adapt dynamically to frequency constraints and observation depth.
- Compute short-term and long-term indicators (returns, volatility, momentum).
- Detect volatility regimes (subdued → turbulent).
- Infer behavioral profiles (defensive, dynamic, speculative, high-beta…).
- Generate a structured PDF report with charts, diagnostics, and commentary.
- Provide stable, interpretable signals even in noisy or incomplete markets.

The system remains robust under **low liquidity**, **data gaps**, **flash-crash effects**, and **young tickers with limited history**.

---

```md
## Project Structure

factor-rotation/
├─ data/
│  ├─ raw/            # User-managed inputs (e.g., enriched tickers CSV)
│  └─ processed/      # Parquet data downloaded + cleaned by the engine
├─ notebooks/         # Exploratory analysis, validation, prototypes
├─ src/               # Core engine (data ingestion, indicators, profiling, report builder)
├─ report/
│  ├─ backtests/      # Scenario-specific stress and validation tests
│  └─ outputs/        # Generated PDF reports
├─ tests/             # (Reserved) future unit tests
├─ requirements.txt
└─ README.md

---
```
## **Methodology Overview**

### **1. Data Ingestion**
- Automatic download from Yahoo Finance  
- Cleaning & resampling  
- Frequency inference  
- Parquet caching for reproducibility  

### **2. Feature Extraction**
- Multi-horizon returns  
- Volatility signatures  
- Momentum curvature (ST/LT consistency)  
- Stress metrics (ΔReturn, Volatility Ratio, Momentum Ratio)  

### **3. Profiling Engine**
- Liquidity buckets (very_liquid → illiquid)  
- Beta-driven and market-cap classification  
- Dynamic vs defensive behavioral profiles  
- Volatility regimes (subdued → turbulent)  

### **4. Scenario Engine**
- Cross-dimensional consistency checks  
- Fallback logic when signals conflict  
- Robustness to anomalies, jumps, and missing data  

### **5. Report Generation**
- Automated PDF including:
  - KPI tables  
  - Momentum & return charts  
  - Rotation metrics  
  - Macro-profile inference  
  - Auto-generated commentary blocks  

---

## **Expected Outputs**

- Clean structured datasets (`data/processed/...`)
- Diagnostic tables (returns, risk, ratios)
- Visualizations (momentum curves, volatility regimes, long/short mismatch)
- Fully automated analytical PDF reports
- Stress tests & backtests under multiple scenarios

---

## **Tools & Libraries**

- Python 3.10+
- pandas, numpy  
- matplotlib  
- yfinance  
- reportlab  

---

## **Author**

**Benjamin Khelifa**  
Project start: **September 2025**  
Scope: *Dynamic multi-asset rotation engine & analytical reporting system*

---

## How to Run the Project
> This project requires **Python 3.10+**
>
> 
### 1. Clone the repository

```bash
git clone https://github.com/benjaminkhelifa/factor-rotation.git
cd factor-rotation
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows activation
.\venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate a report

```bash
python src/report_builder.py
```

The generated PDF will appear in:

```
report/outputs/
```