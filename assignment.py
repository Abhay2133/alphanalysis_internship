# ### Assignment
# 
# 1. Accept input from user for data period and investment amount 
# 2. Use trading view/Yahoo finance API to fetch required daily candle data
# 3. Once data is fetched, workout amount to be invested in each stock by multiplying stock weightage with investment amount. 
# 4. Calculate number of shares that can be bought with this amount by dividing it with daily closing price. You will get number of shares that can be bought for that stock for that particular day.
# 5. Likewise need to be done for all stocks in input sheet for all dates of user input
# 

import pandas as pd
import yfinance as yf


# ### Step 1: Load stocks data
# 
# Loading csv data into pandas Dataframe and cleaning the Ticker values by appending `.NS` for Indian Stock market query



stocks = pd.read_csv('Stocks.csv').iloc[:, :2]
stocks.columns = ['Ticker', 'Weightage']

# Append `.NS` to tickers for Indian stock market
stocks['Ticker'] = stocks['Ticker'] + '.NS'


# ### Step 2: Get user input
# 
# Taking 3 user input 
#  - `start_date`        : The starting of period the user start investing
#  - `end_date`          : The ending of period the user last invests
#  - `investment_amount` : The amount of money user is going to invest each day



start_date = input("Enter start date (YYYY-MM-DD): ")
end_date = input("Enter end date (YYYY-MM-DD): ")
investment_amount = float(input("Enter total investment amount: "))

# data for teseting

# start_date = "2023-04-24"
# end_date = "2023-04-26"
# investment_amount = 10000000.01 


# #### Step 2.1 : Utility Function to generate list of dates for columns
# 
# date format : `YYYY-MM-DD`
# 
# This format also match the format of `yfinance` api
# 


from datetime import datetime, timedelta

def generate_date_list(start_date, end_date):
    """
    Generate a list of dates between two given dates.
    
    Args:
        start_date (str): The start date in "YYYY-MM-DD" format.
        end_date (str): The end date in "YYYY-MM-DD" format.
    
    Returns:
        list: A list of dates in "YYYY-MM-DD" format.
    """
    # Convert strings to datetime objects
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    # Generate list of dates
    date_list = []
    current_date = start
    while current_date <= end:
        date_list.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
    
    return date_list

dates = generate_date_list(start_date, end_date)
print(dates)



# ### Step 3: Fetch stock data
# 
# Fetching stock data from yahoo finance api and calcuting the shares based on weightage and closing_price


# incrementing end_date by 1 day for yfinance exclusive range
end_date = datetime.strptime(end_date, "%Y-%m-%d")
end_date += timedelta(days=1)
end_date = end_date.strftime("%Y-%m-%d")

results = []
# dates = []
for index, row in stocks.iterrows():
    ticker = row['Ticker']
    weightage = row['Weightage']
    stock_investment = investment_amount * weightage

    try:
        # Fetch stock data
        data = yf.download(ticker, start=start_date, end=end_date)
        _shares = {key:0 for key in dates}

        for date, daily_data in data.iterrows():
            _date =  date.strftime("%Y-%m-%d")
            closing_price = float(daily_data['Close']._values[0])
            shares = stock_investment / closing_price
            _shares[_date] = shares

        results.append({"Ticker":ticker, "Weightage":weightage, **_shares})
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")


# ### Step 4: Write results to Excel


date = dates[0]
print(str(date).split(' ')[0])



output_df = pd.DataFrame(results)
print(output_df.head())
output_df.to_csv('Investment_Results.csv', index=False)

print("Results saved to Investment_Results.xlsx")


