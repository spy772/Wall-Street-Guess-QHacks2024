from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2

app = Flask(__name__, template_folder='template')
app.secret_key = 'StockGuessFTW'

# Connect to the database 
conn = psycopg2.connect(database="StockGuess", user="edward", 
                        password="x", host="localhost", port="5432") 

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/')
@app.route('/login.html')
def login():
    if session:
        session.pop('loggedin', None)
        session.pop('email', None)
        session.pop('location', None)
        session.pop('guesstoday', None)
        session.pop('streak', None)
    return render_template('login.html')

@app.route('/stats.html')
def stats():
    conn = psycopg2.connect(database="StockGuess", user="edward", 
                        password="x", host="localhost", port="5432") 
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE email = %s', 
                  (session['email'],))
    user = cur.fetchone()

    if user:
        data = {
            'location': user[2],
            'guesstoday': user[3],
            'streak': user[4]
        }
        return render_template('stats.html', data=data)

    return render_template('stats.html')

@app.route('/about.html')
def about():
    return render_template('about.html')  

@app.route('/signup', methods=['POST'])
def signup():
    conn = psycopg2.connect(database="StockGuess", user="edward", 
                        password="x", host="localhost", port="5432") 
    cur = conn.cursor()

    email = request.form['email']
    password = request.form['pswd']
    location = request.form['location']

    cur.execute('SELECT * FROM users WHERE email = %s', 
                  (email,))

    user = cur.fetchone()

    if user:
        return redirect(url_for('login'))
    else:
        cur.execute('''INSERT INTO users \
                    (email, password, location) VALUES (%s, %s, %s)''',
                    (email,password,location,))
        conn.commit()

        cur.execute('SELECT * FROM users WHERE email = %s', 
                  (email,))

        user = cur.fetchone()
        session['loggedin'] = True
        session['email'] = user[0]
        session['location'] = user[2]
        session['guesstoday'] = user[3]
        session['streak'] = user[4]
        return redirect(url_for('index'))

@app.route('/submit', methods=['POST'])
def submit():
    conn = psycopg2.connect(database="StockGuess", user="edward", 
                        password="x", host="localhost", port="5432") 
    cur = conn.cursor()

    email = request.form['email']
    password = request.form['pswd']

    cur.execute('SELECT * FROM users WHERE email = %s AND password = %s', 
                  (email, password, ))

    user = cur.fetchone()

    if user:
        session['loggedin'] = True
        session['email'] = user[0]
        session['location'] = user[2]
        session['guesstoday'] = user[3]
        session['streak'] = user[4]
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/higher')
def higher():
    conn = psycopg2.connect(database="StockGuess", user="edward", 
                        password="x", host="localhost", port="5432") 
    cur = conn.cursor()
    cur.execute("SELECT guesstoday FROM users WHERE email=%s", (session['email'],))

    guess = cur.fetchone()
    print(session['email'])
    print(guess)
    print("HIGHER")
    if guess[0] == None:
        cur.execute("UPDATE users SET guesstoday = 'Higher' WHERE email=%s", (session['email'],))
        conn.commit()

    return redirect(url_for('index'))

@app.route('/lower')
def lower():
    conn = psycopg2.connect(database="StockGuess", user="edward", 
                        password="x", host="localhost", port="5432") 
    cur = conn.cursor()
    cur.execute("SELECT guesstoday FROM users WHERE email=%s", (session['email'],))

    guess = cur.fetchall()
    print(guess)
    print("LOWER")
    if guess[0] == None:
        cur.execute("UPDATE users SET guesstoday = 'Lower' WHERE email=%s", (session['email'],))
        conn.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
