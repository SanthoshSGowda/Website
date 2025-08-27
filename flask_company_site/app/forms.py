from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=200)])
    slug = StringField("Slug", validators=[DataRequired(), Length(max=220)])
    body = TextAreaField("Body", validators=[DataRequired()])
    published = BooleanField("Published")
    submit = SubmitField("Save")

class ServiceForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=150)])
    description = TextAreaField("Description", validators=[DataRequired()])
    price_inr = IntegerField("Price (INR)", validators=[Optional()])
    submit = SubmitField("Save")

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    subject = StringField("Subject", validators=[Optional(), Length(max=200)])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send Message")
