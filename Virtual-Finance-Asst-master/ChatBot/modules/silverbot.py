import os
import requests

class SilverChatterbot:
    def __init__(self):
        # Get the path of silver.txt dynamically
        current_dir = os.path.dirname(os.path.abspath(__file__))
        silver_file_path = os.path.join(current_dir, "silver.txt")

        # Load trigger phrases from file
        with open(silver_file_path, "r") as file:
            self.silver_phrases = [line.strip() for line in file]
    
    def respond(self, input_text):
        if any(phrase.lower() in input_text.lower() for phrase in self.silver_phrases):
            silver_price = self.get_silver_price()
            return silver_price
        elif "exit" in input_text.lower():
            return "Goodbye!"
        else:
            return "I'm sorry, I don't understand that."

    def get_silver_price(self):
        metal = "XAG"  # XAG is the code for silver
        url = f"https://live-metal-prices.p.rapidapi.com/v1/latest/{metal}/INR"

        headers = {
            "X-RapidAPI-Key": "aaef3a7cc0mshe80ecbea96aa648p1ed56cjsnb28bb180413b",
	        "X-RapidAPI-Host": "live-metal-prices.p.rapidapi.com"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Check for errors

            metal_data = response.json()

            metal_price_ounce = metal_data["rates"].get(metal)
            if metal_price_ounce is not None:
                # Convert price from per ounce to per 10 grams
                metal_price_10g = metal_price_ounce / 2.8  # 1 ounce = 2.8 grams
                return f"The current price of silver is {metal_price_10g:.2f} INR per 10 grams"
            else:
                return "Could not fetch the price for silver."

        except requests.exceptions.RequestException as e:
            print(f"Error fetching silver price: {e}")
            return "Could not fetch the price for silver."

# Example usage
if __name__ == "__main__":
    chatbot = SilverChatterbot()
    print("Welcome to the Silver Chatterbot!")
    while True:
        user_input = input("You: ")
        if "exit" in user_input.lower():
            print("Bot: Goodbye!")
            break
        response = chatbot.respond(user_input)
        print("Bot:", response)
