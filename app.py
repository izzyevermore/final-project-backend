import sqlite3
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Defining the function that opens sqlite database and creates table
def create_student_table():
    connect = sqlite3.connect('apacademy.db')
    print("Databases has opened")

    connect.execute('CREATE TABLE IF NOT EXISTS students (userid INTEGER PRIMARY KEY AUTOINCREMENT, fullname TEXT, age INTEGER, username TEXT, password TEXT, email_address TEXT)')
    print("Table was created successfully")
    connect.close()


create_student_table()

# Route for opening the registration form and rendering template
@app.route('/')
@app.route('/register-student/', methods=['GET'])
def register_form():
    return render_template('register.html')

# Fetching form info and adding user to database
@app.route('/')
@app.route('/add-student/', methods=['POST'])
def add_student():
    try:
        fullname = request.form['name']
        age = request.form['age']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm']
        email = request.form['email']

        if password == confirm_password:
            with sqlite3.connect('apacademy.db') as con:
                cursor = con.cursor()
                cursor.execute("INSERT INTO students (fullname, age, username, password, email_address) VALUES (?, ?, ?, ?, ?)", (fullname, age, username, password, email))
                con.commit()
                msg = username + " was added to the databases"
    except Exception as e:
        con.rollback()
        msg = "Error occured in insert" + str(e)
    finally:
        con.close()
    return render_template('results.html', msg=msg)

@app.route('/show-students/', methods=['GET'])
def show_students():
    students = []
    try:
        with sqlite3.connect('apacademy.db') as connect:
            cursor = connect.cursor()
            cursor.execute("SELECT * FROM students")
            students = cursor.fetchall()
    except Exception as e:
        connect.rollback()
        print("There was an error fetching results from the database: " + str(e))
    finally:
        connect.close()
        return jsonify(students)


@app.route('/login/', methods=['POST'])
def login():
    try:
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect('apacademy.db') as con:
            mycursor = con.cursor()
            mycursor.execute('SELECT * FROM students WHERE username = ? and password = ?', (username, password))
            con.commit()
            message = username + " has logged in."
    except Exception as e:
        con.rollback()
        msg = "There was a problem logging in try again later " + str(e)
    finally:
        con.close()
        return render_template('index.html', msg=msg)




