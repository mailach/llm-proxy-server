from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)], render_kw={"class": "form-control", "placeholder": "Enter username"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"class": "form-control", "placeholder": "Enter password"})
    submit = SubmitField('Login', render_kw={"class": "btn btn-primary btn-block"})
