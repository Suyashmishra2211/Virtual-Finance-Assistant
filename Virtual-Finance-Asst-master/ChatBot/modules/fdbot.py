import os
import re

class FDCalculatorBot:
    def __init__(self):
        # Get the directory path of the current file
        current_directory = os.path.dirname(__file__)
        # Combine the directory path with the file name
        self.file_path = os.path.join(current_directory, "FD_phrases.txt")
    
    def respond(self, input_text):
        try:
            # Read FD_phrases.txt from the file_path
            with open(self.file_path, "r") as file:
                calculate_phrases = [line.strip() for line in file]
        except FileNotFoundError:
            return "I'm sorry, the necessary file is missing."

        if any(phrase.lower() in input_text.lower() for phrase in calculate_phrases):
            principal, annual_interest_rate, duration_days, monthly_payout = self.extract_fd_details(input_text)
            if principal is not None and annual_interest_rate is not None and duration_days is not None:
                maturity_amount = self.calculate_fd_maturity(principal, annual_interest_rate, duration_days, monthly_payout)
                return f"The maturity amount for the Fixed Deposit is ₹{maturity_amount:.2f}"
            else:
                return "Please give all the required values with proper units"
        elif "exit" in input_text.lower():
            return "Goodbye!"
        else:
            return "I'm sorry, I don't understand that."

    def calculate_fd_maturity(self, principal, annual_interest_rate, duration_days, monthly_payout=False):
        interest_rate_decimal = annual_interest_rate / 100
        duration_years = duration_days / 365
        
        if duration_years <= 0.5:
            maturity_amount = principal * (1 + interest_rate_decimal * duration_years)
        else:
            if monthly_payout:
                total_interest = principal * interest_rate_decimal * duration_years
                monthly_interest = total_interest / 12
                maturity_amount = principal + total_interest
            else:
                maturity_amount = principal * (1 + interest_rate_decimal) ** duration_years
        
        return round(maturity_amount, 2)

    def extract_fd_details(self, input_text):
        principal = None
        annual_interest_rate = None
        duration_days = None
        monthly_payout = False
        
        # First regex to check for ₹ symbol before the amount
        principal_match_1 = re.search(r"(?:₹\s*)(\d+(?:,\d{3})*(?:\.\d+)?)\b", input_text, re.IGNORECASE)
        if principal_match_1:
            principal = float(principal_match_1.group(1).replace(",", ""))
        else:
            # Second regex to check for terms like "rs", "rupee", "rupees", "INR" after any value
            principal_match_2 = re.search(r"(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:rs|rupee|rupees|INR)\b", input_text, re.IGNORECASE)
            if principal_match_2:
                principal = float(principal_match_2.group(1).replace(",", ""))
        
        interest_rate_match = re.search(r"(\d+(?:\.\d+)?)(?:%|\s*%|\s*percent)", input_text, re.IGNORECASE)
        if interest_rate_match:
            annual_interest_rate = float(interest_rate_match.group(1))
        
        duration_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:day|days|da|month|months|mon|year|years|yea)", input_text, re.IGNORECASE)
        if duration_match:
            duration_str = duration_match.group(0)
            duration_days = self.convert_to_days(duration_str)
        
        if not duration_days:
            # Check for terms spelled out in alphabetical form up to twenty
            term_alphabetical_match = re.search(r"(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)\s*(?:day|days|da|month|months|mon|year|years|yea)", input_text, re.IGNORECASE)
            if term_alphabetical_match:
                term_word = term_alphabetical_match.group(1).lower()
                term_dict = {
                    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
                    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
                    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20
                }
                duration_days = self.convert_to_days(f"{term_dict.get(term_word)} years")

        if re.search(r"monthly interest payout", input_text, re.IGNORECASE):
            monthly_payout = True
        
        return principal, annual_interest_rate, duration_days, monthly_payout

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
