def calculate_fd_maturity(principal, annual_interest_rate, duration_days, monthly_payout=False):
    # Convert annual interest rate to decimal
    interest_rate_decimal = annual_interest_rate / 100
    
    duration_years = duration_days / 365  # Convert duration to years
    
    if duration_years <= 0.5:  # If duration is 6 months or less
        # Calculate maturity amount using simple interest
        maturity_amount = principal * (1 + interest_rate_decimal * duration_years)
    else:
        if monthly_payout:
            # Calculate interest for entire term upfront (discounted rates)
            total_interest = principal * interest_rate_decimal * duration_years
            # Divide by 12 for monthly payout
            monthly_interest = total_interest / 12
            # Maturity amount is principal plus total interest
            maturity_amount = principal + total_interest
        else:
            # Calculate maturity amount using compound interest formula
            maturity_amount = principal * (1 + interest_rate_decimal) ** duration_years
    
    return maturity_amount

def convert_to_days(duration_str):
    while True:
        try:
            duration, unit = duration_str.split(" ")
            duration = float(duration)
            if unit.lower() == 'day' or unit.lower() == 'days' or unit.lower() == 'da':
                return duration
            elif unit.lower() == 'month' or unit.lower() == 'months' or unit.lower() == 'mon':
                return duration * 30  # Assuming 1 month = 30 days
            elif unit.lower() == 'year' or unit.lower() == 'years' or unit.lower() == 'yea':
                return duration * 365  # Assuming 1 year = 365 days
            else:
                print("Invalid unit. Please provide the duration with a valid unit.")
                duration_str = input("Enter the duration (e.g., 1 day, 3 months, 2 years): ")
        except ValueError:
            print("Invalid format. Please provide the duration in the correct format.")
            duration_str = input("Enter the duration (e.g., 1 day, 3 months, 2 years): ")

def main():
    print("Fixed Deposit Calculator")
    print("-----------------------------")
    
    # Loop until a valid input for principal amount is provided
    while True:
        try:
            principal = float(input("Enter the principal amount (₹): "))
            break  # Exit the loop if conversion to float is successful
        except ValueError:
            print("Invalid input. Please enter a valid number for the principal amount.")
    
    # Loop until a valid input for annual interest rate is provided
    while True:
        try:
            annual_interest_rate = float(input("Enter the annual interest rate (%): "))
            break  # Exit the loop if conversion to float is successful
        except ValueError:
            print("Invalid input. Please enter a valid number for the annual interest rate.")
    
    duration_str = input("Enter the duration (e.g., 1 day, 3 months, 2 years): ")
    duration_days = convert_to_days(duration_str)
    
    # Loop until a valid input for monthly interest payout is provided
    while True:
        monthly_payout_str = input("Do you want monthly interest payout? (yes/no): ").lower()
        if monthly_payout_str in ["yes", "no"]:
            monthly_payout = monthly_payout_str == "yes"
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
    
    maturity_amount = calculate_fd_maturity(principal, annual_interest_rate, duration_days, monthly_payout)
    
    print("-----------------------------")
    print("Principal Amount: ₹{:.2f}".format(principal))
    print("Annual Interest Rate: {}%".format(annual_interest_rate))
    print("Duration of FD: {}".format(duration_str))
    if monthly_payout:
        print("Monthly Interest Payout: Yes")
    else:
        print("Monthly Interest Payout: No")
    print("Maturity Amount: ₹{:.2f}".format(maturity_amount))

if __name__ == "__main__":
    main()
