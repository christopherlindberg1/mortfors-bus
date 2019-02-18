from wtforms import Form, StringField, TextAreaField, PasswordField, BooleanField, validators


class Register(Form):
    email = StringField("E-post", [validators.Email()])
    firstname = StringField("Förnamn", [validators.DataRequired()])
    lastname = StringField("Efternamn", [validators.DataRequired()])
    country = StringField("Land", [validators.DataRequired()])
    city = StringField("Stad", [validators.DataRequired()])
    post_nr = StringField("Postnummer", [validators.DataRequired()])
    street = StringField("Gata", [validators.DataRequired()])
    tel_nr = StringField("Telefonnummer")
    password = PasswordField("Lösenord", [validators.DataRequired(), validators.EqualTo("confirm", message="Fel lösenord")])
    confirm = PasswordField("Bekräfta lösenord")


class Login(Form):
    email = StringField("E-post", [validators.Email()])
    password = PasswordField("Lösenord", [validators.DataRequired()])
    remember_me = BooleanField("Kom ihåg mig")