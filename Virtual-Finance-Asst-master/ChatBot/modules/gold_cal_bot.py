import os
import requests
import re

class GoldInvestmentBot:
    def __init__(self):
        pass
    
    def respond(self, input_text):
        file_path = os.path.join(os.path.dirname(__file__), "gold_invest.txt")
        with open(file_path, "r") as file:
            calculate_phrases = [line.strip() for line in file]
        
        if any(phrase.lower() in input_text.lower() for phrase in calculate_phrases):
            return self.calculate_gold_investment(input_text)
        elif "exit" in input_text.lower():
            return "Goodbye!"
        else:
            return "I'm sorry, I don't understand that."

    def calculate_gold_investment(self, input_text):
        amount_inr, duration_days = self.extract_investment_details(input_text)
        if amount_inr is None or duration_days is None:
            return "Please enter a valid amount and duration"
        
        if amount_inr <= 0 or duration_days <= 0:
            return "Please enter a valid amount and duration."

        current_gold_price_inr = self.get_gold_price()
        if current_gold_price_inr is None:
            return "Failed to fetch current gold price. Please try again later."

        total_value_inr, profit_inr = self.gold_investment(amount_inr, duration_days, current_gold_price_inr)
        total_value_inr = round(total_value_inr, 2)
        profit_inr = round(profit_inr, 2)
        if total_value_inr is not None and profit_inr is not None:
            return f"\nFor an investment amount of ₹{amount_inr} and duration of {duration_days} days, the total value of gold is ₹{total_value_inr} and the profit after {duration_days} days is ₹{profit_inr}"
        else:
            return "Failed to calculate investment. Please try again later."

    def get_gold_price(self):
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
            return gold_price_inr if gold_price_inr is not None else None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching gold price: {e}")
            return None

    def convert_to_days(self, duration_str):
        try:
            duration, unit = duration_str.split()
            duration = float(duration)
            if unit.lower() in ['day', 'days', 'da']:
                return duration
            elif unit.lower() in ['month', 'months', 'mon']:
                return duration * 30
            elif unit.lower() in ['year', 'years', 'yea']:
                return duration * 365
            else:
                raise ValueError("Invalid unit.")
        except ValueError as e:
            raise ValueError("Invalid format. Please use the correct unit for duration.") from e

    def parse_duration(self, duration_str):
        try:
            parts = duration_str.split()
            value = float(parts[0])
            unit = parts[1]
            return value, unit
        except:
            return None, None

    def gold_investment(self, amount, days, current_gold_price):
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

    def extract_investment_details(self, input_text):
        amount_inr = None
        duration_days = None

        # First regex to check for ₹ symbol before the amount
        amount_match_1 = re.search(r"(?:₹\s*)(\d+(?:,\d{3})*(?:\.\d+)?)\b", input_text, re.IGNORECASE)
        if amount_match_1:
            amount_inr = float(amount_match_1.group(1).replace(",", ""))
        else:
            # Second regex to check for terms like "rs", "rupee", "rupees", "INR" after any value
            amount_match_2 = re.search(r"(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:rs|rupee|rupees|INR)\b", input_text, re.IGNORECASE)
            if amount_match_2:
                amount_inr = float(amount_match_2.group(1).replace(",", ""))

        duration_match = re.search(r"(\d+(?:\.\d+)?)\s*(year[s]?|month[s]?|day[s]?|yr[s]?|mon|da)", input_text, re.IGNORECASE)
        if duration_match:
            duration = float(duration_match.group(1))
            unit = duration_match.group(2).lower()
            duration_days = self.convert_to_days(f"{duration} {unit}")
        
        if not duration_days:
            # Check for terms spelled out in alphabetical form up to twenty
            term_alphabetical_match = re.search(r"(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)\s*(year[s]?|month[s]?|day[s]?|yr[s]?|mon|da)", input_text, re.IGNORECASE)
            if term_alphabetical_match:
                term_word = term_alphabetical_match.group(1).lower()
                term_dict = {
                    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
                    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
                    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20
                }
                duration_days = self.convert_to_days(f"{term_dict.get(term_word)} {term_alphabetical_match.group(2).lower()}")

        return amount_inr, duration_days
