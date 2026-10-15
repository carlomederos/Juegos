from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from extensions import db
from models import User
from auth import auth
from auth.forms import LoginForm, RegistrationForm

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('juegos'))

    form = RegistrationForm()

    if form.validate_on_submit():
        usuario_existente = User.query.filter_by(
            username=form.username.data
        ).first()

        if usuario_existente:
            flash('Ese nombre de usuario ya está registrado.')
            return redirect(url_for('auth.register'))

        usuario = User(username=form.username.data)
        usuario.password = form.password.data

        db.session.add(usuario)
        db.session.commit()

        flash('Cuenta creada correctamente. Ya puedes ingresar.')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('juegos'))

    form = LoginForm()

    if form.validate_on_submit():
        usuario = User.query.filter_by(
            username=form.username.data
        ).first()

        if usuario is None or not usuario.verify_password(
            form.password.data
        ):
            flash('Usuario o contraseña incorrectos.')
            return redirect(url_for('auth.login'))

        login_user(usuario, remember=form.remember_me.data)
        flash('Has iniciado sesión correctamente.')

        return redirect(url_for('juegos'))

    return render_template('auth/login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.')
    return redirect(url_for('auth.login'))