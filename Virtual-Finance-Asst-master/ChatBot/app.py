from modules.emibot import Chatterbot  # Import the EMIBot class
from modules.fdbot import FDCalculatorBot
from modules.goldbot import GoldChatterbot
from modules.silverbot import SilverChatterbot
from modules.rdbot import RDChatterbot
from modules.tdbot import TDChatterbot
from modules.sipbot import SipChatterbot
from modules.stockweekbot import stockbot
from modules.gold_cal_bot import GoldInvestmentBot
from modules.stocktodaybot import StockBot
from modules.stockinvestcalcbot import StockInvestmentChatterbot  # Import the StockInvestmentChatterbot class
from modules.stockpricebot import stock_price
from flask import Flask, render_template, request
import speech_recognition as sr
import pyttsx3
import re
import requests
import yfinance as yf
import pandas as pd
import os

# Initialize Flask app
app = Flask(__name__)

# Create instances of bots
chatbot = Chatterbot()
fd_calculator = FDCalculatorBot()
goldbot = GoldChatterbot()
silverbot = SilverChatterbot()
rd_bot = RDChatterbot()
td_bot = TDChatterbot()
sip_bot = SipChatterbot()
gold_investment_bot = GoldInvestmentBot()
stock_bot = stockbot()
stock_today = StockBot()
emi_bot = Chatterbot()
stock_price_bot = stock_price()
stock_investment_bot = StockInvestmentChatterbot()  # Create an instance of StockInvestmentChatterbot

# Define route to handle index page
@app.route("/")
def index():
    return render_template('chat.html')

# Define route to handle user messages
@app.route("/get", methods=["POST"])
def get_response():
    user_input = request.form["msg"]
    return process_user_input(user_input)

# Process user input
def process_user_input(user_input):
    print("User Input:", user_input)
    if user_input.startswith("voice:"):
        voice_input = user_input.replace("voice:", "")
        bot_response = process_voice_input(voice_input)
    else:
        bot_response = None
        # Check for stock-related keywords
        stock_keywords = ["week"]
        if any(keyword in user_input.lower() for keyword in stock_keywords):
            bot_response = stock_bot.respond(user_input)  # Pass user_input to respond method
        else:
            # Check for gold investment keywords
            gold_investment_keywords = ["investing","gold investment", "gold price prediction", "gold returns", "gold analysis","gold return"]
            if any(keyword in user_input.lower() for keyword in gold_investment_keywords):
                print("Detected gold investment keyword.")
                try:
                    bot_response = gold_investment_bot.respond(user_input)
                except Exception as e:
                    bot_response = f"Error: {str(e)}"
            else:
                fd_keywords = ["calculate fd", "fd", "fixed deposit"]
                for keyword in fd_keywords:
                    if keyword in user_input.lower():
                        bot_response = fd_calculator.respond(user_input)
                        break

                if not bot_response:
                    # Check for EMI-related keywords
                    emi_keywords = ["emi", "loan"]
                    if any(keyword in user_input.lower() for keyword in emi_keywords):
                        bot_response = emi_bot.respond(user_input)
                    else:
                        # Check for general gold-related keywords
                        gold_keywords = ["gold", "gold price"]
                        if any(keyword in user_input.lower() for keyword in gold_keywords):
                            print("Detected gold keyword.")
                            bot_response = goldbot.respond(user_input)
                        else:
                            # Check for silver keywords
                            silver_keywords = ["silver", "silver price"]
                            if any(keyword in user_input.lower() for keyword in silver_keywords):
                                bot_response = silverbot.respond(user_input)
                            else:
                                # Check for RD keywords
                                rd_keywords = ["rd", "recurring deposit"]
                                if any(keyword in user_input.lower() for keyword in rd_keywords):
                                    try:
                                        bot_response = rd_bot.respond(user_input)
                                    except ValueError as ve:
                                        bot_response = str(ve)
                                else:
                                    # Check for TD keywords
                                    td_keywords = ["td", "time deposit"]
                                    if any(keyword in user_input.lower() for keyword in td_keywords):
                                        try:
                                            bot_response = td_bot.respond(user_input)
                                        except ValueError as ve:
                                            bot_response = str(ve)
                                    else:
                                        # Check for SIP keywords
                                        sip_keywords = ["sip", "systematic investment plan","systematic"]
                                        if any(keyword in user_input.lower() for keyword in sip_keywords):
                                            try:
                                                bot_response = sip_bot.respond(user_input)
                                            except ValueError as ve:
                                                bot_response = str(ve)
                                        else:
                                            # Check for stock price-related keywords before invoking stock_bot
                                            stock_price_keywords = ["price", "price of", "rate"]
                                            if any(keyword in user_input.lower() for keyword in stock_price_keywords):
                                                bot_response = stock_price_bot.respond_to_user(user_input)
                                            else:
                                                # Use StockBot for general stock-related queries
                                                bot_response = stock_today.bot_response(user_input)
            
                                                # Check for stock investment keywords
                                                stock_investment_keywords = ["stock","stocks","invest","stock investment", "stock invest", "investment advice"]
                                                if any(keyword in user_input.lower() for keyword in stock_investment_keywords):
                                                    try:
                                                        bot_response = stock_investment_bot.respond(user_input)
                                                    except Exception as e:
                                                        bot_response = f"Error: {str(e)}"

    print("Bot Response:", bot_response)
    return bot_response

def process_voice_input(voice_input):
    recognizer = sr.Recognizer()

    with sr.AudioFile(voice_input) as source:
        audio_data = recognizer.record(source)

    try:
        user_message = recognizer.recognize_google(audio_data)
        print("User said:", user_message)
        bot_response = chatbot.respond(user_message)

        engine = pyttsx3.init()
        engine.say(bot_response)
        engine.runAndWait()

        return bot_response

    except sr.UnknownValueError:
        return "Sorry, I could not understand what you said."

if __name__ == '__main__':
    app.run(port=7070,debug=True)
