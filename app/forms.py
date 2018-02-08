from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class ButtonForm(FlaskForm):
    label = "Submit"
    submit = SubmitField(label=label)
    recaptcha = RecaptchaField()

