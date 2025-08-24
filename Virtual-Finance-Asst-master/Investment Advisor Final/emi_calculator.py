def calculate_loan_payment(principal, annual_interest_rate, loan_term_years):
    # Convert annual interest rate to monthly rate
    monthly_interest_rate = annual_interest_rate / 12 / 100
    # Convert loan term from years to months
    loan_term_months = loan_term_years * 12
    
    # Calculate monthly payment using the formula
    monthly_payment = (principal * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -loan_term_months)
    
    return monthly_payment

def main():
    print("Loan EMI Calculator")
    print("-----------------------------")
    
    # Input validation loop
    while True:
        try:
            principal = float(input("Enter the loan amount: ₹"))
            annual_interest_rate = float(input("Enter the annual interest rate (%): "))
            loan_term_years = int(input("Enter the loan term (in years): "))
            break  # Exit the loop if all inputs are valid
        except ValueError:
            print("Please enter valid numerical values.")
    
    monthly_payment = calculate_loan_payment(principal, annual_interest_rate, loan_term_years)
    
    print("-----------------------------")
    print("Monthly Payment: ₹{:.2f}".format(round(monthly_payment, 2)))
    total_payment = monthly_payment * loan_term_years * 12
    print("Total Payment: ₹{:.2f}".format(round(total_payment, 2)))
    total_interest = total_payment - principal
    print("Total Interest: ₹{:.2f}".format(round(total_interest, 2)))

if __name__ == "__main__":
    main()