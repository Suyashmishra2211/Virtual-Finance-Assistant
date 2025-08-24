import re
import requests
import os

class GoldChatterbot:
    def __init__(self):
        # Get the directory path of the current file
        current_directory = os.path.dirname(__file__)
        # Combine the directory path with the file name
        file_path = os.path.join(current_directory, "gold.txt")
        
        # Load trigger phrases from file
        with open(file_path, "r") as file:
            self.gold_phrases = [line.strip() for line in file]
    
    def respond(self, input_text):
        if any(phrase.lower() in input_text.lower() for phrase in self.gold_phrases):
            gold_price = self.get_gold_price()
            return gold_price
        elif "exit" in input_text.lower():
            return "Goodbye!"
        else:
            return "I'm sorry, I don't understand that."

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

            gold_price_ounce = gold_data["rates"].get("XAU")
            if gold_price_ounce is not None:
                # Convert price from per ounce to per 10 grams
                gold_price_10g = gold_price_ounce / 2.65 
                return f"The current price of gold is {gold_price_10g:.2f} INR per 10 grams"
            else:
                return "Could not fetch the price for gold."

        except requests.exceptions.RequestException as e:
            print(f"Error fetching gold price: {e}")
            return "Could not fetch the price for gold."

# Example usage
if __name__ == "__main__":
    chatbot = GoldChatterbot()
    print("Welcome to the Gold Chatterbot!")
    while True:
        user_input = input("You: ")
        if "exit" in user_input.lower():
            print("Bot: Goodbye!")
            break
        response = chatbot.respond(user_input)
        print("Bot:", response)
