from wtforms import Form, StringField, TextAreaField, PasswordField
from wtforms import SelectField, BooleanField, IntegerField
from wtforms.validators import Email, DataRequired, EqualTo, NumberRange
from helper_data import countries, times_traveled



class RegistrationForm(Form):
    email = StringField("Email", validators=[Email(), DataRequired()])
    firstname = StringField("First name", validators=[DataRequired()])
    lastname = StringField("Last name", validators=[DataRequired()])
    country = SelectField(u"Country", choices=countries)
    city = StringField("City", validators=[DataRequired()])
    zip = StringField("ZIP code", validators=[DataRequired()])
    street = StringField("Street", validators=[DataRequired()])
    tel_nr = StringField("Phone")
    password = PasswordField("Password", validators=[DataRequired(),
            EqualTo("confirm", message="Fel lösenord")])
    confirm = PasswordField("Confirm password")


class LoginForm(Form):
    email = StringField("Email", validators=[Email(), DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")


class AddDestinationForm(Form):
    city_name = StringField("City", validators=[DataRequired()])
    country = SelectField(u"Country", choices=countries)
    zip = StringField("ZIP code", validators=[DataRequired()])
    street = StringField("Street", validators=[DataRequired()])


class CreateTripForm(Form):
    pass


class TimesTraveledForm(Form):
    times_traveled = SelectField("Number of trips", choices=times_traveled)
