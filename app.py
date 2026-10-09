from flask import Flask, render_template, request, redirect
import json, os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "bank_accounts.json"

def load_accounts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_accounts(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def home():
    accounts = load_accounts()
    total = sum(a['balance'] for a in accounts.values())
    return render_template("index.html", accounts=accounts, total=total, count=len(accounts))

@app.route("/create", methods=["POST"])
def create():
    name = request.form["name"]
    pin = request.form["pin"]
    acc_type = request.form["type"]
    accounts = load_accounts()
    if name not in accounts:
        accounts[name] = {"name":name,"pin":pin,"balance":0,"loan":0,"type":acc_type,"transactions":[f"Created {datetime.now()}"]}
        save_accounts(accounts)
    return redirect("/")

@app.route("/deposit", methods=["POST"])
def deposit():
    name = request.form["name"]
    amount = int(request.form["amount"])
    accounts = load_accounts()
    if name in accounts:
        accounts[name]["balance"] += amount
        save_accounts(accounts)
    return redirect("/")

@app.route("/send", methods=["POST"])
def send():
    s = request.form["sender"]
    r = request.form["receiver"]
    a = int(request.form["amount"])
    accounts = load_accounts()
    if s in accounts and r in accounts and accounts[s]["balance"] >= a:
        accounts[s]["balance"] -= a
        accounts[r]["balance"] += a
        save_accounts(accounts)
    return redirect("/")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)