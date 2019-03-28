from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_bcrypt import Bcrypt
from functools import wraps
import forms
import db_functions
import destinations
import sys
sys.path.append("../")
import config
from datetime import datetime


app = Flask(__name__)
app.config["SECRET_KEY"] = config.secret_key
bcrypt = Bcrypt(app)


def is_logged_in(f):
    """ Used to make certain pages only visible to logged in users """
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("To access this page you have to be logged in",
            "success")
            return redirect(url_for("login"))
    return wrap


@app.route("/")
def index():
    """ Returns the landing page """
    return render_template("index.html")


@app.route("/register/", methods=["GET", "POST"])
def register():
    """ Registers a new user """
    if session:
        return redirect(url_for("index"))

    form = forms.RegistrationForm(request.form)
    if request.method == "GET":
        return render_template("register.html", form=form, title="Register")

    elif request.method == "POST":
        try:
            email = form.email.data
            firstname = form.firstname.data.strip().title()
            lastname = form.lastname.data.strip().title()
            country = form.country.data.strip().title()
            city = form.city.data.strip().title()
            zip = form.zip.data.strip()
            street = form.street.data.strip().title()
            tel_nr = form.tel_nr.data.strip()
            password = bcrypt.generate_password_hash(
                       form.password.data).decode("utf-8")

            conn = db_functions.create_db_conn()
            cur = db_functions.create_db_cur(conn)
            cur.execute("""INSERT INTO customer VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (email, firstname, lastname, country,
                         city, zip, street, tel_nr, password))
            conn.commit()
            cur.close()
            conn.close()

            session["logged_in"] = True
            session["email"] = email

            flash(f"Welcome to Mortfors Bus, {firstname}!", "success")
            return redirect(url_for("index"))
        except:
           flash("An account is already registered with this email address",
                 "danger")
           return redirect(url_for("register"))


@app.route("/login/", methods=["GET", "POST"])
def login():
    """ Customer log in """
    if session:
        return redirect(url_for("index"))

    form = forms.LoginForm(request.form)
    if request.method == "GET":
        return render_template("login.html", form=form, title="Log in")

    elif request.method == "POST":
        email = request.form["email"]
        password_candidate = request.form["password"]

        conn = db_functions.create_db_conn()
        cur = db_functions.create_db_cur(conn)

        # Pulls data about a user with a certain email, if there is one
        cur.execute("SELECT * FROM customer WHERE email = %s",
                             (email,))
        data = cur.fetchone()
        cur.close()
        conn.close()

        if data != None:
            password_hash = data["password"]
            email = data["email"]
            if bcrypt.check_password_hash(password_hash, password_candidate):
                session["logged_in"] = True
                session["email"] = email
                firstname = data["firstname"]
                flash("Welcome " + firstname + "!", "success")
                return redirect(url_for("index"))
            else:
                flash("Email and password does not match", "danger")
                return render_template("login.html", form=form)
        else:
            flash("Email and password does not match",
            "danger")
            return render_template("login.html", form=form)


@app.route("/admin_login/", methods=["GET", "POST"])
def admin_login():
    """ Admin log in """
    if session:
        return redirect(url_for("index"))

    form = forms.LoginForm(request.form)
    if request.method == "GET":
        return render_template("a_admin_login.html", form=form, title="Admin Login")

    elif request.method == "POST":
        email = request.form["email"]
        password_candidate = request.form["password"]

        conn = db_functions.create_db_conn()
        cur = db_functions.create_db_cur(conn)

        # Pulls data about an admin with a certain email, if there is one
        cur.execute("SELECT * FROM admin WHERE email = %s",
                             (email,))
        data = cur.fetchone()
        cur.close()
        conn.close()

        if data != None:
            password_hash = data["password"]
            email = data["email"]
            if bcrypt.check_password_hash(password_hash, password_candidate):
                session["logged_in"] = True
                session["email"] = email
                session["admin"] = True
                flash("Welcome, Boss", "success")
                return redirect(url_for("admin_cp"))
            else:
                return redirect(url_for("admin_login"))
        else:
            return redirect(url_for("admin_login"))


@app.route("/logout/")
@is_logged_in
def logout():
    """ Logs a user out by clearing the session object """
    session.clear()
    return redirect(url_for("index"))


@app.route("/trips/")
def trips():
    """ Lists all available trips """
    conn = db_functions.create_db_conn()
    cur = db_functions.create_db_cur(conn)
    cur.execute("""SELECT * FROM trip WHERE empty_seats != 0
                    ORDER BY startdest, enddest, departure""");
    trips = cur.fetchall()
    cur.close()
    conn.close()

    if len(trips) != 0:
        return render_template("trips.html", trips=trips)
    return render_template("trips.html")


@app.route("/trip/<trip_id>", methods=["GET", "POST"])
@is_logged_in
def trip(trip_id):
    """ Shows informaion about a single trip """
    conn = db_functions.create_db_conn()
    cur = db_functions.create_db_cur(conn)

    # Pulls all relevant data about an individual trip by trip_id
    cur.execute("""SELECT t.trip_id, t.startdest, t.enddest, t.departure,
    t.arrival, t.price, t.empty_seats, d.firstname, d.lastname,
    c1.street AS startstreet, c2.street AS arrivalstreet,
    c1.country AS startcountry, c2.country AS arrivalcountry
    FROM trip AS t
    JOIN city AS c1 ON t.startdest = c1.city_name
    JOIN city AS c2 ON t.enddest = c2.city_name
    JOIN driver AS d ON t.driver = d.pers_nr AND t.trip_id = %s""",
    (trip_id,))

    trip_info = cur.fetchone()

    if trip_info == None:
        return redirect(url_for("trips"))

    if request.method == "GET":
        return render_template("trip.html", trip_info=trip_info)

    elif request.method == "POST":
        try:
            nr_of_seats = request.form["nr_of_seats"]
            seats_left = int(trip_info["empty_seats"]) - int(nr_of_seats)

            # Registers the booking
            cur.execute("INSERT INTO booking VALUES (%s, %s, %s)",
                        (session["email"], trip_id, nr_of_seats))

            # Updates the amount of empty seats after a booking
            cur.execute("UPDATE trip SET empty_seats = %s WHERE trip_id = %s",
                        (seats_left, trip_id))

            flash("Thank you for your booking", "success")

            # Commits transaction if both queries were executed successfully
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for("my_bookings"))
        except:
            flash('You have already booked this trip. Go to "My bookings"\
                   if you want to edit your booking.', 'success')
            return render_template("trip.html", trip_info=trip_info)


@app.route("/my_bookings/")
@is_logged_in
def my_bookings():
    """ Shows a user all of their bookings, if there are any """
    if "admin" in session:
        return redirect(url_for("admin_cp"))

    conn = db_functions.create_db_conn()
    cur = db_functions.create_db_cur(conn)

    # Pulls information about all bookings for a certain user
    cur.execute("""
    SELECT t.trip_id, t.startdest, t.enddest, t.departure,
    t.arrival, b.nr_of_seats
    FROM trip as t
    JOIN booking as b
    ON b.email = %s AND t.trip_id = b.trip_id
    ORDER BY departure""",
    (session["email"],))

    bookings = cur.fetchall()
    cur.close()
    conn.close()

    if len(bookings) != 0:
        return render_template("my_bookings.html", bookings=bookings)
    return render_template("my_bookings.html")


@app.route("/edit_booking/<trip_id>", methods=["GET", "POST"])
@is_logged_in
def edit_booking(trip_id):
    """ Edits the amount of seats in a user's booking """
    if "admin" in session:
        return redirect(url_for("admin_cp"))

    conn = db_functions.create_db_conn()
    cur = db_functions.create_db_cur(conn)

    # Pulls information about a specific booking
    cur.execute("""
    SELECT b.email, b.trip_id, b.nr_of_seats,
    t.trip_id, t.startdest, t.enddest, t.departure,
    t.arrival, t.price, t.empty_seats
    FROM booking as b
    JOIN trip as t
    ON b.trip_id = %s AND b.trip_id = t.trip_id AND email = %s""",
    (trip_id, session["email"]))

    trip_data = cur.fetchone()
    cur.close()
    conn.close()

    if request.method == "GET":
        return render_template("edit_booking.html", trip_data=trip_data)

    elif request.method == "POST":
        updated_nr_of_seats = int(request.form["nr_of_seats"])
        conn = db_functions.create_db_conn()
        cur = db_functions.create_db_cur(conn)

        # Updates a booking
        cur.execute("""UPDATE booking SET nr_of_seats = %s,
        last_edit_timestamp = %s WHERE email = %s
        AND trip_id = %s""",
        (updated_nr_of_seats, datetime.now(), session["email"], trip_id))
        # Want to have current datetime without microseconds

        diff_amount_of_seats = trip_data["nr_of_seats"] - updated_nr_of_seats
        updated_empty_seats = trip_data["empty_seats"] + diff_amount_of_seats

        # Updates the amount of empty seats after a booking update
        cur.execute("""UPDATE trip SET empty_seats = %s
        WHERE trip_id = %s""",
        (updated_empty_seats, trip_id))

        # Commits transaction if both queries were executed successfully
        conn.commit()
        cur.close()
        conn.close()
        flash("Your changes has been saved", "success")
        return redirect(url_for("my_bookings"))


@app.route("/cancel_booking/<trip_id>", methods=["POST"])
@is_logged_in
def cancel_booking(trip_id):
    """ Cancels a user's booking """
    if "admin" in session:
        return redirect(url_for("admin_cp"))

    conn = db_functions.create_db_conn()
    cur = db_functions.create_db_cur(conn)

    # Pulls nr of booked seats for the booking that shall be deleted
    cur.execute("""SELECT nr_of_seats FROM booking
                   WHERE email = %s and trip_id = %s""",
                   (session["email"], trip_id))
    data = cur.fetchone()

    try:
        nr_of_seats = data["nr_of_seats"]
    except TypeError:
        # data["nr_of_seats"] generates TypeError if
        # the query above finds no match
        flash("You have not booked this trip", "success")
        return redirect(url_for("my_bookings"))

    # Removes a user's booking
    cur.execute("DELETE FROM booking WHERE trip_id = %s AND email = %s",
    (trip_id, session["email"]))

    # Updates the amount of available seats
    cur.execute("""UPDATE trip SET empty_seats = empty_seats + %s
                   WHERE trip_id = %s""",
                   (nr_of_seats, trip_id))

    # Commits transaction if the last two queries were executed successfully
    conn.commit()
    cur.close()
    conn.close()
    flash("Your booking has been removed", "success")
    return redirect(url_for("my_bookings"))


@app.route("/admin_cp/")
def admin_cp():
    """ Admin control panel """
    if "admin" not in session:
        return redirect(url_for("index"))
    return render_template("a_admin_cp.html", title="Control Panel")


@app.route("/destinations/", methods=["GET", "POST"])
def destinations():
    """ Control page for destinations """
    if "admin" not in session:
        return redirect(url_for("index"))

    form = forms.AddDestinationForm(request.form)

    conn = db_functions.create_db_conn()
    cur = db_functions.create_db_cur(conn)
    cur.execute("SELECT * FROM city ORDER BY country, city")
    destinations = cur.fetchall()
    cur.close()
    conn.close()

    if request.method == "GET":
        return render_template("a_destinations.html", form=form,
                destinations=destinations, title="Destinations")

    elif request.method == "POST":
        city_name = request.form["city_name"].strip().title()
        country = request.form["country"]
        zip = request.form["zip"]
        street = request.form["street"].strip().title()

        conn = db_functions.create_db_conn()
        cur = db_functions.create_db_cur(conn)
        cur.execute("INSERT INTO city VALUES (%s, %s, %s, %s)",
                    (city_name, country, zip, street))
        conn.commit()
        cur.close()
        conn.close()
        flash(f"{city_name} has been added to your list of destinations",
               "success")
        return redirect(url_for("destinations"))


@app.route("/a_trips/")
def our_trips():
    """ Control page for trips """
    if "admin" not in session:
        return redirect(url_for("index"))

    conn = db_functions.create_db_conn()
    cur = db_functions.create_db_cur(conn)
    cur.execute("""SELECT t.trip_id, t.startdest, t.enddest,
    t.departure, t.arrival, t.price, t.empty_seats,
    d.firstname, d.lastname
    FROM trip as t JOIN driver as d
    ON t.driver = d.pers_nr
    ORDER BY startdest, enddest, departure""")
    trips = cur.fetchall()
    cur.close()
    conn.close()
    print(trips)

    return render_template("a_trips.html", trips=trips,
            title="Our trips")


@app.route("/edit_trip/<trip_id>", methods=["GET", "POST"])
def edit_trip(trip_id):
    if "admin" not in session:
        return redirect(url_for("index"))

    if request.method == "GET":
        conn = db_functions.create_db_conn()
        cur = db_functions.create_db_cur(conn)
        cur.execute("""SELECT t.startdest, t.enddest, t.departure,
        t.arrival, t.price, t.empty_seats,
        d.firstname, d.lastname
        FROM trip as t JOIN driver as d
        ON t.driver = d.pers_nr
        WHERE t.trip_id = %s""",
        (trip_id,))

        data = cur.fetchone()

        cur.close()
        conn.close()
        print(data)

        if data == None:
            return redirect(url_for("our_trips"))
        return render_template("a_trip.html", data=data)


@app.route("/create_trip/", methods=["GET", "POST"])
def create_trip():
    """ Route for creating a new trip """
    if "admin" not in session:
        return redirect(url_for("index"))

    form = forms.CreateTripForm(request.form)
    if request.method == "GET":
        return render_template("a_create_trip.html", form=form)

    elif request.method == "POST":
        pass


@app.route("/customers/", methods=["GET", "POST"])
def customers():
    """ Control page for customers """
    if "admin" not in session:
        return redirect(url_for("index"))

    form = forms.TimesTraveledForm(request.form)
    if request.method == "GET":
        return render_template("a_customers.html", form=form,
                customers="no search", title="Customers")

    elif request.method == "POST":
        times_traveled = request.form["times_traveled"]
        conn = db_functions.create_db_conn()
        cur = db_functions.create_db_cur(conn)
        cur.execute("""SELECT firstname, lastname, email, bookings
        FROM nr_bookings_per_person_past_year
        WHERE bookings >= %s""",
        (times_traveled,))
        customers = cur.fetchall()
        cur.close()
        conn.close()

        if len(customers) != 0:
            return render_template("a_customers.html", form=form,
                    customers=customers, times_traveled=times_traveled,
                    title="Customers")
        return render_template("a_customers.html", form=form,
                customers=None, title="Customers")


@app.route("/customer/<email>", methods=["GET", "POST"])
def customer_page(email):
    if "admin" not in session:
        return redirect(url_for("index"))

    conn = db_functions.create_db_conn()
    cur = db_functions.create_db_cur(conn)
    cur.execute("""SELECT c.email, c.firstname, c.lastname, t.startdest,
    t.enddest, b.trip_id, count(b.trip_id) AS nr_bookings
    FROM customer AS c
    JOIN bookings_past_year AS b ON c.email = b.email
    JOIN trip AS t ON t.trip_id = b.trip_id
    WHERE c.email = %s
    GROUP BY c.email, c.firstname, c.lastname, b.trip_id,
    t.startdest, t.enddest""",
    (email,))

    trips = cur.fetchall()
    cur.close()
    conn.close()

    if trips == []:
        return redirect(url_for("customers"))

    return render_template("a_customer.html",
            trips=trips, title="Customer page")


if __name__ == "__main__":
    app.run(debug=True)
