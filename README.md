# 📊 Dataset Overview

Three distinct datasets to investigate the relationship between national car registration trends and the quarterly financial performance and stock prices of selected automotive companies listed on Bursa Malaysia. The goal is to explore whether vehicle registration data—available prior to quarterly earnings announcements—can serve as a predictive indicator of financial or stock price movements.

## 🏢 Companies Covered

The following publicly listed automotive companies are included in the analysis:

| Company Name                  | Bursa Stock Code |
|------------------------------|------------------|
| DRB-HICOM Berhad             | 1619             |
| Sime UMW Holdings Berhad     | 4588             |
| Bermaz Auto Berhad           | 5248             |
| Sime Darby Berhad            | 4197             |
| Tan Chong Motor Holdings Bhd | 4405             |

These companies represent key players in Malaysia’s automotive industry, covering vehicle assembly, distribution, and sales.

## 🗓 Time Range and Coverage

| Dataset                   | Time Frame                  | Remarks                                                                 |
|---------------------------|-----------------------------|-------------------------------------------------------------------------|
| Vehicle Registration      | Jan 2023 – Mar 2025         | Monthly data from JPJ/DOSM, used as industry proxy                      |
| Quarterly Financials      | Full historical results     | All available quarters; Sime UMW available up to Feb 2024 (manual input possible) |
| Stock Prices              | Matches financials dataset  | Daily or quarterly-closing data aligned with financial result periods   |

Each dataset is time-aligned to facilitate correlation and trend analysis across reporting cycles.

## 📁 Dataset Structure

The data is structured and stored as follows:

- **Quarterly Financials**: Contains company-specific historical financial metrics on a quarterly basis, indexed by stock code and quarter-end date.
- **Stock Prices**: Comprises historical stock prices for each company, aligned with earnings reporting periods for comparative analysis.
- **Vehicle Registration Data**: Provides national monthly registration counts, categorized by vehicle type, representing sector-level demand signals.

All datasets include the necessary timestamp and identifier fields (e.g., dates, stock codes) to enable merging and analysis without the need for data imputation or complex transformation.

## 🛠️ Data Extraction & Scraping Process

All datasets in this project are programmatically extracted and kept up-to-date using reproducible scripts and notebooks:

### 1. Vehicle Registration Data

- **Source:** [data.gov.my](https://data.gov.my/data-catalogue/registration_transactions_car)
- **Method:** The notebook [`data-extraction.ipynb`](data-extraction.ipynb) uses `pandas` to directly download and process Parquet files for each year (2023–2025). The script converts registration dates to datetime format and saves the cleaned data locally in the `data/` folder.

### 2. Quarterly Financial Results

- **Source:** [i3investor.com](https://klse.i3investor.com/)
- **Method:** The notebook leverages `selenium` (headless Chrome) and `BeautifulSoup` to automate browsing and scrape quarterly financial tables for each company. Data is parsed into `pandas` DataFrames and saved as both CSV and Parquet files in `data/quarterly_financials/`.

### 3. Stock Price Data

- **Source:** [Yahoo Finance](https://finance.yahoo.com/) via `yfinance` Python package.
- **Method:** The notebook downloads daily historical stock prices for each company using their Bursa Malaysia stock codes. Data is saved as CSV and Parquet in `data/stock_prices/`. For delisted stocks (e.g., Sime UMW post-Feb 2025), data is manually downloaded from [investing.com](https://www.investing.com/equities/umw-holdings-bhd-historical-data).

All scripts are located in [`data-extraction.ipynb`](data-extraction.ipynb) and are designed for easy re-execution to refresh the datasets as new data becomes available.