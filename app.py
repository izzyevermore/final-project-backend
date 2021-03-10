import sqlite3
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import smtplib


app = Flask(__name__)
CORS(app)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

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
    return jsonify(msg=msg)


@app.route('/show-students/', methods=['GET'])
def show_students():
    students = []
    try:
        with sqlite3.connect('apacademy.db') as connect:
            connect.row_factory = dict_factory
            cursor = connect.cursor()
            cursor.execute("SELECT * FROM students")
            students = cursor.fetchall()
    except Exception as e:
        connect.rollback()
        print("There was an error fetching results from the database: " + str(e))
    finally:
        connect.close()
        return jsonify(students)

@app.route('/')
@app.route('/send-email/', methods=['GET'])
def email_sender():
    return render_template('contact.html')


@app.route('/send-email/', methods=["POST", "GET"])
def send_email():
    try:
        email = "izzyevermore123@gmail.com"
        email_2 = request.form['email']
        message = "Thank you for your response!! AP Academy will get back to you shortly regarding the scheduling of your lessons"

        server = smtplib.SMTP('smtp.gmail.com', 587)
        sender_email = email
        receiver_email = email_2
        password = "callmedorg420"

        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        server.quit()
    except smtplib.SMTPException as e:
        return "Something wrong happened: " + str(e)
    return render_template('email-success.html', email=sender_email)


@app.route('/')
@app.route('/delete-student/<int:student_id>/', methods=["GET"])
def delete_student(student_id):
    msg = None
    try:
        with sqlite3.connect('apacademy.db') as con:
            cur = con.cursor()
            cur.execute("DELETE FROM students WHERE username = ? AND password = ?" + str(student_id))
            con.commit()
            msg = "A record was deleted successfully from the database."
    except Exception as e:
        con.rollback()
        msg = "Error occurred when deleting a student in the database: " + str(e)
    finally:
        con.close()
        return jsonify(msg=msg)


@app.route('/display-students/', methods=['GET'])
def display():
    records = []
    try:
        with sqlite3.connect('apacademy.db') as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM students")
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching resuls from database: "+ str(e))
    finally:
        con.close()
        return render_template('students.html', records=records)




if __name__ == '__main__':
    app.run(debug=True)



