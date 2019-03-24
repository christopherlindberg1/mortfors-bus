from wtforms import Form, StringField, TextAreaField, PasswordField
from wtforms import SelectField, BooleanField, IntegerField
from wtforms.validators import Email, DataRequired, EqualTo, NumberRange
import countries
import destinations


class RegistrationForm(Form):
    email = StringField("Email", validators=[Email()])
    firstname = StringField("First name", validators=[DataRequired()])
    lastname = StringField("Last name", validators=[DataRequired()])
    country = SelectField(u"Country", choices=countries.countries)
    city = StringField("City", validators=[DataRequired()])
    post_nr = StringField("ZIP code", validators=[DataRequired()])
    street = StringField("Street", validators=[DataRequired()])
    tel_nr = StringField("Phone")
    password = PasswordField("Password", validators=[DataRequired(),
            EqualTo("confirm", message="Fel lösenord")])
    confirm = PasswordField("Confirm password")


class LoginForm(Form):
    email = StringField("Email", validators=[Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")


class AddDestinationForm(Form):
    city_name = StringField("City", validators=[DataRequired()])
    country = SelectField(u"Country", choices=countries.countries)
    post_nr = StringField("ZIP code", validators=[DataRequired()])
    street = StringField("Street", validators=[DataRequired()])


class CreateTripForm(Form):
    # startdest = SelectField(u"City", choices=destinations.destinations)
    # enddest = SelectField(u"City", choices=destinations.destinations)
    # departure = # Timestamp
    # arrival = # Timestamp
    price = StringField("Price")
    # driver = SelectField(u"City", choices=drivers.drivers,
    #         validators=[Optional()])
