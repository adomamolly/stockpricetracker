# Quantitative Analytics & Stochastic Backtesting Engine

An end-to-end systematic trading pipeline and risk-validation workspace built in Python. The framework ingests raw market microstructure data, flattens relational dimensions to calculate real-time technical indicators, and cross-validates baseline trend-following strategies using a parallelized, high-performance stochastic simulation engine.

## 🚀 Core Architecture & Features

The workspace is structurally bifurcated into two independent, isolated analytical execution modes managed via a programmatic memory state machine (`st.session_state`):

### 📊 Mode A: Historical Ticker Analytics
* **Data Ingestion Pipeline:** Integrates with the `yfinance` API to fetch, process, and clean historical market equity intervals.
* **Dynamic Index Flattening:** Includes a robust translation layer designed to parse and flatten multi-level relational data blocks (`MultiIndex DataFrame`), converting hierarchical columns into clean, queryable data streams.
* **Signal Generation Matrix:** Computes a Dual Moving Average Crossover model using a 20-period Simple Moving Average (SMA) as the short-term momentum tracker and a 50-period Exponential Moving Average (EMA) as the structural trend baseline.

### 🎲 Mode B: Stochastic Strategy Validation (Monte Carlo Sandbox)
* **Synthetic Path Generation:** Employs continuous-time stochastic processes via **Geometric Brownian Motion (GBM)** to project thousands of independent asset lifetimes based on customizable expected drift ($\mu$) and annualized volatility ($\sigma$).
* **Vectorized Parallel Backtesting:** Bypasses slow, iterative Python loops by leveraging highly optimized 2D NumPy array matrices ($Time \times Paths$). The entire backtest matrix calculates performance returns natively in compiled C layers.
* **Risk Profile Distribution Modeling:** Maps complete probabilistic risk landscapes by generating density functions for strategy Sharpe Ratios, Maximum Portfolio Drawdowns (MDD), and alpha generation bounds across 500,000+ generated data points in $<150\text{ms}$.

---

## 🔬 Mathematical Framework

### 1. Exponential Smoothing Multiplier
To ensure immediate sensitivity to price inflection points without losing long-term trend context, the fast-moving signal calculates exponential weights using a recursive decay constant:

$$\alpha = \frac{2}{N + 1}$$

### 2. Asset Path SDE (Geometric Brownian Motion)
Synthetic market pricing structures are simulated using the classical stochastic differential equation:

$$dS_t = \mu S_t dt + \sigma S_t dW_t$$

Where $dW_t$ represents a standard Wiener process drawn randomly from a normal distribution matrix $N(0, dt)$.

---

## 🛠️ Tech Stack

* **Language:** Python 3.13
* **Mathematical Operations:** NumPy (Vectorized array manipulation), Pandas (Time-series data frames)
* **Data Extraction:** yFinance API
* **Data Visualization:** Plotly Express / Graph Objects (Interactive charts)
* **Interface Architecture:** Streamlit (State-managed web implementation)

---

## 📁 Repository Structure

```text
stochastic-backtest-engine/
│
├── visuals/
│   ├── mainc.py           # Application mainframe and conditional state router
│   └── sidebar_layout.py  # Isolated, firewall-protected input widget mapping
│
├── src/
│   ├── __init__.py        # Package initialization node
│   ├── fetch.py           # MultiIndex extraction and data cleaning layer
│   ├── indicators.py      # Core math formulas & vectorized simulation arrays
│   └── metrics.py         # Descriptive analytics and risk aggregation loops
│
├── requirements.txt       # Software and environment dependencies
└── README.md              # System specification sheet