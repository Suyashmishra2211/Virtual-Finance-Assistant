from flask import Flask, render_template, request, redirect
import budget as bd

app = Flask(__name__)

file_name = "transactions.xlsx"

# Route for rendering the index page
@app.route("/")
def index():
    transactions = bd.load_transactions(file_name)
    indexed_transactions = preprocess_transactions(transactions)
    return render_template("index.html", transactions=indexed_transactions)

# Route for adding an expense
@app.route("/add_expense", methods=["POST"])
def add_expense():
    name = request.form["name"]
    amount = float(request.form["amount"])
    bd.add_transaction(file_name, "Expense", amount, name)
    return redirect("/")

# Route for adding an income
@app.route("/add_income", methods=["POST"])
def add_income():
    name = request.form["name"]
    amount = float(request.form["amount"])
    bd.add_transaction(file_name, "Income", amount, name)
    return redirect("/")

# Route for deleting a transaction
@app.route("/delete_transaction", methods=["POST"])
def delete_transaction():
    idx = int(request.form["index"])
    bd.delete_transaction(file_name, idx)
    return redirect("/")

# Preprocess transactions to add index
def preprocess_transactions(transactions):
    indexed_transactions = [(idx + 1, transaction) for idx, transaction in enumerate(transactions)]
    return indexed_transactions

if __name__ == "__main__":
    app.run(debug=True)
