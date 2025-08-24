import os
import re

class Chatterbot:
    def __init__(self):
        # Get the directory path of the current file
        current_directory = os.path.dirname(__file__)
        # Combine the directory path with the file name
        self.file_path = os.path.join(current_directory, "calculate_phrases.txt")
    
    def respond(self, input_text):
        # Read calculate_phrases.txt from the file_path
        with open(self.file_path, "r") as file:
            calculate_phrases = [line.strip() for line in file]
        
        if any(phrase.lower() in input_text.lower() for phrase in calculate_phrases):
            principal, annual_interest_rate, loan_term_years = self.extract_loan_details(input_text)
            if principal is not None and annual_interest_rate is not None and loan_term_years is not None:
                monthly_payment, total_payment, total_interest = self.calculate_loan_payment(principal, annual_interest_rate, loan_term_years)
                return f"Your monthly EMI will be ₹{monthly_payment:.2f}. Total Payment: ₹{total_payment:.2f}, Total Interest: ₹{total_interest:.2f}"
            else:
                return "Please give the amount in rupees along with interest percent and duration"
        elif "exit" in input_text.lower():
            return "Goodbye!"
        else:
            return "I'm sorry, I don't understand that."

    def calculate_loan_payment(self, principal, annual_interest_rate, loan_term_years):
        # Convert annual interest rate to monthly rate
        monthly_interest_rate = annual_interest_rate / 12 / 100
        # Convert loan term from years to months
        loan_term_months = loan_term_years * 12
        
        # Calculate monthly payment using the formula
        monthly_payment = (principal * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -loan_term_months)
        
        # Calculate total payment and total interest
        total_payment = monthly_payment * loan_term_years * 12
        total_interest = total_payment - principal
        
        return monthly_payment, total_payment, total_interest

    def extract_loan_details(self, input_text):
        principal = None
        annual_interest_rate = None
        loan_term_years = None
        
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
        
        term_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)", input_text, re.IGNORECASE)
        if term_match:
            loan_term_years = float(term_match.group(1))
        
        if not loan_term_years:
            # Check for terms spelled out in alphabetical form up to twenty
            term_alphabetical_match = re.search(r"(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)\s*(?:years?|yrs?)", input_text, re.IGNORECASE)
            if term_alphabetical_match:
                term_word = term_alphabetical_match.group(1)
                term_dict = {
                    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
                    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
                    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20
                }
                loan_term_years = term_dict.get(term_word.lower())

        return principal, annual_interest_rate, loan_term_years
