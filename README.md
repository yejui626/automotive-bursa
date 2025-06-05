# 📊 Automotive Bursa Malaysia: Data & Exploratory Analysis Overview

This project investigates the relationship between national car registration trends and the quarterly financial performance and stock prices of selected automotive companies listed on Bursa Malaysia. The core objective is to explore whether vehicle registration data—available prior to quarterly earnings announcements—can serve as a predictive indicator of financial or stock price movements.

---
## 📌 Industry Problem & Business Context

### 🏭 Industry Problem Statement

**How do macroeconomic conditions affect automotive sales performance and revenue generation across competing manufacturers and distributors in Malaysia?**

This project investigates whether publicly available macroeconomic indicators—such as monthly vehicle registration data, inflation (Cars CPI), and labour force statistics—can be used as predictive tools for company-level financial outcomes, particularly quarterly revenue.

---

### 📈 Business Context & Relevance

In Malaysia’s automotive industry, public-listed companies such as **Sime Darby**, **DRB-HICOM**, and **Bermaz Auto** face a significant forecasting challenge. Their financial performance is directly influenced by macroeconomic conditions that affect consumer behavior, purchasing power, and financing capacity.

Key macroeconomic variables include:

- **Overnight Policy Rate (OPR):** Affects loan affordability for auto financing, which in turn influences demand.
- **Consumer Price Index (Cars CPI):** Reflects vehicle price changes and inflationary pressures, which affect affordability and margins.
- **Labour Force Statistics:** Employment levels, participation rates, and unemployment rates serve as proxies for disposable income and consumer confidence.

---

### 🔍 Opportunity: Addressing a Structural “Information Gap”

A potential **information asymmetry** exists in how frequently data is reported:

- **Macroeconomic data** (e.g., vehicle registration, CPI, labour force statistics) is updated **monthly** by DOSM.
- **Company financials (QR results)** are published **quarterly**, typically 6–8 weeks after a quarter ends.

This time gap presents a **predictive window**, where macro-level signals (available in advance) may be used to forecast:

- Near-term vehicle registration trends
- Upcoming company revenue
- Investor expectations vs. actual performance

This creates a strong use case for leveraging **data analytics** in investment research, sector analysis, and even earnings prediction models.

---

### 💼 Financial & Strategic Applications

From a financial services or investment banking perspective, this study supports:

- **Sector Outlook Analysis:** Gauge market demand sensitivity to policy and economic conditions.
- **Earnings Forecasting:** Estimate company revenues ahead of quarterly disclosures.
- **Equity Research Models:** Generate investment insights by correlating macro signals with firm-level KPIs.
- **Credit Risk Evaluation:** Use leading indicators to anticipate financial stress or performance downturns.
  
---

## 🏢 Companies Covered

| Company Name                  | Bursa Stock Code |
|------------------------------|------------------|
| DRB-HICOM Berhad             | 1619             |
| Sime UMW Holdings Berhad     | 4588             |
| Bermaz Auto Berhad           | 5248             |
| Sime Darby Berhad            | 4197             |
| Tan Chong Motor Holdings Bhd | 4405             |

These companies represent key players in Malaysia’s automotive industry, covering vehicle assembly, distribution, and sales.

---

## 🗓 Time Range and Coverage

| Dataset                   | Time Frame                  | Remarks                                                                 |
|---------------------------|-----------------------------|-------------------------------------------------------------------------|
| Vehicle Registration      | Jan 2018 – Mar 2025         | Monthly data from JPJ/DOSM, used as industry proxy                      |
| Quarterly Financials      | Full historical results     | All available quarters; Sime UMW available up to Feb 2024 (manual input possible) |
| Stock Prices              | Matches financials dataset  | Daily or quarterly-closing data aligned with financial result periods   |
| Macroeconomic Indicators  | Jan 2018 – Mar 2025         | Monthly CPI, BNM OPR, Labour Force Statistics                           |

All datasets are time-aligned to facilitate correlation and trend analysis across reporting cycles.

---

## 📁 Data Structure & Extraction

- **Vehicle Registration Data**: Monthly registration counts by company, derived from DOSM/JPJ data (2018–2025). Data is cleaned, mapped to public-listed companies, and available at both daily and monthly granularity.
- **Quarterly Financials**: Company-specific historical financial metrics on a quarterly basis, scraped from i3investor and cleaned for analysis.
- **Stock Prices**: Daily and quarterly-closing prices for each company, sourced from Yahoo Finance (`yfinance`) and Investing.com for delisted stocks.
- **Macroeconomic Data**: Includes Consumer Price Index (CPI) for cars, Bank Negara Malaysia (BNM) Overnight Policy Rate (OPR), and Labour Force Statistics, all merged at monthly frequency.

All extraction and cleaning scripts are in [`data-extraction.ipynb`](data-extraction.ipynb) and [`data-preparation.ipynb`](data-preparation.ipynb). Data is stored in the `data/` directory, with subfolders for each dataset.

---

## 🛠️ Data Extraction & Processing Workflow

1. **Vehicle Registration**:  
   - Downloaded as Parquet files per year from [data.gov.my](https://data.gov.my/data-catalogue/registration_transactions_car).
   - Cleaned, mapped to listed companies, and aggregated to daily/monthly counts ([`data-preparation.ipynb`](data-preparation.ipynb)).

2. **Quarterly Financials**:  
   - Scraped using Selenium and BeautifulSoup from [i3investor.com](https://klse.i3investor.com/).
   - Cleaned and merged into a master CSV for all companies.

3. **Stock Prices**:  
   - Downloaded via `yfinance` for each Bursa stock code.
   - Delisted stocks (e.g., Sime UMW post-Feb 2025) are manually downloaded.

4. **Macroeconomic Data**:  
   - CPI for cars and Labour Force Statistics from DOSM.
   - BNM OPR rates manually compiled and forward-filled to monthly frequency.

5. **Data Merging**:  
   - All datasets are merged on date (monthly or quarterly) for unified analysis.

---

## 🔎 Exploratory Data Analysis (EDA) Highlights

### 1. Revenue vs Vehicle Registration

- **Strong Positive Correlation**:  
  All companies show strong positive correlations (ranging from 0.816 to 0.971) between vehicle registration volume and revenue.
    - **Tan Chong Motor Holdings Berhad**: Correlation ≈ 0.97 (almost linear relationship).
    - **DRB-HICOM Berhad**: Correlation ≈ 0.91.
    - **Sime UMW Holdings Berhad**: Correlation ≈ 0.90.
    - **Sime Darby Berhad**: Correlation ≈ 0.84.
    - **Bermaz Auto Berhad**: Correlation ≈ 0.82 (other factors like model mix, pricing, and government policy also play a role).

- **Operational KPI**:  
  Vehicle registration data is a leading indicator for revenue, allowing for early estimation of financial performance before quarterly results are published.

- **Company-Specific Insights**:  
  - **Tan Chong** and **DRB-HICOM**: Revenue is highly dependent on vehicle sales volume.
  - **Bermaz Auto**: Revenue influenced by vehicle count and other factors (e.g., tax holidays, model launches).
  - **Sime Darby**: Slightly lower correlation due to diversified business segments.

### 2. Macroeconomic Factors

- **Merged Dataset**:  
  Monthly vehicle registration data is combined with macroeconomic indicators (CPI, OPR, Labour Force).
- **Correlation Analysis**:  
  - Vehicle count shows varying degrees of correlation with macroeconomic variables (e.g., CPI for cars, unemployment rate).
  - Exogenous variables (CPI, OPR, unemployment) are used in time series forecasting models.

### 3. Time Series Forecasting

- **SARIMAX/ARIMAX Models**:  
  - Used to forecast monthly vehicle registrations for each company, incorporating macroeconomic exogenous variables.
  - Models validated on recent periods (e.g., Oct 2024 – Mar 2025) show reasonable predictive performance.

### 4. Outlier & Event Analysis

- **Outliers**:  
  - Notable outliers (e.g., TCMH) often coincide with new model launches or government policy changes (e.g., tax holidays).
  - Suggests the value of incorporating event-based features in predictive models.

---

## 📂 Notebooks Overview

- [`data-extraction.ipynb`](data-extraction.ipynb): Data download, scraping, and initial cleaning.
- [`data-preparation.ipynb`](data-preparation.ipynb): Data merging, mapping, and preparation for analysis.
- [`eda/1. revenue-vs-vehicle_count-eda.ipynb`](eda/1.%20revenue-vs-vehicle_count-eda.ipynb): Analysis of the relationship between vehicle registrations and revenue.
- [`eda/2. macro-vs-vehicle_count-eda.ipynb`](eda/2.%20macro-vs-vehicle_count-eda.ipynb): Analysis of macroeconomic factors and time series forecasting.

---

## 📈 Key Takeaways

- **Vehicle registration data is a robust, timely operational KPI for forecasting automotive company revenue in Malaysia.**
- **Macroeconomic indicators provide additional explanatory power and can improve forecasting accuracy.**
- **The project’s reproducible pipeline enables ongoing updates and extension to new companies or macroeconomic variables.**

---
