def calculate_TD_return(investment_amount, duration_years, duration_months, td_type):
    # Interest rates for Post Office TD from 01.01.2024 to 31.03.2024
    interest_rates_TD = {
        "1.0": 0.069,  # 6.9% for 1 year TD
        "2.0": 0.07,   # 7.0% for 2 year TD
        "3.0": 0.071,  # 7.1% for 3 year TD
        "4.0": 0.071,  # 7.1% for 4 year TD (considered the same as 3 year TD)
        "5.0": 0.075   # 7.5% for 5 year TD
    }
    
    # Check if the TD type is valid
    if td_type not in interest_rates_TD:
        return "Invalid TD type", None
    
    # Convert duration to months
    total_months = duration_years * 12 + duration_months
    
    # Calculate expected return for TD
    rate = interest_rates_TD[td_type]
    quarterly_rate = rate / 4
    quarters = total_months // 3
    expected_return_TD = investment_amount * ((1 + quarterly_rate) ** quarters)
    
    return "{} Time Deposit Account".format(td_type.capitalize()), expected_return_TD

# Main function for TD calculation
def main_TD():
    while True:
        try:
            investment_amount = float(input("Enter the investment amount: "))
            break  # Break out of the loop if input is successfully converted to float
        except ValueError:
            print("Invalid input. Please enter a valid numeric value.")

    while True:
        try:
            duration_years = round(float(input("Enter the investment duration (in years 1-5): ")))  # Round off the duration
            if 1 <= duration_years <= 5:
                break  # Break out of the loop if input is within the valid range
            else:
                print("Duration should be between 1 and 5 years.")
        except ValueError:
            print("Invalid input. Please enter a valid numeric value.")

    duration_months = 0  # Assuming no months input for simplicity

    # Calculate the TD type based on the rounded off duration
    td_type = str(duration_years)

    td_account, expected_return_TD = calculate_TD_return(investment_amount, duration_years, duration_months, td_type)
    print("For an investment amount of {} rupees and an investment duration of {} years:".format(investment_amount, duration_years))
    print("Expected return : {} rupees".format(expected_return_TD))

if __name__ == "__main__":
    main_TD()
