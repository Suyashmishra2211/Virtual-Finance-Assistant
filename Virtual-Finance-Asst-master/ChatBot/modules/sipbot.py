import os
import re

class SipChatterbot:
    def __init__(self):
        pass
    
    def respond(self, input_text):
        trigger_file_path = os.path.join(os.path.dirname(__file__), "sip.txt")
        with open(trigger_file_path, "r") as file:
            calculate_phrases = [line.strip() for line in file]
        
        if any(phrase.lower() in input_text.lower() for phrase in calculate_phrases):
            return self.extract_sip_details(input_text)  # Return SIP details directly
        elif "exit" in input_text.lower():
            return "Goodbye!"
        else:
            return "I'm sorry, I don't understand that."

    def sip_calculator(self, sip_amount, duration_years, rate_of_return, frequency=12):
        # Calculate monthly investment amount
        monthly_investment = sip_amount / (duration_years * frequency)

        # Convert annual rate of return to monthly
        rate_of_return_monthly = rate_of_return / (12 * 100)

        # Calculate total number of investments
        total_investments = int(duration_years * frequency)  # Ensure total_investments is an integer

        # Calculate future value of SIP investment
        future_value = 0
        for month in range(1, total_investments + 1):
            future_value += monthly_investment * ((1 + rate_of_return_monthly) ** (total_investments - month))

        # Calculate total invested amount
        total_invested = sip_amount

        # Calculate returns earned
        returns_earned = future_value - total_invested

        return future_value, total_invested, returns_earned

    def extract_sip_details(self, input_text):
        sip_amount = None
        duration_years = None
        rate_of_return = None
        
        # First regex to check for ₹ symbol before the amount
        sip_amount_match_1 = re.search(r"(?:₹\s*)(\d+(?:,\d{3})*(?:\.\d+)?)\b", input_text, re.IGNORECASE)
        if sip_amount_match_1:
            sip_amount = float(sip_amount_match_1.group(1).replace(",", ""))
        else:
            # Second regex to check for terms like "rs", "rupee", "rupees", "INR" after any value
            sip_amount_match_2 = re.search(r"(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:rs|rupee|rupees|INR)\b", input_text, re.IGNORECASE)
            if sip_amount_match_2:
                sip_amount = float(sip_amount_match_2.group(1).replace(",", ""))

        duration_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:year[s]?|yrs?|month[s]?|mon|day[s]?|da)", input_text, re.IGNORECASE)
        if duration_match:
            duration_str = duration_match.group(0)
            duration_years = self.convert_to_years(duration_str)

        if not duration_years:
            # Check for terms spelled out in alphabetical form up to twenty
            term_alphabetical_match = re.search(r"(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)\s*(year[s]?|yrs?|month[s]?|mon|day[s]?|da)", input_text, re.IGNORECASE)
            if term_alphabetical_match:
                term_word = term_alphabetical_match.group(1).lower()
                term_dict = {
                    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
                    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
                    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20
                }
                duration_years = self.convert_to_years(f"{term_dict.get(term_word)} {term_alphabetical_match.group(2).lower()}")

        rate_of_return_match = re.search(r"(\d+(?:\.\d+)?)(?:%|\s*%|\s*percent)", input_text, re.IGNORECASE)
        if rate_of_return_match:
            rate_of_return = float(rate_of_return_match.group(1))
        
        if sip_amount is not None and duration_years is not None and rate_of_return is not None:
            future_value, total_invested, returns_earned = self.sip_calculator(sip_amount, duration_years, rate_of_return)
            return f"Monthly investment amount: ₹{sip_amount / (duration_years * 12):.2f}<br>The future value of SIP investment: ₹{future_value:.2f}<br>Total invested amount: ₹{total_invested:.2f}<br>Returns earned: ₹{returns_earned:.2f}"
        else:
            return "Please provide SIP amount, duration, and rate of return to calculate SIP details."

    def convert_to_years(self, duration_str):
        try:
            duration, unit = duration_str.split()
            duration = float(duration)
            if unit.lower() in ['day', 'days', 'da']:
                return duration / 365
            elif unit.lower() in ['month', 'months', 'mon']:
                return duration / 12
            elif unit.lower() in ['year', 'years', 'yrs']:
                return duration
            else:
                raise ValueError("Invalid unit.")
        except ValueError as e:
            raise ValueError("Invalid format. Please use the correct unit for duration.") from e

# Example usage
if __name__ == "__main__":
    chatbot = SipChatterbot()
    print("Welcome to the SIP Chatterbot!")
    while True:
        user_input = input("You: ")
        if "exit" in user_input.lower():
            print("Bot: Goodbye!")
            break
        response = chatbot.respond(user_input)
        print("Bot:", response)
