from flask import Flask,flash, render_template, request, redirect, session
import mysql.connector
from datetime import date
from functools import wraps

from nlp import feedback_analytics
from flask_bcrypt import Bcrypt

import yaml

with open("./helpers/config.yaml", "r") as stream:
    try:
        data=(yaml.safe_load(stream))
    except yaml.YAMLError as exc:
        print(exc)

bcrypt = Bcrypt()
app = Flask(__name__)
app.secret_key = data['SECRET_KEY']
#app = Flask(__name__)
#bcrypt = Bcrypt(app)  # initialize with app


try:
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Varshith@30',
        database='americanairlines'
    )
except:
    print('Connection failed')

@app.route('/')
def select_user_or_admin():
    if 'user_id' not in list(session) and 'admin_id' not in list(session): 
        return render_template('select.html')
    elif 'user_id' in list(session):
        return render_template('/user/login.html',message='Logout properly')
    elif 'admin_id' in list(session):
        return render_template('/admin/login.html',message='Logout properly')
    
    
@app.route('/select', methods=['POST'])
def process_selection():
    option = request.form['option']
    if option == 'user':
        return redirect('/user/login')
    elif option == 'admin':
        return redirect('/admin/login')
    else:
        return redirect('/')

# User Side

#@app.route('/user/login', methods=['GET', 'POST'])
#def user_login():
 #   if request.method == 'POST':
  #      email = request.form['email']
   #     password = request.form['password']
    #    cursor = db.cursor()
     #   cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
      #  user = cursor.fetchone()

        #if user and bcrypt.check_password_hash(user[3], password):
        #if user and user[3] and bcrypt.check_password_hash(user[3], password):
         #   session['user_id'] = user[0]
          #  session['user_name'] = user[1]
        #    return render_template('user/dashboard.html', username=session['user_name'])
        #else:
         #  return render_template('user/login.html', error='Invalid credentials')
    #return render_template('user/login.html')
   
@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        if user:
            try:
                if user[3] and bcrypt.check_password_hash(user[3], password):
                    session['user_id'] = user[0]
                    session['user_name'] = user[1]
                    return render_template('user/dashboard.html', username=session['user_name'])
                else:
                    return render_template('user/login.html', error='Invalid credentials')
            except ValueError:
                return render_template('user/login.html', error='Corrupted password hash. Please reset your password or contact support.')
        else:
            return render_template('user/login.html', error='Invalid credentials')
    # This line ensures GET requests return the login page
    return render_template('user/login.html')

   

@app.route('/user/signup', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        if not name or not email or not password:
            return render_template('user/signup.html', error='All fields are required')
        
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        if user:
            return render_template('user/signup.html', error='Email is already registered')
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        #new_hashed_password = bcrypt.generate_password_hash(user[3]).decode('utf-8')
        cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)', (name, email, hashed_password))
        #cursor.execute('UPDATE users SET password = %s WHERE email = %s', (new_hashed_password, email))
        db.commit()
        
        return redirect('/user/login')

    return render_template('user/signup.html')

def login_required_user(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user_id' in list(session):
            return f(*args, **kwargs)
        else:
            return render_template('user/login.html', error='You need to login!!')
            return redirect('/user/login')

    return wrap
def login_required_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_id' in list(session):
            return f(*args, **kwargs)
        else:
            return render_template('admin/login.html', error='You need to login!!')
            return redirect('/admin/login')

    return wrap



@app.route('/user/dashboard')
@login_required_user
def user_dashboard():
        return render_template('user/dashboard.html',username=session['user_name'])

@app.route('/user/search', methods=['GET', 'POST'])
@login_required_user
def search_flights():
    import datetime
    if 'user_id' in session:
        if request.method == 'POST':
            date = request.form['date']
            time = request.form['time']
            fromm = request.form['fromm']
            to = request.form['to']
            cursor = db.cursor()
            cursor.execute('SELECT * FROM flights WHERE date = %s AND time = %s AND `from` = %s AND `to` = %s ', (date, time,fromm,to,))
            flights = cursor.fetchall()
            return render_template('user/flights.html', flights=flights)
        
        cursor = db.cursor()
        today=(datetime.date.today()).strftime("%Y-%m-%d")
        cursor.execute('SELECT * FROM flights WHERE date = %s',(today,))
        today_flights = cursor.fetchall()
        #print(today_flights)
        return render_template('user/search.html',today_flights=today_flights) 
    else:
        return redirect('/user/login')

@app.route('/user/book/<int:flight_id>', methods=['GET', 'POST'])
@login_required_user
def book_flight(flight_id):
    if 'user_id' in session:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM flights WHERE id = %s', (flight_id,))
        flight = cursor.fetchone()

        if request.method == 'POST':
            total_seats_needed = int(request.form['seats_needed'])
            available_seats = int(flight[5])

            if total_seats_needed <= available_seats:
                new_available_seats = available_seats - total_seats_needed
                cursor.execute('UPDATE flights SET seat_count = %s WHERE id = %s', (new_available_seats, flight_id))
                cursor.execute('INSERT INTO bookings (user_id, flight_id, seats_booked) VALUES (%s, %s, %s)', (session['user_id'], flight_id, total_seats_needed))
                db.commit()
                return render_template('user/confirmation.html', flight=flight, seats_booked=total_seats_needed, total_price=total_seats_needed * int(flight[4]))
            else:
                return render_template('user/book.html', flight=flight, error='Insufficient seats')

        return render_template('user/book.html', flight=flight)
    else:
        return redirect('/user/login')



@app.route('/user/mybookings')
@login_required_user
def my_bookings():
    if 'user_id' in session:
        query = '''
        SELECT users.id, users.username, flights.flight_number,flights.date,flights.time,flights.from,flights.to, bookings.seats_booked
        FROM bookings
        INNER JOIN users ON bookings.user_id = users.id
        INNER JOIN flights ON bookings.flight_id = flights.id
        WHERE bookings.user_id = %s
        '''
        
        cursor = db.cursor()
        cursor.execute(query, (session['user_id'],))
        bookings = cursor.fetchall()
        
        return render_template('/user/mybookings.html', bookings=bookings)
    else:
        return redirect('/user/login')

@app.route('/user/feedback', methods=['GET', 'POST'])
@login_required_user
def feedback():
    if 'user_id' in session:
        if request.method == 'POST':
            feedback = request.form['feedback']
            

            if  not feedback:
                return render_template('user/feedback.html', error='Please enter')
            
            cursor = db.cursor()
            cursor.execute('INSERT INTO feedback (user_id, message) VALUES (%s, %s)',
                           (session['user_id'], feedback))
            db.commit()
            return render_template('user/thankyou.html')

        return render_template('user/feedback.html')
    else:
        return redirect('/user/login')


@app.route('/user/logout')
@login_required_user
def user_logout():
    session.clear()
    #print('At logout')
    #print(session)
    flash("You have been logged out!")
    return redirect('/user/login')


# Admin Side

@app.route('/admin/login', methods=['GET', 'POST'])
#def admin_login():
 #   if request.method == 'POST':
  #      username = request.form['username']
   #     password = request.form['password']
    #    
     #   cursor = db.cursor()
      #  cursor.execute('SELECT * FROM admins WHERE username = %s', (username,))
       # admin = cursor.fetchone()
#
 #       cursor.fetchall()
#
 #       #if admin and bcrypt.check_password_hash(admin[3], password):
  ##         session['admin_id'] = admin[0]
    #        session['admin_username'] = admin[1]
     #       return render_template('admin/dashboard.html')
      #  else:
       #     return render_template('admin/login.html', error='Invalid credentials')
#
    #return render_template('admin/login.html')
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = db.cursor()
        cursor.execute('SELECT * FROM admins WHERE username = %s', (username,))
        admin = cursor.fetchone()
        cursor.fetchall()
        if admin and admin[3] and bcrypt.check_password_hash(admin[3], password):
                    session['admin_id'] = admin[0]
                    session['admin_username'] = admin[1]
                    return render_template('admin/dashboard.html')
        else:
                # This handles the "Invalid salt" error
                  return render_template('admin/login.html', error='Invalid credentials')
    return render_template('admin/login.html')


@app.route('/admin/add_admin', methods=['GET', 'POST'])
@login_required_admin
def add_admin():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        con_password = request.form['con_password']
        admin_key = request.form['admin key']
        key=data['key']
        
        if not username or not password:
            return render_template('admin/add_admin.html', error='All fields are required')
        if password != con_password:
            return render_template('admin/add_admin.html', error="Password doesn't match")
        if admin_key != key:
            return render_template('admin/add_admin.html', error="Enter valid admin key")
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        cursor = db.cursor()
        cursor.execute('INSERT INTO admins (username,email, password) VALUES (%s,%s, %s)', (username,email, hashed_password))
        db.commit()
        
        return render_template('admin/login.html',error='Added succesfully')

    return render_template('admin/add_admin.html')

@app.route('/admin/dashboard')
@login_required_admin
def admin_dashboard():
        return render_template('admin/dashboard.html')

@app.route('/admin/flights')
@login_required_admin
def admin_flights():
    if 'admin_id' in session:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM flights')
        flights = cursor.fetchall()
        return render_template('admin/flights.html', flights=flights)
    else:
        return redirect('/admin/login')
    

@app.route('/admin/add_flight', methods=['GET', 'POST'])
@login_required_admin
def add_flight():
    if request.method == 'POST':
        flight_number = request.form['flight_number']
        date = request.form['date']
        time = request.form['time']
        price = request.form['price']
        seat_count = request.form['seat count']
        fromm = request.form['fromm']
        to = request.form['to']

        cursor = db.cursor()
        cursor.execute('SELECT flight_number FROM flights')
        data = cursor.fetchall()
        string_list = [''.join(item) for tup in data for item in tup]
        print(string_list)
        
        if flight_number in list(string_list):
            print(string_list)
            message='Opps Flight number already exists'
            return render_template('admin/success_add.html',message_error=message)
        else:

            query = "INSERT INTO flights (flight_number, date, time, price, seat_count, `from` , `to`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor = db.cursor()
            cursor.execute(query, (flight_number, date, time,price ,seat_count,fromm,to))
            db.commit()
            message='Flight added succesfully'
            
            return render_template('admin/success_add.html',message=message)
    
    return render_template('admin/add_flight.html')


@app.route('/admin/remove_flight', methods=['GET', 'POST'])
@login_required_admin
def remove_flight():
    if request.method == 'POST':
        flight_id = request.form['flight_id']
        remove_query = "DELETE FROM flights WHERE id = %s"
        cursor = db.cursor()
        cursor.execute(remove_query, (flight_id,))
        db.commit()
        return render_template('/admin/success_remove.html')

    else:
        fetch_query = "SELECT * FROM flights"
        cursor = db.cursor()
        cursor.execute(fetch_query)
        flights = cursor.fetchall()
        return render_template('admin/remove_flight.html', flights=flights)



@app.route('/admin/view_feedback')
@login_required_admin
def view_feedback():

    query = "SELECT * FROM feedback"
    cursor = db.cursor()
    cursor.execute(query)
    feedback = cursor.fetchall()
    
    return render_template('admin/view_feedback.html', feedback=feedback)

@app.route('/admin/bookings/<int:flight_id>')
@login_required_admin
def admin_bookings(flight_id):
    if 'admin_id' in session:
        cursor = db.cursor()
        cursor.execute('SELECT F.flight_number,U.username,U.email,B.seats_booked FROM flights as F INNER JOIN bookings as B Inner join users as U ON F.id=B.flight_id and B.user_id=U.id WHERE F.id= %s', (flight_id,))
        bookings = cursor.fetchall()
        return render_template('admin/bookings.html', bookings=bookings)
    else:
        return redirect('/admin/login')


@app.route('/admin/nlp')
@login_required_admin
def nlp():
    chart_filename = feedback_analytics.analyze()
    return render_template('admin/analytics.html', chart_filename=chart_filename)


@app.route('/admin/logout')
@login_required_admin
def admin_logout():

    session.clear()
    flash("You have been logged out!")
    return redirect('/admin/login')


if __name__ == '__main__':
    app.run(debug=True)
    app = Flask(__name__)#static_folder="C:\\Users\\suriy\\OneDrive\\Desktop\\Devrev\\Flask sample 2""

