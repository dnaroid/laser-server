from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class LoginForm(Form):
    login = StringField('Login', validators=[DataRequired])
    password = PasswordField('Password', validators=[DataRequired])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class AddNewsForm(Form):
    title = StringField('Title', validators=[DataRequired, Length(1, 30)])
    short_text = StringField('Short text',
                             validators=[DataRequired, Length(1, 100)])
    full_text = TextAreaField('Full text',
                              validators=[DataRequired, Length(1, 2000)])
    submit = SubmitField('Add')


class FilterForm(Form):
    filter = SubmitField('Filter')
    reset = SubmitField('Reset')
