from wtforms import Form, StringField, TextAreaField, PasswordField, BooleanField, validators


class RegistrationForm(Form):
    email = StringField("Email", [validators.Email()])
    firstname = StringField("First name", [validators.DataRequired()])
    lastname = StringField("Last name", [validators.DataRequired()])
    country = StringField("Country", [validators.DataRequired()])
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
