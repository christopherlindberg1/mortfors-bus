from wtforms import Form, StringField, TextAreaField, PasswordField
from wtforms import SelectField, BooleanField, IntegerField
from wtforms.validators import Email, DataRequired, EqualTo, NumberRange
import helper_data


class RegistrationForm(Form):
    email = StringField("Email", validators=[Email(), DataRequired()])
    firstname = StringField("First name", validators=[DataRequired()])
    lastname = StringField("Last name", validators=[DataRequired()])
    country = SelectField(u"Country", choices=helper_data.countries)
    city = StringField("City", validators=[DataRequired()])
    zip = StringField("ZIP code", validators=[DataRequired()])
    street = StringField("Street", validators=[DataRequired()])
    tel_nr = StringField("Phone")
    password = PasswordField("Password", validators=[DataRequired(),
            EqualTo("confirm", message="Password mismatch")])
    confirm = PasswordField("Confirm password")


class AdminRegForm(Form):
    email = StringField("Email", validators=[Email(), DataRequired()])
    firstname = StringField("First name", validators=[DataRequired()])
    lastname = StringField("Last name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(),
            EqualTo("confirm", message="Password mismatch")])
    confirm = PasswordField("Confirm password")


class LoginForm(Form):
    email = StringField("Email", validators=[Email(), DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")


class AddDestinationForm(Form):
    city_name = StringField("City", validators=[DataRequired()])
    country = SelectField(u"Country", choices=helper_data.countries)
    zip = StringField("ZIP code", validators=[DataRequired()])
    street = StringField("Street", validators=[DataRequired()])


class CreateTripForm(Form):
    pass


class ChangeDriver(Form):
    driver = SelectField(u"Driver", choices=helper_data.get_drivers_names())


class TimesTraveledForm(Form):
    times_traveled = SelectField("Number of trips",
            choices=helper_data.times_traveled)
