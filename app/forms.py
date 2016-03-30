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
    short_text = StringField('Short text', validators=[DataRequired, Length(1, 100)])
    full_text = TextAreaField('Full text', validators=[DataRequired, Length(1, 2000)])
    submit = SubmitField('Add')


class FilterForm(Form):
    # def __init__(self, author=0, tags=[]):
    # self.authors = SelectField('Author', default=author, coerce=int,
    #                            choices=[(0, 'All authors')] + [(a.author_id, a.author_name) for
    #                                                            a in Author.query.filter(
    #                                    Author.expired is not None).order_by('author_name')])
    # self.tags = SelectMultipleField('Tags', coerce=int, choices=[(t.tag_id, t.tag_name) for t in
    #                                                              Tag.query.order_by(
    #                                                                  'tag_name')])
    filter = SubmitField('Filter')
    reset = SubmitField('Reset')

    # def update(self, author=0):  # todo check
    #     # self.authors.choices = [(a.author_id, a.author_name) for a in
    #     #                         Author.query.filter(Author.expired is not None).order_by(
    #     #                             'author_name')]
    #     #
    #     # self.tags.choices = [(t.tag_id, t.tag_name) for t in Tag.query.order_by('tag_name')]
    #     self.authors.default = author
