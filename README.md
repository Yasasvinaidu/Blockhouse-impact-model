# Blockhouse Temporary Impact Modeling

This repository contains the solution to the Blockhouse Work Trial Task involving market microstructure modeling. Specifically, it focuses on modeling the **temporary market impact function** \( g_t(x) \) and formulating a share allocation strategy to minimize trading cost over time.

---

## 📄 Project Overview

This project addresses the following key components:

- **Empirical modeling** of slippage using limit order book (LOB) data.
- **Convex approximation** of the impact function using a power-law model:  
  \[
  g_t(x) = \alpha_t x^\delta
  \]
- **Optimization formulation** to determine how to allocate total trades across time steps to minimize execution cost.
- **Slippage simulation** across 390 time intervals using LOB snapshots for 3 stocks: **AMZN**, **MSFT**, and **GOOG**.

---

## 📁 Contents

| File / Folder               | Description                                                        |
|----------------------------|--------------------------------------------------------------------|
| `slippage_analysis.py`     | Python script for computing and plotting average slippage curves   |
| `Blockhouse_task.pdf`| Final compiled report summarizing approach and results             |
| `data/`                    | Provided LOB CSV files for 3 stocks (AMZN, MSFT, GOOG)             |
| `README.md`                | This documentation file                                            |

---

## 📊 Methodology Summary

### Temporary Impact Function

The slippage for a buy order of size \( x \) at time \( t \) is defined as:
\[
g_t(x) = \frac{\text{Cost}_t(x)}{x} - \text{Mid}_t
\]
where:
- \( \text{Mid}_t = \frac{\text{Best Ask}_t + \text{Best Bid}_t}{2} \)
- \( \text{Cost}_t(x) \) is computed from available liquidity in the top 5 ask levels.

A power-law curve is fitted to each minute's slippage curve:
\[
g_t(x) = \alpha_t x^{\delta}
\]

---

### Optimization Formulation

Given a total target volume \( S \) to execute over 390 intervals, we solve:

\[
\min_{\sum x_t = S,\, x_t \ge 0} \sum_{t=1}^{390} \alpha_t x_t^{1+\delta}
\]

This convex optimization problem yields an optimal execution schedule that minimizes total market impact.

---

## 📂 Data

LOB data for **AMZN**, **MSFT**, and **GOOG** was provided as part of the Blockhouse Task. Each file contains 390 one-minute snapshots of the order book with 5 levels of depth, formatted similarly to LOBSTER data.

---

## 📎 Author

**Yasasvi Naidu Vennela**  
This repository was created as part of the Blockhouse Work Trial Task and contains both implementation and analytical documentation.

---
