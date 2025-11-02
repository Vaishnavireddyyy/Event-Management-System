from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Path to your SQLite database
db_path = os.path.join(os.path.dirname(__file__), 'event.db')

# Initialize database (create tables if not exist)
def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Events (
                        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        event_name TEXT NOT NULL,
                        event_date TEXT NOT NULL,
                        venue TEXT NOT NULL
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Participants (
                        participant_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        event_id INTEGER,
                        FOREIGN KEY (event_id) REFERENCES Events(event_id)
                    )''')
    conn.commit()
    conn.close()

init_db()

# -------------------- ROUTES --------------------

@app.route('/')
def home():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Events")
    events = cursor.fetchall()
    conn.close()
    return render_template('index.html', events=events)

@app.route('/add_event', methods=['POST'])
def add_event():
    name = request.form['event_name']
    date = request.form['event_date']
    venue = request.form['venue']

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Events (event_name, event_date, venue) VALUES (?, ?, ?)", (name, date, venue))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    conn = sqlite3.connect('event.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Events WHERE event_id = ?", (event_id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/register')
def register():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Events")
    events = cursor.fetchall()
    conn.close()
    return render_template('register.html', events=events)

@app.route('/register_participant', methods=['POST'])
def register_participant():
    name = request.form['name']
    email = request.form['email']
    event_id = request.form['event_id']

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Participants (name, email, event_id) VALUES (?, ?, ?)", (name, email, event_id))
    conn.commit()
    conn.close()

    return redirect('/participants')

@app.route('/participants')
def participants():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""SELECT p.participant_id, p.name, p.email, e.event_name
                      FROM Participants p 
                      JOIN Events e ON p.event_id = e.event_id""")
    participants = cursor.fetchall()
    conn.close()
    return render_template('view.html', participants=participants)

# -------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
