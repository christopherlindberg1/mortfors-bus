from wtforms import Form, StringField, TextAreaField, PasswordField, SelectField, BooleanField, validators
import countries


class RegistrationForm(Form):
    email = StringField("Email", [validators.Email()])
    firstname = StringField("First name", [validators.DataRequired()])
    lastname = StringField("Last name", [validators.DataRequired()])
    country = SelectField(u"Country", choices=countries.countries)
    city = StringField("City", [validators.DataRequired()])
    post_nr = StringField("ZIP code", [validators.DataRequired()])
    street = StringField("Street", [validators.DataRequired()])
    tel_nr = StringField("Phone")
    password = PasswordField("Password", [validators.DataRequired(),
            validators.EqualTo("confirm", message="Fel lösenord")])
    confirm = PasswordField("Confirm password")


class LoginForm(Form):
    email = StringField("Email", [validators.Email()])
    password = PasswordField("Password", [validators.DataRequired()])
    remember_me = BooleanField("Remember me")
