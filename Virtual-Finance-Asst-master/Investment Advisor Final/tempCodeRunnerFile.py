from flask import Flask, render_template, request
import FD_calculator as fd
import gold_calculator as gold
import TD as td
import RD as rd
import sip_calculator as sip
import stock_investment_calculator as stock

app = Flask(__name__)

def compare_investments(principal_fd, rate_fd, duration_fd, monthly_payout_fd,
                        amount_inr_gold, duration_gold,
                        investment_amount_td, duration_years_td,
                        monthly_investment_rd, duration_rd,
                        sip_amount, sip_duration, sip_rate,
                        initial_investment_stock, duration_stock):
    # Calculate returns for each investment type
    fd_return = calculate_fd_return(principal_fd, rate_fd, duration_fd, monthly_payout_fd)
    gold_return = calculate_gold_return(amount_inr_gold, duration_gold)
    td_return = calculate_td_return(investment_amount_td, duration_years_td)
    rd_return = calculate_rd_return(monthly_investment_rd, duration_rd)
    sip_return = calculate_sip_return(sip_amount, sip_duration, sip_rate)
    stock_return = calculate_stock_return(initial_investment_stock, duration_stock)

    print("FD Return:", fd_return)
    print("Gold Return:", gold_return)
    print("TD Return:", td_return)
    print("RD Return:", rd_return)
    print("SIP Return:", sip_return)
    print("Stock Return:", stock_return)

    # Determining the most profitable option
    max_return = max(fd_return, gold_return, td_return, sip_return, stock_return)
    options = {
        fd_return: "Fixed Deposit",
        gold_return: "Gold Investment",
        td_return: "Time Deposit",
        sip_return: "SIP",
        stock_return: "Stock Investment",
        rd_return: "Recurring Deposit"
    }
    most_profitable_investment = options[max_return]
    return f"The most profitable investment type is: {most_profitable_investment} with a return value of ₹{max_return}"

def calculate_fd_return(principal_fd, rate_fd, duration_fd, monthly_payout_fd):
    # Convert duration to days
    duration_days = fd.convert_to_days(duration_fd)
    
    fd_return = fd.calculate_fd_maturity(principal_fd, rate_fd, duration_days, monthly_payout_fd)
    return fd_return

def calculate_gold_return(amount_inr, duration_str):
    # Parse duration string
    duration, unit = gold.parse_duration(duration_str)

    if duration is None or unit is None or duration <= 0:
        return None, "Please enter a valid duration."

    # Convert duration to days
    days = int(gold.convert_to_days(duration, unit))  # Convert to integer

    if amount_inr <= 0 or days <= 0:
        return None, "Please enter a valid amount and duration."

    # Get current gold price in INR
    current_gold_price_inr = gold.get_gold_price()

    # Calculate total value and profit based on the current gold price
    total_value_inr, profit_inr = gold.gold_investment(amount_inr, days, current_gold_price_inr)

    if total_value_inr is not None and profit_inr is not None:
        return total_value_inr  # Return calculated value and no error message
    else:
        return None, "Failed to calculate investment. Please try again later."

def calculate_td_return(investment_amount_td, duration_years_td):
    duration_months = 0  # Assuming no months input for simplicity

    # Calculate the TD type using duration
    td_type = str(duration_years_td)

    td_account, td_return = td.calculate_TD_return(investment_amount_td, duration_years_td, duration_months, td_type)
    
    return td_return

def calculate_rd_return(monthly_investment_rd, duration_rd):
    duration_years, duration_months = rd.convert_to_years_months(duration_rd)
    a,rd_return,x,y,z = rd.calculate_RD_return(monthly_investment_rd, duration_years,duration_months)
    return rd_return

def calculate_sip_return(sip_amount, sip_duration, sip_rate):
    future_value,total_value,sip_return = sip.sip_calculator(sip_amount, sip_duration, sip_rate)
    return sip_return

def calculate_stock_return(initial_investment_stock, duration_stock):
    best_company, max_return = stock.find_best_company(initial_investment_stock, duration_stock)

    if best_company is not None:
        return max_return
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():

    print("Received form data.")

    principal_fd = float(request.form['principal_fd'])
    rate_fd = float(request.form['rate_fd'])
    duration_fd = request.form['duration_fd']
    monthly_payout_fd = request.form['monthly_payout_fd'].lower() == "yes"
    amount_inr_gold = float(request.form['amount_inr_gold'])
    duration_gold = request.form['duration_gold']
    investment_amount_td = float(request.form['investment_amount_td'])
    duration_years_td = float(request.form['duration_years_td'])
    monthly_investment_rd = float(request.form['monthly_investment_rd'])
    duration_rd = float(request.form['duration_rd'])
    sip_amount = float(request.form['sip_amount'])
    sip_duration = int(request.form['sip_duration'])
    sip_rate = float(request.form['sip_rate'])
    initial_investment_stock = float(request.form['initial_investment_stock'])
    duration_stock = request.form['duration_stock']

    print("Form data received and processed successfully.")

    response = compare_investments(principal_fd, rate_fd, duration_fd, monthly_payout_fd,
                                   amount_inr_gold, duration_gold,
                                   investment_amount_td, duration_years_td,
                                   monthly_investment_rd, duration_rd,
                                   sip_amount, sip_duration, sip_rate,
                                   initial_investment_stock, duration_stock)
    
    print("Sending response:", response)

    return response

if __name__ == "__main__":
    app.run(debug=True)
