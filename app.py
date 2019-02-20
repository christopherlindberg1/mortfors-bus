from flask import Flask, render_template, request, flash, redirect, url_for, session
import mysql.connector
from passlib.hash import sha256_crypt
from functools import wraps

# Imports from other project files
from forms import Register, Login

app = Flask(__name__)

# Connects to a local MySQL server
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "clean417k(dj",
    database = "mortfors",
    )


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
    """ Returns the start page """

    return render_template("index.html")


@app.route("/register/", methods=["GET", "POST"])
def register():
    """ Registers a new user """

    form = Register(request.form)

    if request.method == "GET":
        return render_template("register.html", form=form, title="Registrera")

    elif request.method == "POST" and form.validate():
        try:
            email = form.email.data
            firstname = form.firstname.data.strip().title()
            lastname = form.lastname.data.strip().title()
            country = form.country.data.strip().title()
            city = form.city.data.strip().title()
            post_nr = form.post_nr.data
            street = form.street.data.strip().title()
            tel_nr = form.street.data
            password = sha256_crypt.encrypt(str(form.password.data))

            cur = db.cursor(dictionary=True)

            # Registers a new user
            cur.execute("""INSERT INTO customer VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (email, firstname, lastname, country,
                         city, post_nr, street, tel_nr, password))
            db.commit()
            cur.close()

            flash('You are registered and can now log in', 'success')
            return redirect(url_for("login"))
        except:
           flash('An account is already registered with this email address',
                 'danger')
           return redirect(url_for("register"))


@app.route("/login/", methods=["GET", "POST"])
def login():
    """ Logs in a user if email and password match """

    form = Login(request.form)
    if request.method == "POST":
        email = request.form["email"]
        password_candidate = request.form["password"]

        cur = db.cursor(dictionary=True)

        # Pulls data about a user with a certain email, if there is one
        result = cur.execute("SELECT * FROM customer WHERE email = %s",
                             (email,))
        data = cur.fetchone()

        if len(data) != 0:

            password = data["password"]
            email = data["email"]
            if sha256_crypt.verify(password_candidate, password):
                session["logged_in"] = True
                session["email"] = email
                firstname = data["firstname"]
                flash("Welcome " + firstname + "!", "success")
                return redirect(url_for("index"))
            else:
                flash("Invalid password", "danger")
                return render_template("login.html", form=form)
            cur.close()
        else:
            flash("Found no registered user with this email address",
            "danger")
            return render_template("login.html", form=form)
    else:
        return render_template("login.html", form=form, title="Logga in")


@app.route("/logout/")
@is_logged_in
def logout():
    """ Logs a user out by clearing the session object """

    session.clear()
    return redirect(url_for("index"))


@app.route("/trips/")
def trips():
    """ Lists all available trips """

    cur = db.cursor(dictionary=True)

    # Pulls data about all available trips
    cur.execute("""SELECT * FROM trip WHERE empty_seats != 0
                   ORDER BY startdest, enddest, starttime""")
    trips = cur.fetchall()

    if len(trips) != 0:
        return render_template("trips.html", trips=trips)
    return render_template("trips.html")


@app.route("/trip/<trip_id>", methods=["GET", "POST"])
@is_logged_in
def trip(trip_id):
    """ Shows informaion about a single trip """
    cur = db.cursor(dictionary=True)
    # Fixa join med City så att gatuadress hämtas

    # Pulls data about a specific trip
    cur.execute("SELECT * FROM trip WHERE trip_id = %s",
    (trip_id,))
    trip_info = cur.fetchone()

    if request.method == "GET":
        return render_template("trip.html", trip_info=trip_info)

    elif request.method == "POST":
        try:
            nr_of_seats = request.form["nr_of_seats"]
            seats_left = int(trip_info["empty_seats"]) - int(nr_of_seats)
            cur = db.cursor(dictionary=True)

            # Updates the amount of empty seats after a booking
            cur.execute("UPDATE trip SET empty_seats = %s WHERE trip_id = %s",
                        (seats_left, trip_id))

            # Registers the booking
            cur.execute("INSERT INTO booking VALUES (%s, %s, %s)",
                        (session["email"], trip_id, nr_of_seats))

            flash("Thank you for your booking", "success")

            # Commits only of both queries were executed successfully
            db.commit()
            cur.close()
            return redirect(url_for("my_trips"))
        except: # Fix so that the specific exception is caught!
            flash('You have already booked this trip. Go to "My bookings"\
                   if you want to edit your booking.', 'success')
            return render_template("trip.html", trip_info=trip_info)


@app.route("/my_trips/")
@is_logged_in
def my_trips():
    """ Shows a user all of their bookings, if there are any """

    cur = db.cursor(dictionary=True)

    # Pulls information about all bookings for a certain user
    cur.execute("""
    SELECT t.trip_id, t.startdest, t.enddest, t.starttime,
    t.arrival, b.nr_of_seats
    FROM trip as t
    JOIN booking as b
    ON b.email = %s AND t.trip_id = b.trip_id
    ORDER BY starttime""",
    (session["email"],))

    trips = cur.fetchall()

    if len(trips) != 0:
        return render_template("my_trips.html", trips=trips)
    return render_template("my_trips.html")


@app.route("/edit_trip/<trip_id>", methods=["GET", "POST"])
@is_logged_in
def edit_trip(trip_id):
    """ Edits the amount of seats in a user's booking """

    cur = db.cursor(dictionary=True)

    # Pulls information about a specific booking
    cur.execute("""
    SELECT b.email, b.trip_id, b.nr_of_seats,
    t.trip_id, t.startdest, t.enddest, t.starttime,
    t.arrival, t.price, t.empty_seats
    FROM booking as b
    JOIN trip as t
    ON b.trip_id = %s AND b.trip_id = t.trip_id AND email = %s""",
    (trip_id, session["email"]))

    trip_data = cur.fetchone()

    if request.method == "GET":
        return render_template("edit_trip.html", trip_data=trip_data)

    elif request.method == "POST":
        updated_nr_of_seats = int(request.form["nr_of_seats"])
        cur = db.cursor(dictionary=True)

        # Updates a booking
        cur.execute("""UPDATE booking SET nr_of_seats = %s WHERE email = %s
        AND trip_id = %s""",
        (updated_nr_of_seats, session["email"], trip_id))

        diff_amount_of_seats = trip_data["nr_of_seats"] - updated_nr_of_seats
        updated_empty_seats = trip_data["empty_seats"] + diff_amount_of_seats

        # Updates the amount of empty seats after a booking update
        cur.execute("""UPDATE trip SET empty_seats = %s
        WHERE trip_id = %s""",
        (updated_empty_seats, trip_id))

        # Commits only if both queries were executed successfully
        db.commit()
        cur.close()
        flash("Your changes has been saved", "success")
        return redirect(url_for("my_trips"))


@app.route("/cancel_trip/<trip_id>", methods=["POST"])
@is_logged_in
def cancel_trip(trip_id):
    """ Cancels a user's booking """

    cur = db.cursor(dictionary=True)

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
        return redirect(url_for("my_trips"))

    # Removes a user's booking
    cur.execute("DELETE FROM booking WHERE trip_id = %s AND email = %s",
    (trip_id, session["email"]))

    # Updates the amount of available seats
    cur.execute("""UPDATE trip SET empty_seats = empty_seats + %s
                   WHERE trip_id = %s""",
                   (nr_of_seats, trip_id))

    """ Can this be done with fewer queries? """

    # Commits only if the two last queries were executed successfully
    db.commit()
    cur.close()

    flash("Your booking has been removed", "success")
    return redirect(url_for("my_trips"))


if __name__ == "__main__":
    app.secret_key='b8123f83ef5752b099e260a90f42d855\
                    e328142f2986f9e8d66c7c864aefe521'
    app.run(debug=True)
