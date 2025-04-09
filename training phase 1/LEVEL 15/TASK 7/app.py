from flask import Flask, render_template
import pandas as pd
import sqlite3
import os

app = Flask(__name__)

# Step 1: Load CSV and save to SQLite DB
def load_data_to_db():
    df = pd.read_csv("customer_shopping_data.csv")
    conn = sqlite3.connect("shopping.db")
    df.to_sql("customer_data", conn, if_exists="replace", index=False)
    conn.close()

# Step 2: Get data from SQLite DB
def fetch_data_from_db():
    conn = sqlite3.connect("shopping.db")
    df = pd.read_sql_query("SELECT * FROM customer_data", conn)
    conn.close()
    return df

@app.route("/")
def home():
    return "<h2>Welcome! Visit <a href='/report'>Report</a> to view the data.</h2>"

@app.route("/report")
def report():
    # Load and fetch the data
    if not os.path.exists("shopping.db"):
        load_data_to_db()
    df = fetch_data_from_db()
    return render_template("report.html", tables=[df.to_html(classes='table table-bordered', index=False)], title="Customer Shopping Report")

if __name__ == "__main__":
    app.run(debug=True)
