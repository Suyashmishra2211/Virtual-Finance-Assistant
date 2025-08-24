import yfinance as yf

# Mapping dictionary for ticker symbols to company names (without .NS)
ticker_company_mapping = {
    "RELIANCE": "Reliance Industries Limited",
    "TCS": "Tata Consultancy Services Limited",
    "HDFCBANK": "HDFC Bank Limited",
    "ICICIBANK": "ICICI Bank Limited",
    "BHARTIARTL": "Bharti Airtel Limited",
    "SBIN": "State Bank of India",
    "INFY": "Infosys Limited",}

def convert_to_days(duration_str):
    duration, unit = duration_str.split(" ")
    duration = float(duration)
    if unit.lower() == 'day' or unit.lower() == 'days' or unit.lower() == 'da':
        return duration
    elif unit.lower() == 'month' or unit.lower() == 'months' or unit.lower() == 'mon':
        return duration * 30  # Assuming 1 month = 30 days
    elif unit.lower() == 'year' or unit.lower() == 'years' or unit.lower() == 'yea':
        return duration * 365  # Assuming 1 year = 365 days
    else:
        return 0  # Invalid unit

def get_current_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        current_price = stock.history(period='1d')['Close'].iloc[-1]
        return current_price
    except Exception as e:
        print(f"Error fetching current price: {e}")
        return None

def get_historical_data(ticker, period):
    try:
        data = yf.download(ticker, period=period, progress=False)
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_expected_return(data, current_price, initial_investment, duration_days):
    try:
        # Check if the current price is greater than the initial investment
        if current_price > initial_investment:
            return None

        # Calculate daily returns
        data['Daily_Return'] = data['Adj Close'].pct_change()

        # Remove NA values
        data.dropna(inplace=True)

        # Calculate cumulative returns over the specified period
        cumulative_return = (1 + data['Daily_Return']).cumprod().iloc[-1]

        # Calculate investment value after the duration based on cumulative return
        investment_value = initial_investment * cumulative_return

        return investment_value
    except Exception as e:
        print(f"Error calculating return: {e}")
        return None

def find_best_company(initial_investment, duration_str):
    num_companies = len(ticker_company_mapping)
    processed_companies = 0

    max_return = -1
    best_company = None

    duration_days = convert_to_days(duration_str)

    for ticker, company_name in ticker_company_mapping.items():
        ticker_with_extension = f"{ticker}.NS"
        period = '1mo'  # Historical data period of 1 month

        data = get_historical_data(ticker_with_extension, period)
        if data is not None:
            current_price = get_current_price(ticker_with_extension)
            if current_price is not None:
                investment_value = calculate_expected_return(data, current_price, initial_investment, duration_days)

                if investment_value is not None and investment_value > max_return:
                    max_return = investment_value
                    best_company = company_name
            else:
                print(f"Failed to fetch current price for {company_name}.")
        else:
            print(f"Failed to fetch historical data for {company_name}.")

        processed_companies += 1
        progress = (processed_companies / num_companies) * 100
        print(f"\rProgress: {progress:.2f}% ({processed_companies}/{num_companies})", end='')

    print()  # New line after the progress bar

    if best_company is not None:
        return best_company, max_return
    else:
        return None, None

def main():
    print("Welcome to the Stock Investment Advisor!")
    print("----------------------------------------")
    
    while True:
        try:
            initial_investment = float(input("Enter your initial investment amount (in INR): "))
            duration_str = input("Enter the investment duration (e.g., 1 day, 3 months, 2 years): ")

            best_company, max_return = find_best_company(initial_investment, duration_str)

            if best_company is not None:
                print(f"The best company to invest in for a {duration_str} investment period with an initial investment of ₹{initial_investment} is {best_company}.")
                print(f"Expected return after {duration_str}: ₹{max_return:.2f}")
                break  # Exit the loop if calculation is successful
            else:
                print("Sorry, unable to find the best company for your investment.")
                break  # Exit the loop if calculation is unsuccessful
        except ValueError:
            print("Please enter a valid numeric value for the initial investment.")

if __name__ == "__main__":
    main()
