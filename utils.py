import re
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
import numpy as np

def create_fiscal_quarter_mapper(financial_data_path):
    """
    Creates a function that maps dates to fiscal quarters based on a company's financial data.
    
    Args:
        financial_data_path: Path to the financial data CSV file with fiscal year markers
    
    Returns:
        A function that takes a date and returns the fiscal year and quarter
    """
    # Read the financial data
    df = pd.read_csv(financial_data_path)
    
    # Extract fiscal year information
    fiscal_years = {}
    current_fiscal_year = None
    fiscal_year_pattern = r"Financial Year: (\d{2}-[A-Za-z]+-\d{4})"
    
    for index, row in df.iterrows():
        # Check any column that might contain the fiscal year marker
        match = re.search(fiscal_year_pattern, row["Date"])
        if match:
            current_fiscal_year = datetime.strptime(match.group(1), '%d-%b-%Y')
            fiscal_years[current_fiscal_year] = []
            continue
        
        if current_fiscal_year:
            current_quarter_date = datetime.strptime(row.get('Date.1'), '%d-%b-%Y')
            
            # Calculate difference in months
            month_diff = (current_fiscal_year.year - current_quarter_date.year) * 12 + (current_fiscal_year.month - current_quarter_date.month)
            
            # Determine quarter based on month difference
            if month_diff == 0:  # Same month as fiscal year end
                qtr = 4
            elif month_diff == 3:  # 3 months before fiscal year end
                qtr = 3
            elif month_diff == 6:  # 6 months before fiscal year end
                qtr = 2
            elif month_diff == 9:  # 9 months before fiscal year end
                qtr = 1
            else:
                qtr = 0  # Error or special case
                
            # Store the quarter date with its fiscal quarter info
            quarter_info = {
                'quarter date': current_quarter_date,
                'fiscal_year': current_fiscal_year,
                'quarter': qtr
            }
            fiscal_years[current_fiscal_year].append(quarter_info)
    return fiscal_years




def forecast_vehicle_count_arimax(
    df,
    company_name,
    exog_vars,
    train_end_date='2024-09-30',
    forecast_end_date='2025-03-01',
    order=(1, 1, 1),
    seasonal_order=(2, 1, 0, 12)
):
    """
    Fits SARIMAX model and forecasts vehicle count for a specific company.

    Parameters:
    - df: Pandas DataFrame with company time series data
    - company_name: str, name of the company to filter
    - exog_vars: list of column names to use as exogenous variables
    - train_end_date: str, end of training data (format: 'YYYY-MM-DD')
    - forecast_end_date: str, end of forecasting range
    - order: tuple, ARIMA (p,d,q)
    - seasonal_order: tuple, Seasonal (P,D,Q,s)

    Returns:
    - forecast_plot: matplotlib plot of forecast vs actual
    - results_df: DataFrame with Forecasted and Actual values
    """

    # Training data
    df_train = df[(df['company'] == company_name) & (df['date'] < train_end_date)].copy()
    df_train.set_index('date', inplace=True)
    df_train.sort_index(inplace=True)

    y_train = df_train['vehicle_count']
    X_train = df_train[exog_vars]

    # Fit model
    model = SARIMAX(
        y_train, exog=X_train, order=order, seasonal_order=seasonal_order,
        enforce_stationarity=False, enforce_invertibility=False
    )
    model_fit = model.fit(disp=False)

    print(model_fit.summary())

    # Validation / forecast period
    df_forecast = df[(df['company'] == company_name) & 
                     (df['date'] >= train_end_date) & 
                     (df['date'] <= forecast_end_date)].copy()

    df_forecast.set_index('date', inplace=True)
    df_forecast.sort_index(inplace=True)

    X_future = df_forecast[exog_vars]
    y_actual = df_forecast['vehicle_count']

    # Forecast
    forecast = model_fit.forecast(steps=len(X_future), exog=X_future)

    # Combine results
    results = pd.DataFrame({
        'Forecasted': forecast,
        'Actual': y_actual
    })

    
    # MAPE
    mape = mean_absolute_percentage_error(results['Actual'], results['Forecasted']) * 100  # in %

    # RMSE
    rmse = np.sqrt(mean_squared_error(results['Actual'], results['Forecasted']))

    # Print results
    print(f"MAPE: {mape:.2f}%")
    print(f"RMSE: {rmse:.2f}")

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(results.index, results['Actual'], label='Actual', marker='o')
    plt.plot(results.index, results['Forecasted'], label='Forecasted', marker='x')
    plt.title(f'ARIMAX Forecast vs Actual ({company_name})')
    plt.xlabel('Date')
    plt.ylabel('Vehicle Count')
    plt.legend()
    plt.grid(True)
    plt.show()

    return results
