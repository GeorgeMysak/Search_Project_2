from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators


class LoginForm(FlaskForm):
    people_email = StringField("Email: ", [
        validators.Length(3, 20),
        validators.Email("Wrong email format"),
        validators.DataRequired("Please enter your email.")
    ])
    people_password = PasswordField("Password: ", [
        validators.DataRequired("Please enter your password."),
    ])

    submit = SubmitField("Sing In")