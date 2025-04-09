from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Load data
df = pd.read_csv('customer_shopping_data.csv')

# Fix date format
df['invoice_date'] = pd.to_datetime(df['invoice_date'], dayfirst=True)

# Calculate total sales
df['total_sales'] = df['quantity'] * df['price']

@app.route('/')
def monthly_sales():
    df['month'] = df['invoice_date'].dt.to_period('M')
    monthly_sales = df.groupby('month')['total_sales'].sum().reset_index()
    monthly_sales['month'] = monthly_sales['month'].astype(str)
    return render_template("monthly_sales.html", sales=monthly_sales.to_dict(orient='records'))

@app.route('/top_customers')
def top_customers_view():
    top5 = df.groupby('customer_id')['total_sales'].sum().reset_index()
    top5 = top5.sort_values('total_sales', ascending=False).head(5)
    return render_template("top_customers.html", data=top5.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
