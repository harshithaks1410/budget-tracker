from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = 'data.json'

# Load data from JSON
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"income": [], "expense": []}
    return {"income": [], "expense": []}

# Save data to JSON
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    data = load_data()
    total_income = sum(item['amount'] for item in data['income'])
    total_expense = sum(item['amount'] for item in data['expense'])
    balance = total_income - total_expense
    return render_template("index.html", data=data, balance=balance,
                           total_income=total_income, total_expense=total_expense)

@app.route('/add_income', methods=['POST'])
def add_income():
    source = request.form['source']
    amount = float(request.form['amount'])
    data = load_data()
    data['income'].append({"source": source, "amount": amount})
    save_data(data)
    return redirect(url_for('index'))

@app.route('/add_expense', methods=['POST'])
def add_expense():
    reason = request.form['reason']
    amount = float(request.form['amount'])
    data = load_data()
    data['expense'].append({"reason": reason, "amount": amount})
    save_data(data)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
