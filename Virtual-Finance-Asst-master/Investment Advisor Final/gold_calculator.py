import requests

def get_gold_price():
    url = "https://live-metal-prices.p.rapidapi.com/v1/latest/XAU/INR"

    headers = {
        "X-RapidAPI-Key": "aaef3a7cc0mshe80ecbea96aa648p1ed56cjsnb28bb180413b",
	    "X-RapidAPI-Host": "live-metal-prices.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for errors

        gold_data = response.json()

        gold_price_inr = gold_data["rates"].get("XAU")
        if gold_price_inr is not None:
            return gold_price_inr
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching gold price: {e}")
        return None

def convert_to_days(duration, unit):
    if unit.lower() == 'day' or unit.lower() == 'days' or unit.lower() == 'da':
        return duration
    elif unit.lower() == 'month' or unit.lower() == 'months' or unit.lower() == 'mon':
        return duration * 30  # Assuming 1 month = 30 days
    elif unit.lower() == 'year' or unit.lower() == 'years' or unit.lower() == 'yea':
        return duration * 365  # Assuming 1 year = 365 days
    else:
        return 0  # Invalid unit

def parse_duration(duration_str):
    try:
        parts = duration_str.split()
        value = float(parts[0])
        unit = parts[1]
        return value, unit
    except:
        return None, None

def gold_investment(amount, days, current_gold_price):
    if current_gold_price is None:
        print("Failed to fetch current gold price. Please try again later.")
        return None, None

    # Calculate total investment amount
    total_investment_inr = amount
    
    # Calculate total gold purchased
    total_gold_purchased = total_investment_inr / current_gold_price
    
    # Fixed growth rate of 15%
    daily_growth_rate = ((1 + 0.15) ** (1/365)) - 1  # Convert annual to daily growth
    total_value_after_days_inr = total_investment_inr + (total_investment_inr * daily_growth_rate * days)
    
    # Calculate profit
    profit_inr = total_value_after_days_inr - total_investment_inr
    
    return total_value_after_days_inr, profit_inr

def main():
    while True:
        try:
            amount_inr = float(input("Enter the amount you want to invest in gold (INR): "))
            duration_str = input("Enter the duration (e.g., 1 month, 2.5 years): ")

            # Parse duration string
            duration, unit = parse_duration(duration_str)

            if duration is None or unit is None or duration <= 0:
                print("Please enter a valid duration.")
                continue

            # Convert duration to days
            days = int(convert_to_days(duration, unit))  # Convert to integer

            if amount_inr <= 0 or days <= 0:
                print("Please enter a valid amount and duration.")
                continue

            # Get current gold price in INR
            current_gold_price_inr = get_gold_price()

            # Calculate total value and profit based on the current gold price
            total_value_inr, profit_inr = gold_investment(amount_inr, days, current_gold_price_inr)

            if total_value_inr is not None and profit_inr is not None:
                print("\nInvestment Summary:")
                print("Initial Investment Amount: ₹", amount_inr)
                print("Duration: {} {}".format(duration, unit))
                print("Total Value of Gold after {} days: ₹".format(days), total_value_inr)
                print("Profit after {} days: ₹".format(days), profit_inr)
            else:
                print("Failed to calculate investment. Please try again later.")

            break  # Exit the loop if all inputs are valid

        except ValueError:
            print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()
