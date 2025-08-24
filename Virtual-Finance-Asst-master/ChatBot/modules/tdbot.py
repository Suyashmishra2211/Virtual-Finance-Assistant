import os
import re

class TDChatterbot:
    def __init__(self):
        pass
    
    def respond(self, input_text):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        td_phrase_file_path = os.path.join(current_dir, "td_phrase.txt")
        
        with open(td_phrase_file_path, "r") as file:
            calculate_phrases = [line.strip() for line in file]
        
        if any(phrase.lower() in input_text.lower() for phrase in calculate_phrases):
            investment_amount, duration_years, duration_unit = self.extract_TD_details(input_text)
            if duration_unit == "Invalid":
                return "The duration must be between 1-5 years."
            if duration_unit and duration_unit not in ['year', 'years']:
                return "Please provide the investment duration in years."
            if duration_years is not None and investment_amount is not None:
                if 1 <= duration_years <= 5:
                    duration_months = 0  # Assuming no months input for simplicity
                    td_type = str(duration_years)
                    return self.calculate_TD_return(investment_amount, duration_years, duration_months, td_type)
                else:
                    return "The duration must be between 1-5 years."
            else:
                return "Please provide both the investment amount and the investment duration in years."
        elif "exit" in input_text.lower():
            return "Goodbye!"
        else:
            return "I'm sorry, I don't understand that."

    def calculate_TD_return(self, investment_amount, duration_years, duration_months, td_type):
        interest_rates_TD = {
            "1": 0.069,  # 6.9% for 1 year TD
            "2": 0.07,   # 7.0% for 2 year TD
            "3": 0.071,  # 7.1% for 3 year TD
            "4": 0.071,  # 7.1% for 4 year TD (considered the same as 3 year TD)
            "5": 0.075   # 7.5% for 5 year TD
        }
        
        if td_type not in interest_rates_TD:
            return "Invalid TD type", None
        
        total_months = duration_years * 12 + duration_months
        rate = interest_rates_TD[td_type]
        quarterly_rate = rate / 4
        quarters = total_months // 3
        expected_return_TD = investment_amount * ((1 + quarterly_rate) ** quarters)
        expected_return_TD = round(expected_return_TD, 2)
        if investment_amount is not None and expected_return_TD is not None:
            return f"\nFor an investment amount of ₹ {investment_amount} and duration of {total_months} months the total return is: ₹ {expected_return_TD}"
        else:
            return "Failed to calculate investment. Please try again later."

    def extract_TD_details(self, input_text):
        investment_amount = None
        duration_years = None
        duration_unit = None
        
        # First regex to check for ₹ symbol before the amount
        amount_match_1 = re.search(r"(?:₹\s*)(\d+(?:,\d{3})*(?:\.\d+)?)\b", input_text, re.IGNORECASE)
        if amount_match_1:
            investment_amount = float(amount_match_1.group(1).replace(",", ""))
        else:
            # Second regex to check for terms like "rs", "rupee", "rupees", "INR" after any value
            amount_match_2 = re.search(r"(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:rs|rupee|rupees|INR)\b", input_text, re.IGNORECASE)
            if amount_match_2:
                investment_amount = float(amount_match_2.group(1).replace(",", ""))

        duration_match = re.search(r"(\d+(?:\.\d+)?)\s*(years?|yrs?)", input_text, re.IGNORECASE)
        if duration_match:
            duration_years = round(float(duration_match.group(1)))
            if not 1 <= duration_years <= 5:
                return investment_amount, duration_years, "Invalid"
            duration_unit = 'year'

        if not duration_years:
            # Check for terms spelled out in alphabetical form up to twenty
            term_alphabetical_match = re.search(r"(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)\s*(years?|yrs?)", input_text, re.IGNORECASE)
            if term_alphabetical_match:
                term_word = term_alphabetical_match.group(1).lower()
                term_dict = {
                    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
                    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
                    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20
                }
                duration_years = term_dict.get(term_word)
                duration_unit = 'year'
                if not 1 <= duration_years <= 5:
                    return investment_amount, duration_years, "Invalid"

        return investment_amount, duration_years, duration_unit

# Example usage
if __name__ == "__main__":
    chatbot = TDChatterbot()
    print("Welcome to the TD Chatterbot!")
    while True:
        user_input = input("You: ")
        if "exit" in user_input.lower():
            print("Bot: Goodbye!")
            break
        response = chatbot.respond(user_input)
        print("Bot:", response)
