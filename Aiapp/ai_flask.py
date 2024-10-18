#  setting up the flask, importing what is needed

from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# creating a database connection
# connecting to the database and sqlite3
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# creating a home route
@app.route('/')
def home():
    return render_template('home.html')

# creating the register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            age = request.form['age']

            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password, age) VALUES (?, ?, ?)', (username, password, age))
            conn.commit()
            conn.close()

            flash('User registered successfully!', 'success')
            return redirect(url_for('login'))

        except KeyError as e:
            flash('Error: Form field missing', 'error')
            return render_template('register.html')

    return render_template('register.html')


# creating the login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()
# if else statement so that the user can login to the database
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

# login out from the database and returning to the home.html or home page
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# creates the main function
if __name__ == '__main__':
    init_db()
    app.run(port=5000, debug=True)