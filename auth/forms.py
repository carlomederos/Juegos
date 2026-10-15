from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField(
        'Usuario',
        validators=[DataRequired()]
    )

    password = PasswordField(
        'Contraseña',
        validators=[DataRequired()]
    )

    remember_me = BooleanField('Recordarme')

    submit = SubmitField('Ingresar')

class RegistrationForm(FlaskForm):
    username = StringField(
        'Usuario',
        validators=[
            DataRequired(),
            Length(min=3, max=64)
        ]
    )

    password = PasswordField(
        'Contraseña',
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )

    confirm_password = PasswordField(
        'Confirmar contraseña',
        validators=[
            DataRequired(),
            EqualTo(
                'password',
                message='Las contraseñas deben coincidir.'
            )
        ]
    )

    submit = SubmitField('Registrarse')