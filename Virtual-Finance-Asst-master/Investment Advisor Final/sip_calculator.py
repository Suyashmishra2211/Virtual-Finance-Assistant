def sip_calculator(sip_amount, duration_years, rate_of_return, frequency=12):
    # Convert annual rate of return to monthly
    rate_of_return_monthly = rate_of_return / (12 * 100)

    # Calculate total number of investments
    total_investments = duration_years * frequency

    # Calculate future value of SIP investment
    future_value = sip_amount * (((1 + rate_of_return_monthly) ** total_investments - 1) / rate_of_return_monthly)

    # Calculate total invested amount
    total_invested = sip_amount * total_investments

    # Calculate returns earned
    returns_earned = future_value - total_invested

    return future_value, total_invested, returns_earned

def main():
    print("Welcome to SIP Calculator")
    print("-------------------------")

    # Get user inputs
    while True:
        try:
            sip_amount = float(input("Enter monthly SIP amount : "))
            duration_years = int(input("Enter investment duration in years : "))
            rate_of_return = float(input("Enter expected annual rate of return : "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Calculate future value, total invested amount, and returns earned
    future_value, total_invested, returns_earned = sip_calculator(sip_amount, duration_years, rate_of_return)

    # Display result
    print(f"Monthly SIP amount: ₹{sip_amount}")
    print(f"Investment duration: {duration_years} years")
    print(f"Expected annual rate of return: {rate_of_return}%")
    print(f"Future value of SIP investment: ₹{future_value:.2f}")
    print(f"Total invested amount: ₹{total_invested:.2f}")
    print(f"Returns earned: ₹{returns_earned:.2f}")

if __name__ == "__main__":
    main()
