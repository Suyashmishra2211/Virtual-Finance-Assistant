import os
import re

class RDChatterbot:
    def __init__(self):
        pass
    
    def respond(self, input_text):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        rd_phrase_file_path = os.path.join(current_dir, "rd_phrase.txt")
        
        with open(rd_phrase_file_path, "r") as file:
            calculate_phrases = [line.strip() for line in file]
        
        if any(phrase.lower() in input_text.lower() for phrase in calculate_phrases):
            monthly_investment, duration, duration_unit = self.extract_RD_details(input_text)
            if duration_unit and duration_unit not in ['year', 'years']:
                return "Please provide the investment duration in years."
            if duration is not None:
                if 1 <= duration <= 5:
                    return self.calculate_RD_return_text(monthly_investment, duration)
                else:
                    return "The duration can be between 1-5 years."
            else:
                return "Please provide both the monthly investment amount and the investment duration in years."
        elif "exit" in input_text.lower():
            return "Goodbye!"
        else:
            return "I'm sorry, I don't understand that."

    def convert_to_years_months(self, duration):
        years = int(duration)
        months = int((duration - years) * 12)
        return years, months

    def calculate_RD_return(self, monthly_investment, duration_years, duration_months):
        quarterly_interest_rate_RD = 0.067 / 4
        total_months = duration_years * 12 + duration_months
        
        total_investment_RD = monthly_investment * total_months
        
        quarters = total_months // 3
        expected_return_RD = total_investment_RD * ((1 + quarterly_interest_rate_RD) ** quarters)
        return expected_return_RD

    def calculate_RD_return_text(self, monthly_investment, duration):
        duration_years, duration_months = self.convert_to_years_months(duration)
        total_months = duration_years * 12 + duration_months
        expected_return_RD = self.calculate_RD_return(monthly_investment, duration_years, duration_months)
        return f"The expected return for a {duration_years}-year Recurring Deposit Account with a monthly investment of ₹{monthly_investment:.2f} over {duration} years is ₹{expected_return_RD:.2f}."

    def extract_RD_details(self, input_text):
        monthly_investment = None
        duration = None
        duration_unit = None

        # First regex to check for ₹ symbol before the amount
        amount_match_1 = re.search(r"(?:₹\s*)(\d+(?:,\d{3})*(?:\.\d+)?)\b", input_text, re.IGNORECASE)
        if amount_match_1:
            monthly_investment = float(amount_match_1.group(1).replace(",", ""))
        else:
            # Second regex to check for terms like "rs", "rupee", "rupees", "INR" after any value
            amount_match_2 = re.search(r"(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:rs|rupee|rupees|INR)\b", input_text, re.IGNORECASE)
            if amount_match_2:
                monthly_investment = float(amount_match_2.group(1).replace(",", ""))

        duration_match = re.search(r"(\d+(?:\.\d+)?)\s*(years?|yrs?|months?|mon|days?|da)", input_text, re.IGNORECASE)
        if duration_match:
            duration = float(duration_match.group(1))
            duration_unit = duration_match.group(2).lower()
            if duration_unit in ['year', 'years', 'yr', 'yrs']:
                duration_unit = 'year'
            elif duration_unit in ['month', 'months', 'mon', 'day', 'days', 'da']:
                return monthly_investment, None, duration_unit
        
        if not duration:
            # Check for terms spelled out in alphabetical form up to twenty
            term_alphabetical_match = re.search(r"(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)\s*(years?|yrs?|months?|mon|days?|da)", input_text, re.IGNORECASE)
            if term_alphabetical_match:
                term_word = term_alphabetical_match.group(1).lower()
                term_dict = {
                    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
                    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
                    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20
                }
                duration = term_dict.get(term_word)
                duration_unit = term_alphabetical_match.group(2).lower()
                if duration_unit in ['year', 'years', 'yr', 'yrs']:
                    duration_unit = 'year'
                elif duration_unit in ['month', 'months', 'mon', 'day', 'days', 'da']:
                    return monthly_investment, None, duration_unit

        return monthly_investment, duration, duration_unit
