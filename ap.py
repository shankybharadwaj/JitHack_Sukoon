from flask import Flask, redirect, url_for, request
from pymongo import MongoClient

app = Flask(__name__)

myclient = MongoClient('mongodb://localhost:27017/')
db = myclient['SB']
collection_1 = db['Login_details']
collection_2 = db['Personal_deatils']

@app.route('/',methods = ['POST','GET'])

def signup() : 
    if request.method == 'POST' : 
        username = request.form['username']
        password = request.form['password']
        confrim_password = request.form['confrim_password']

        if password == confrim_password : 
            user_data = {
                'Username' : username,
                'Paswword' : password
            }
            collection_1.insert_one(user_data)
            return redirect(url_for('login'))
        else : 
            return "Passwords donot match"
    return (redirect(url_for('signup')))

if __name__ == "__main__" : 
    app.run(debug=True)