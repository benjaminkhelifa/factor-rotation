# factor-rotation
Sector rotation analysis and backtesting project (Python)
# 🧠 Factor Rotation Project

This project aims to analyze and backtest a **sector rotation strategy** using Python.

The goal is to understand **when and why an investor might reallocate their portfolio across sectors**, based on quantitative indicators such as momentum, volatility, and other factors.

---

## 🎯 Objective

- Collect and clean sector ETF data (free from Yahoo Finance)
- Build financial indicators (momentum, volatility, etc.)
- Test allocation rules through backtesting
- Produce performance reports and visualizations
- Automate report generation (PDF)

---

## 📊 Context

In financial markets, sectors do not perform equally over time.  
Technology often outperforms during expansion phases, while healthcare and utilities are more resilient during recessions.  
This project studies how a dynamic allocation between sectors could improve portfolio performance and reduce risk compared to a static allocation.

---

## 📁 Project Structure
factor-rotation/
├─ data/              # Raw and processed data
│  ├─ raw/
│  └─ processed/
├─ notebooks/         # Jupyter notebooks (EDA, modeling, backtest)
├─ src/               # Source code (data.py, features.py, etc.)
├─ tests/             # Unit tests
├─ report/            # Generated figures and final report
├─ requirements.txt   # Python dependencies
└─ README.md
---

## ⚙️ Tools and Libraries

- Python (3.10+)
- pandas, numpy, matplotlib, statsmodels, scikit-learn
- yfinance (data source)
- pytest (testing)

---

## 🧩 Methodology Overview

1. **Data Collection** → Download historical sector ETF prices (Yahoo Finance)
2. **Feature Engineering** → Compute financial signals (momentum, volatility, etc.)
3. **Modeling** → Run rolling regressions to estimate factor exposure
4. **Backtesting** → Simulate monthly rebalancing strategies and compare results
5. **Reporting** → Generate performance charts, metrics, and a final PDF report

---

## 📈 Expected Outputs

- Cleaned datasets (`data/processed/`)
- Visualizations (performance, correlations, drawdowns)
- Backtest results (CAGR, volatility, Sharpe ratio)
- Automated report (`report/report.pdf`)

---

## 👤 Author

**Ben**  
Project start: October 2025  
Status: **Day 1 – Structure setup ✅**

---

