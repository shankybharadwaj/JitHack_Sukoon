from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import datetime as datetime

app = Flask(__name__)
app.secret_key = "prg"  
bcrypt = Bcrypt(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
users_collection = db['users']  
profiles_collection = db['profiles']

@app.route('/')
def home_page() : 
    return render_template('login.html')
@app.route('/signPage')
def signuppage() : 
    return render_template('signup.html')
@app.route('/datehtml')
def datehtml() : 
    return render_template('date.html')
#signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password == confirm_password:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user_data = {'username': username, 'password': hashed_password}
            users_collection.insert_one(user_data)
            return render_template('login1.html')
        else:
            return "Passwords do not match"
    return render_template('signup.html')
#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_collection.find_one({'username': username})
        if user and bcrypt.check_password_hash(user['password'], password):
            session['username'] = username
            return render_template('profile.html')
        else:
            return "Invalid username or password"
    return render_template('login.html')
#login1
@app.route('/login1', methods=['GET', 'POST'])
def login1():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_collection.find_one({'username': username})
        if user and bcrypt.check_password_hash(user['password'], password):
            session['username'] = username
            return render_template('doctor.html')
        else:
            return "Invalid username or password"
    return render_template('login.html')
#profile
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' in session:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            ph_no = request.form['ph_no']
            dob = request.form['dob']
            occ = request.form['occ']
            username = session['username']
            data = {'name': name, 'email': email, 'username': username, 'ph_no' : ph_no, 'dob': dob, 'occ': occ}
            profiles_collection.insert_one(data)
            return render_template("doctor.html")
        return render_template('profile.html')
    return render_template('login.html')

#appointment date 
@app.route('/appointment', methods=['POST'])
def appointment():
    if 'username' in session:
        date = request.form.get('date')
        time = request.form.get('time')
        if date and time:
            appointment_date = datetime.datetime.strptime(date, '%Y-%m-%d')
            current_date = datetime.datetime.now()

            if appointment_date.date() < current_date.date():
                return "Cannot book an appointment for a past date."

            data1 = {'date': date, 'time': time, 'username': session['username']}
            profiles_collection.insert_one(data1)
            return "Appointment fixed "
        else:
            return "Date or Time not provided"
    else:
        return "Username not found"

         
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
