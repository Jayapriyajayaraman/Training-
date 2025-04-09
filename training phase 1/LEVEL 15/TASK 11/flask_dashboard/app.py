from flask import Flask, render_template
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)

# Load and preprocess data
df = pd.read_csv('customer_shopping_data.csv')
df['invoice_date'] = pd.to_datetime(df['invoice_date'], errors='coerce')

# Create a month-year column
df['MonthYear'] = df['invoice_date'].dt.to_period('M').astype(str)

# =========================
# Route 1: Cumulative Sales
# =========================
@app.route('/')
def index():
    monthly_sales = df.groupby('MonthYear')['price'].sum().reset_index()
    monthly_sales['CumulativeSales'] = monthly_sales['price'].cumsum()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_sales['MonthYear'],
        y=monthly_sales['CumulativeSales'],
        mode='lines+markers',
        name='Cumulative Sales',
        line=dict(color='royalblue')
    ))

    fig.update_layout(
        title='Monthly Cumulative Sales',
        xaxis_title='Month-Year',
        yaxis_title='Cumulative Sales',
        title_x=0.5
    )

    graph = pio.to_html(fig, full_html=False)
    return render_template('index.html', graph=graph)

# ================================
# Route 2: Number of Customers
# ================================
@app.route('/customers')
def customer_count():
    monthly_customers = df.groupby('MonthYear')['customer_id'].nunique().reset_index()
    monthly_customers.columns = ['MonthYear', 'UniqueCustomers']

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_customers['MonthYear'],
        y=monthly_customers['UniqueCustomers'],
        mode='lines+markers',
        name='Monthly Customers',
        line=dict(color='green')
    ))

    fig.update_layout(
        title='Number of Unique Customers per Month',
        xaxis_title='Month-Year',
        yaxis_title='Customers',
        title_x=0.5
    )

    graph = pio.to_html(fig, full_html=False)
    return render_template('customers.html', graph=graph)

if __name__ == '__main__':
    app.run(debug=True)
