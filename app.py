from flask import Flask, render_template, request, redirect, url_for, flash,session,jsonify
import random
import re
import pandas as pd
import numpy as np
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mahi123'
app.config['MYSQL_DB'] = 'airline_system'

mysql = MySQL(app)
bcrypt = Bcrypt(app)

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    flights = []
    if request.method == 'POST':
        name = request.form['Name']
        dob = request.form['DOB']
        source = request.form['source'].strip().title()
        destination = request.form['destination'].strip().title()

        try:
            df = pd.read_csv('Data_Train.csv')

            df.columns = df.columns.str.strip()

            print("Available Routes:")
            print(df[['Source', 'Destination']].drop_duplicates())

            flights = df[(df['Source'].str.strip().str.title() == source) & 
                         (df['Destination'].str.strip().str.title() == destination)].to_dict(orient='records')

            if not flights:
                flash(f'No flights found from {source} to {destination}.')
        except Exception as e:
            print("Error reading or filtering CSV:", e)
            flash("Something went wrong while fetching flights. Please try again.")
        
    return render_template('Book.html', flights=flights)

@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    name = request.form['name']
    dob = request.form['dob']
    airline = request.form['airline']
    route = request.form['route']
    dep_time = request.form['dep_time']
    arr_time = request.form['arr_time']
    duration = request.form['duration']
    stops = request.form['stops']
    price = request.form['price']
   
    normalized_route = re.sub(r'\s*(-+>|to|→)\s*', ' → ', str(route))
    legs = [leg.strip() for leg in normalized_route.split('→') if leg.strip()]
    
    if len(legs) < 2:
        flash('Invalid route format! Please make sure the route has at least Source → Destination.', 'danger')
        return redirect(url_for('book'))
    
    source = legs[0]
    destination = legs[-1]
    pnr = str(random.randint(100000, 999999))

    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO bookings (name, pnr, source, destination) VALUES (%s, %s, %s, %s)",
                    (name, pnr, source, destination))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        mysql.connection.rollback()
        flash(f"Error saving booking: {e}", "danger")

    return render_template('confirm.html', name=name, dob=dob, airline=airline,
                           route=route, dep_time=dep_time, arr_time=arr_time,
                           duration=duration, stops=stops, price=price, pnr=pnr,
                           source=source, destination=destination)

@app.route('/cancel', methods=['GET', 'POST'])
def cancel():
    if request.method == 'POST':
        pnr = request.form.get('pnr', '').strip()
        print("Form Data Received:", request.form)
        name=request.form.get('name', '').strip()
        reason=request.form.get('reason', '').strip()

        if not pnr or not name or not reason:
            flash("Please fill all fiels.","warning")
            return redirect(url_for('cancel'))

        try:
            cur=mysql.connection.cursor()
            cur.execute("select * from bookings where pnr=%s And name=%s",(pnr,name))
            booking=cur.fetchone()

            if not booking:
                flash("No booking found with given pnr and name.","warning")
                cur.close()
                return redirect(url_for('cancel'))
            cur.execute(
                "INSERT into cancellation(pnr,name,reason) values(%s,%s,%s)",
                (pnr,name,reason)
            )
            cur.execute("delete from bookings where pnr=%s",(pnr,))
            mysql.connection.commit()
            cur.close()
            flash("Your ticket has been cancelled successfully.","success")

        except Exception as e:
            mysql.connection.rollback()
            flash(f"Error during cancellation:{str(e)}","danger")
        
        return redirect(url_for('cancel'))

        
    return render_template('cancel.html')

@app.route('/journey', methods=['GET', 'POST'])
def journey():
    if request.method == 'POST':
        pnr = request.form['PNRNumber'].strip()
        name = request.form['PassengerName'].strip()

        try:
            cursor = mysql.connection.cursor()
            query = "SELECT * FROM bookings WHERE pnr = %s AND name = %s"
            cursor.execute(query, (pnr, name))
            journey_info = cursor.fetchone()
            cursor.close()

            if journey_info:
                return render_template('journey.html', journey_info=journey_info)
            else:
                flash("No journey found with the provided details.", "warning")
                return redirect(url_for('journey'))
        except Exception as e:
            flash(f"Error fetching journey: {str(e)}", "danger")
            return redirect(url_for('journey'))

    return render_template('journey.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('identifier') 
        password = request.form.get('password')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s OR email = %s", (identifier, identifier))
        users = cur.fetchone()
        cur.close()
        print(f"Entered Identifier: {identifier}")
        print(f"Entered Password: {password}")
        if users:
            print(f"User found: {users}")
            
            if users and bcrypt.check_password_hash(users[3], password):  
                session['username'] = users[1]  
                return redirect(url_for('home'))  
                
            
            return redirect(url_for('login'))
           
        else:
            flash("User not found. Please check your credentials.", "danger")

        return redirect(url_for('home'))  

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        username = request.form.get('username')
        password = request.form.get('new-password')
        print("Received Signup Data:", name, email, phone, username, password)
        if not password:
            flash("Password cannot be empty.", "warning")
            return redirect(url_for('signup'))

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, email,password) VALUES (%s, %s, %s)",
                        (username, email,hashed_pw))
        print("Received Signup Data:", name, email, phone, username, password)
        mysql.connection.commit()
        cur.close()
        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/flight-details')
def flight_details():
    cur = mysql.connection.cursor()
    import numpy as np
    df = pd.read_csv('Data_Train.csv')
    df = df.applymap(lambda x: None if isinstance(x, float) and np.isnan(x) else x)
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO flights 
            (airline, source_city, destination_city, route, departure_time, arrival_time, duration, total_stops, additional_info, price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, tuple(row))
    mysql.connection.commit()
    cur.execute("SELECT * FROM flights LIMIT 50,50")
    flights = cur.fetchall()
    # Close the cursor
    cur.close()
    return render_template('flightDet.html', flights=flights)

import MySQLdb.cursors

@app.route('/get', methods=['POST'])
def get_response():
    user_msg = request.json['message'].lower()

    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        if "flight" in user_msg and "from" in user_msg and "to" in user_msg:
            # Extract source and destination
            match = re.search(r"flight from (.+?) to (.+)", user_msg)
            if match:
                source = match.group(1).strip().title()
                destination = match.group(2).strip().title()

                cursor.execute("SELECT * FROM flights WHERE source_city=%s AND destination_city=%s", (source, destination))
                flights = cursor.fetchall()

                if flights:
                    response = "Here are some available flights:\n"
                    for f in flights:
                        response += f"- ✈️ Flight {f['airline']} at {f['departure_time']}\n"
                else:
                    response = "❌No flights found for that route."
            else:
                response = "Please specify source and destination properly."

        elif "pnr" in user_msg:
            pnr = user_msg.split()[-1].strip()
            cursor.execute("SELECT * FROM bookings WHERE pnr=%s", (pnr,))
            booking = cursor.fetchone()
            if booking:
                response = f"🧳 Booking found: Flight from {booking['source'] } to {booking['destination']} of passenger {booking['name']}."
            else:
                response = "⚠️PNR not found. Please check again."

        elif "hello" in user_msg or "hi" in user_msg:
            response = "Hello! I can help you with flights, bookings, or PNR info😊."

        
        elif "bye" in user_msg or "thank you" in user_msg:
            response = "Thanks for chatting with me! Have a great journey! ✈️😊"

        else:
            response = "Sorry, I didn't understand that. Try asking about flights or PNR status😞."

        return jsonify({'response': response})

    except Exception as e:
        return jsonify({'response': f"An error occurred: {str(e)}"})
if __name__ == '__main__':
    app.run(debug=True)
