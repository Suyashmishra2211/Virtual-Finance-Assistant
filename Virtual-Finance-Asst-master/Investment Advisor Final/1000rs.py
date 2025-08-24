# Importing required modules
import FD_calculator as fd
import gold_calculator as gold
import TD as td
import RD as rd
import sip_calculator as sip
import stock_investment_calculator as stock

# Function to calculate returns for each investment type
def calculate_returns():
    # Fixed Deposit Calculator
    print("Please Enter the Values for Fixed Deposit:")
    while True:
        try:
            principal_fd = float(input("Enter the principal amount (₹): "))
            break  # Exit the loop if conversion to float is successful
        except ValueError:
            print("Invalid input. Please enter a valid number for the principal amount.")
    
    # Loop until a valid input for annual interest rate is provided
    while True:
        try:
            rate_fd = float(input("Enter the annual interest rate (%): "))
            break  # Exit the loop if conversion to float is successful
        except ValueError:
            print("Invalid input. Please enter a valid number for the annual interest rate.")
    
    duration_str = input("Enter the duration : ")
    duration_days = fd.convert_to_days(duration_str)
    
    # Loop until a valid input for monthly interest payout is provided
    while True:
        monthly_payout_str = input("Do you want monthly interest payout? (yes/no): ").lower()
        if monthly_payout_str in ["yes", "no"]:
            monthly_payout_fd = monthly_payout_str == "yes"
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
    fd_return = fd.calculate_fd_maturity(principal_fd, rate_fd, duration_days, monthly_payout_fd == "yes")

    # Gold Investment Calculator
    print("Please Enter the Values for Gold Investment:")
    while True:
        try:
            amount_inr = float(input("Enter the amount you want to invest in gold (INR): "))
            duration_str = input("Enter the duration : ")

            # Parse duration string
            duration, unit = gold.parse_duration(duration_str)

            if duration is None or unit is None or duration <= 0:
                print("Please enter a valid duration.")
                continue

            # Convert duration to days
            days = int(gold.convert_to_days(duration, unit))  # Convert to integer

            if amount_inr <= 0 or days <= 0:
                print("Please enter a valid amount and duration.")
                continue

            # Get current gold price in INR
            current_gold_price_inr = gold.get_gold_price()

            # Calculate total value and profit based on the current gold price
            total_value_inr, profit_inr = gold.gold_investment(amount_inr, days, current_gold_price_inr)

            if total_value_inr is not None and profit_inr is not None:
                gold_return=total_value_inr
            else:
                print("Failed to calculate investment. Please try again later.")

            break  # Exit the loop if all inputs are valid

        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Calculate expected returns for TD
    print("Please Enter the Values for Time Deposit Account:")
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

    # Calculate the TD type using duration
    td_type = str(duration_years)

    td_account, td_return = td.calculate_TD_return(investment_amount, duration_years, duration_months, td_type)

    #Calculate the RD account
    print("Please Enter the Values for recurring deposit account:")
    while True:
        try:
            monthly_investment = float(input("Enter the investment amount:"))
            duration = float(input("Enter the investment duration (in years 1-5): "))
            if duration < 1 or duration > 5:
                raise ValueError("Duration must be between 1 and 5 years")
            break  # If input conversion is successful and duration is valid, break the loop
        except ValueError as e:
            print("Invalid input:", e)
    duration_years, duration_months = rd.convert_to_years_months(duration)
    a,rd_return,x,y,z = rd.calculate_RD_return(monthly_investment, duration_years,duration_months)

    # SIP Calculator
    print("Please Enter the Values for Systematic Investment Plan:")
    while True:
        try:
            sip_amount = float(input("Enter monthly SIP amount : "))
            sip_duration = int(input("Enter investment duration in years : "))
            sip_rate = float(input("Enter expected annual rate of return : "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    future_value,total_value,sip_return = sip.sip_calculator(sip_amount, sip_duration, sip_rate)

    # Stock Investment Selector
    print("Please Enter the Values for Stock Investment:")
    while True:
        try:
            initial_investment = float(input("Enter your initial investment amount (in INR): "))
            duration_str = input("Enter the investment duration (e.g., 1 day, 3 months, 2 years): ")

            best_company, max_return = stock.find_best_company(initial_investment, duration_str)

            if best_company is not None:
                stock_return=max_return
                break
            else:
                stock_return=None
                break  # Exit the loop if calculation is unsuccessful
        except ValueError:
            print("Please enter a valid numeric value for the initial investment.")


    # Printing returns for each investment type
    print("\nReturns for each investment type:")
    print("1. Fixed Deposit: ₹", fd_return)
    print("2. Gold Investment: ₹", gold_return)
    print("3. Time Deposit: ₹", td_return)
    print("4. Recurring Deposit: ₹", rd_return)
    print("5. SIP: ₹", sip_return)
    print("6. Stock Investment: ₹", stock_return)

    # Determining the most profitable option
    max_return = max(fd_return, gold_return, td_return, sip_return, stock_return)
    options = {
        fd_return: "Fixed Deposit",
        gold_return: "Gold Investment",
        td_return: "Time Deposit",
        sip_return: "SIP",
        stock_return: "Stock Investment",
        rd_return: "Recurring Deposit"
    }
    print("\nThe most profitable investment type is:", options[max_return])
    print("With a return value of ₹", max_return)


# Main function
if __name__ == "__main__":
    calculate_returns()