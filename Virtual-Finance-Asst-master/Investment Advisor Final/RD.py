def convert_to_years_months(duration):
    years = int(duration)
    months = int((duration - years) * 12)
    return years, months

def calculate_RD_return(monthly_investment, duration_years, duration_months):
    quarterly_interest_rate_RD = 0.067 / 4
    total_months = duration_years * 12 + duration_months
    
    # Calculate the monthly investment amount
    monthly_investment_amount = monthly_investment / total_months
    
    # Calculate the total investment
    total_investment_RD = monthly_investment_amount * total_months
    
    quarters = total_months // 3
    expected_return_RD = total_investment_RD * ((1 + quarterly_interest_rate_RD) ** quarters)
    return "5-Year Recurring Deposit Account", expected_return_RD, total_investment_RD, total_months, monthly_investment_amount

# Main function for RD calculation
def main_RD():
    while True:
        try:
            monthly_investment = float(input("Enter the investment amount:"))
            duration = float(input("Enter the investment duration (in years 1-5): "))
            if duration < 1 or duration > 5:
                raise ValueError("Duration must be between 1 and 5 years")
            break  # If input conversion is successful and duration is valid, break the loop
        except ValueError as e:
            print("Invalid input:", e)

    duration_years, duration_months = convert_to_years_months(duration)

    rd_account, expected_return_RD, total_investment_RD, total_months, monthly_investment_amount = calculate_RD_return(monthly_investment, duration_years, duration_months)
    print("Monthly investment amount: {} rupees".format(monthly_investment_amount))
    print("{} Expected return is: {} rupees".format(rd_account, expected_return_RD))
    print("Total amount to deposit in Recurring Deposit Account: {} rupees over {} months".format(total_investment_RD, total_months))

if __name__ == "__main__":
    main_RD()
