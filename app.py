from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS patients 
                 (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, gender TEXT, 
                  disease TEXT, admission_date TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/patients')
def patients():
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    c.execute("SELECT * FROM patients")
    patients_list = c.fetchall()
    conn.close()
    return render_template('patients.html', patients=patients_list)

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        disease = request.form['disease']
        
        conn = sqlite3.connect('hospital.db')
        c = conn.cursor()
        c.execute("INSERT INTO patients (name, age, gender, disease, admission_date) VALUES (?, ?, ?, ?, ?)",
                  (name, age, gender, disease, datetime.now().strftime("%Y-%m-%d")))
        conn.commit()
        conn.close()
        return redirect(url_for('patients'))
    return render_template('add_patient.html')

if __name__ == '__main__':
    app.run(debug=True)