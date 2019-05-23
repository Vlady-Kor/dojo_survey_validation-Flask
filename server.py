from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key="keep it a secret"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=["POST"])
def create():
    is_valid = True
    if len(request.form['name']) < 1:
    	is_valid = False
    	flash("Please enter a first name")
    if len(request.form['location']) < 1:
    	is_valid = False
    	flash("Please enter a last name")
    if len(request.form['language']) < 2:
    	is_valid = False
    	flash("Occupation should be at least 2 characters")
    if len(request.form ['comments']) > 120:
        is_valid = False
        flash("Comments is too long")

    if is_valid:
        mysql = connectToMySQL('dojo_survey')
        query = "INSERT INTO survey (name, dojo_location, favorite_language, comments) VALUES (%(nm)s, %(dl)s, %(fl)s, %(cm)s);"
        data = {
            'nm': request.form['name'],
            'dl': request.form['location'],
            'fl': request.form['language'],
            'cm': request.form['comments']
        }
        user_name = mysql.query_db(query, data)
        print(user_name)
        session['xy'] = user_name
        return redirect('/result')
    return redirect('/')

@app.route('/result')
def results():
    mysql = connectToMySQL('dojo_survey')
    query = 'SELECT * FROM survey WHERE survey_id=%(x)s;'
    data = {
        'x': session['xy']
    }
    username = mysql.query_db(query, data)
    print(data['x'])
    return render_template('result.html', all_users=username)

@app.route("/test")
def test():
    mysql = connectToMySQL('dojo_survey')
    query = 'SELECT * FROM survey;'
    results = mysql.query_db(query)
    print(results)
    return "we hit db for biz"



if __name__ =="__main__":
    app.run(debug=True)