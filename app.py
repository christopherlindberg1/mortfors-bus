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
    """Used to make certain pages only visible to logged in users"""
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("För att ta del av den här sidan måste du vara inloggad", "success")
            return redirect(url_for("login"))
    return wrap


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register/", methods=["GET", "POST"])
def register():
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

            flash('Du är nu registrerad och kan logga in', 'success')
            return redirect(url_for("login"))
        except:
           flash('Det finns redan ett konto registrerat på denna e-post',
                 'danger')
           return redirect(url_for("register"))


@app.route("/login/", methods=["GET", "POST"])
def login():
    form = Login(request.form)
    if request.method == "POST":
        email = request.form["email"]
        password_candidate = request.form["password"]

        cur = db.cursor(dictionary=True)

        # Pulls data about a user with a certain email, if there is one
        result = cur.execute("SELECT * FROM customer WHERE email = %s",
                             (email,))
        data = cur.fetchone()
        print(data)
        if len(data) != 0:

            password = data["password"]
            email = data["email"]
            if sha256_crypt.verify(password_candidate, password):
                session["logged_in"] = True
                session["email"] = email
                firstname = data["firstname"]
                flash("Välkommen " + firstname + "!", "success")
                return redirect(url_for("index"))
            else:
                flash("Ogiltigt lösenord", "danger")
                return render_template("login.html", form=form)
            cur.close()
        else:
            flash("Ingen användare med denna epost hittades", "danger")
            return render_template("login.html", form=form)
    else:
        return render_template("login.html", form=form, title="Logga in")


@app.route("/logout/")
@is_logged_in
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/trips/")
def trips():
    cur = db.cursor(dictionary=True)

    # Pulls data about all available trips
    cur.execute("SELECT * FROM trip ORDER BY startdest, enddest, starttime")
    trips = cur.fetchall()
    return render_template("trips.html", trips=trips)


@app.route("/trip/<trip_id>", methods=["GET", "POST"])
@is_logged_in
def trip(trip_id):
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

            flash("Tack för din bokning", "success")

            # Commits only of both queries were executed successfully
            db.commit()
            cur.close()
            return redirect(url_for("my_trips"))
        except: # Fix so that the specific exception is caught!
            flash('Du har redan bokat denna resan. Gå till "Mina bokningar"\
                   om du vill redigera din bokning.', 'success')
            return render_template("trip.html", trip_info=trip_info)


@app.route("/my_trips/")
@is_logged_in
def my_trips():
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
        flash("Dina ändringar har sparats", "success")
        return redirect(url_for("my_trips"))


@app.route("/cancel_trip/<trip_id>", methods=["GET", "POST"])
@is_logged_in
def cancel_trip(trip_id):
    cur = db.cursor(dictionary=True)

    # Removes a user's booking
    cur.execute("DELETE FROM booking WHERE trip_id = %s AND email = %s",
    (trip_id, session["email"]))

    #Fix so that nr of available seats also is updated
    # Updaterar antalet lediga platser
    # cur.execute()

    db.commit()
    cur.close()


if __name__ == "__main__":
    app.secret_key='b8123f83ef5752b099e260a90f42d855\
                    e328142f2986f9e8d66c7c864aefe521'
    app.run(debug=True)
