from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="L'email è obbligatoria"),
        Email(message="Inserisci un'email valida")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="La password è obbligatoria")
    ])
    remember_me = BooleanField('Ricordami')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="L'username è obbligatorio"),
        Length(min=3, max=80, message="L'username deve essere tra 3 e 80 caratteri")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="L'email è obbligatoria"),
        Email(message="Inserisci un'email valida")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="La password è obbligatoria"),
        Length(min=6, message="La password deve essere di almeno 6 caratteri")
    ])
    confirm_password = PasswordField('Conferma Password', validators=[
        DataRequired(message="La conferma password è obbligatoria"),
        EqualTo('password', message="Le password devono coincidere")
    ]) 