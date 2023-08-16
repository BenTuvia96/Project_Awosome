from flask import Flask, render_template, request, redirect, url_for, flash, session
from sql_connector import SQLConnector

app = Flask(__name__)

# Secret key for the session
app.secret_key = 'some_secret_key'

# Create a connection to the database
conn = SQLConnector(host='localhost', database='project_awsome', user='root', password='Aa123456')

@app.route('/')
def index():
    if 'username' in session:
        user_id = conn.get_user_id_by_username(session['username'])
        balance = conn.get_user_balance(user_id)
        return render_template('dashboard.html', balance=balance)
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        full_name = request.form['full_name']

        conn.insert_user(username, password, email, full_name)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_id = conn.get_user_id_by_username(username)
        if user_id:
            stored_password = conn.get_user_stored_password(user_id)
            if conn.verify_password(stored_password, password):
                session['username'] = username
                session['user_id'] = conn.get_user_id_by_username(username)
                return redirect(url_for('index'))
            else:
                flash('Incorrect password.')
        else:
            flash('User does not exist.')
    return render_template('login.html')

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    if 'username' in session:
        if request.method == 'POST':
            user_id = conn.get_user_id_by_username(session['username'])
            date = request.form['date']
            description = request.form['description']
            category = request.form['category']
            amount = request.form['amount']
            transaction_type = request.form['transaction_type']

            conn.insert_transaction(user_id, date, description, category, amount, transaction_type)
            return redirect(url_for('index'))
        return render_template('add_transaction.html')
    return redirect(url_for('login'))

@app.route('/update_transaction', methods=['GET', 'POST'])
def update_transaction():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        transaction_id = request.form['transaction_id']
        date = request.form['date']
        description = request.form['description']
        category = request.form['category']
        if request.form['amount'] == '':
            amount = 0
        else:
            amount = float(request.form['amount'])
        transaction_type = request.form['transaction_type']

        conn.update_transaction(transaction_id, date, description, category, amount, transaction_type)
        return redirect(url_for('update_transaction'))
    
    # Fetching transactions for the user to display in the table.
    user_id = conn.get_user_id_by_username(session.get('username'))
    print(user_id)
    transactions = conn.get_all_user_transactions(user_id)  # Ensure you have this method or something similar in your conn
    print(transactions)
    return render_template('update_transaction.html', transactions=transactions)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
