from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# -------- DATABASE SETUP --------
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS water_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pincode TEXT,
        source TEXT,
        tds REAL,
        ph REAL,
        hardness REAL,
        do REAL
    )''')
    conn.commit()
    conn.close()

init_db()


# -------- LOGIC --------
def check_water_quality(tds, ph, hardness, do):
    if tds < 300 and 6.5 <= ph <= 8.5 and hardness < 200 and do > 5:
        return "Safe for Drinking"
    elif tds < 600 and 6 <= ph <= 9:
        return "Suitable for Agriculture"
    else:
        return "Not Safe"


# -------- ROUTES --------
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        pincode = request.form['pincode']
        source = request.form['source']
        tds = float(request.form['tds'])
        ph = float(request.form['ph'])
        hardness = float(request.form['hardness'])
        do = float(request.form['do'])

        result = check_water_quality(tds, ph, hardness, do)

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO water_data (pincode, source, tds, ph, hardness, do) VALUES (?, ?, ?, ?, ?, ?)",
                  (pincode, source, tds, ph, hardness, do))
        conn.commit()
        conn.close()

    return render_template('index.html', result=result)


@app.route('/data')
def data():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM water_data ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return render_template('data.html', rows=rows)


# -------- RUN --------
if __name__ == '__main__':
    app.run(debug=True)