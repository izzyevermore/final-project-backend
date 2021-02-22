import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

def create_student_table():
    connect = sqlite3.connect('apacademy.db')
    print("Databases has opened")

    connect.execute('CREATE TABLE IF NOT EXISTS students (userid INTEGER PRIMARY KEY AUTOINCREMENT, fullname TEXT, age INTEGER, username TEXT, password TEXT, email_address TEXT)')
    print("Table was created successfully")
    connect.close()


create_student_table()

@app.route('/')
@app.route('/register-student/')
def register_form():
    return render_template('register.html')

@app.route('/')
@app.route('/add-student/', methods=['POST'])
def add_student():
    if request.method == "POST":
        try:
            fullname = request.form['name']
            age = request.form['age']
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm']
            email = request.form['email']

            with sqlite3.connect('apacademy.db') as con:
                cursor = con.cursor()
                cursor.execute("INSERT INTO students (fullname, age, username, password, email) VALUES (?, ?, ?, ?, ?)", (fullname, age, username, password, email))
                con.commit()
                msg = username + "was added to the databases"
        except Exception as e:
            con.rollback()
            msg = "Error occured in insert" + str(e)

        finally:
            con.close()
            return render_template('results.html', msg=msg)


