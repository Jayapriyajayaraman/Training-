from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DATABASE = 'shopping.db'

# Initialize the DB
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT,
            category TEXT,
            sales REAL
        )
    ''')
    conn.commit()
    conn.close()

# Route to input page
@app.route('/input', methods=['GET', 'POST'])
def input_data():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        category = request.form['category']
        sales = float(request.form['sales'])

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO customers (customer_id, category, sales) VALUES (?, ?, ?)',
                       (customer_id, category, sales))
        conn.commit()
        conn.close()
        return redirect('/report')
    return render_template('input.html')

# Route to report page
@app.route('/report')
def report():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT customer_id, category, SUM(sales) as total_sales FROM customers GROUP BY customer_id, category ORDER BY total_sales DESC')
    data = cursor.fetchall()
    conn.close()
    return render_template('report.html', data=data)

# Home redirects to input
@app.route('/')
def home():
    return redirect('/input')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
