from flask import Flask, render_template
import pandas as pd
import sqlite3
import os

app = Flask(__name__)

DATABASE = "sales.db"

def init_db():
    if not os.path.exists(DATABASE):
        df = pd.read_csv("customer_shopping_data.csv")

        # Convert to datetime
        df["invoice_date"] = pd.to_datetime(df["invoice_date"], dayfirst=True)

        # Calculate total sales per row
        df["total"] = df["quantity"] * df["price"]

        # Save to SQLite
        conn = sqlite3.connect(DATABASE)
        df.to_sql("sales", conn, index=False, if_exists="replace")
        conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/monthly_sales')
def monthly_sales():
    conn = sqlite3.connect(DATABASE)
    query = """
        SELECT strftime('%Y-%m', invoice_date) AS month,
               ROUND(SUM(quantity * price), 2) AS monthly_sales
        FROM sales
        GROUP BY month
        ORDER BY month
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return render_template('monthly_sales.html', data=df)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
