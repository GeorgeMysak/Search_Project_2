from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms import validators
from wtforms.fields import DateField


class FestFormEdit(FlaskForm):
    fest_name = HiddenField("Name: ", [validators.Length(3, 20, "Name should be from 3 to 20 symbols")])
    fest_date = DateField("Date: ", [validators.DataRequired("Please enter date of event")])


    submit = SubmitField("Save")

    def validate_date(self):
        return bool(self.fest_date.data.year > 2020)