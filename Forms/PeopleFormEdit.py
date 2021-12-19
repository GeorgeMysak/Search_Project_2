from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms import validators
from wtforms.fields import DateField


class PeopleFormEdit(FlaskForm):
    people_name = StringField("Name: ", [validators.Length(1, 20, "Name should be from 1 to 20 symbols"),
                                         validators.DataRequired("Please enter your name.")])
    people_email = HiddenField("Email: ", [validators.Email("Wrong email format")])
    people_birthday = DateField("Birthday: ", [validators.DataRequired("Please enter your birthday.")])
    people_phone = StringField("Phone: ", [validators.Length(10, 10, "Your phone number must contain 10 symbols"),
                                           validators.DataRequired("Please enter your phone number.")])

    submit = SubmitField("Save")

    def validate_birthday(self):
        return bool(self.people_birthday.data.year > 1900)