from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms import validators
from wtforms import DateField


class FestForm(FlaskForm):
    fest_name = StringField("Name: ", [
        validators.DataRequired("Please enter name of the event"),
        validators.Length(3, 20, "Name should be from 3 to 20 symbols")
    ])

    fest_date = DateField("Date: ", [validators.DataRequired("Please enter the date of the event")])

    people_email = StringField("Email: ", [
        validators.Length(3, 20, "Name should be from 3 to 20 symbols"),
        validators.Email("Wrong email format"),
        validators.DataRequired("Please enter your email")
    ])

    place_name = StringField("Place: ", [
        validators.DataRequired("Please enter the name of place."),
        validators.Length(3, 20, "Name should be from 3 to 20 symbols")
    ])

    place_adress = StringField("Address: ", [
        validators.DataRequired("Please enter your place address."),
        validators.Length(3, 100, "Name should be from 3 to 100 symbols")
    ])

    place_price = IntegerField("Price: ", [
        validators.NumberRange(0, 10000000000, "Should be from 0 to 10000000000 symbols"),
    ])

    submit = SubmitField("Save")

    def validate_date(self):
        return bool(self.fest_date.data.year > 2020)


