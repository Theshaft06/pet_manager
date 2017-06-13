from flask import Flask, request, render_template, redirect, session
from mysqlconnection import MySQLConnector

app = Flask(__name__)
mysql = MySQLConnector(app, 'mydb')

@app.route('/')
def index():
    print "Inside the index method."

    users = mysql.query_db("select id, first_name, last_name from users")
    pets = mysql.query_db("select pets.nickname, pets.type, pets.id, users.first_name as user_firstname, users.last_name as user_lastname from pets join users on pets.user_id = users.id")

    return render_template('index.html', users = users, pets = pets)

@app.route('/create', methods=["POST"])
def create():
    query = "insert into pets (nickname, type, user_id, created_at, updated_at) values (:nickname, :type, :user_id, now(), now())"

    data = {
        'nickname': request.form["nickname"],
        'type': request.form["type"],
        'user_id': request.form["user_id"]
    }

    result = mysql.query_db(query, data)

    print result

    return redirect('/')

app.run(debug=True)