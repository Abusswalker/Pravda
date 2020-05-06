from flask import render_template, redirect
from flask_login import login_user, logout_user, login_required
from app import db
from app.auth.forms import LoginForm, RegisterForm
from app.models import User
from app.main import bp


@bp.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registr.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if db.session.query(User).filter(User.email == form.email.data).first():
            return render_template('registr.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        if db.session.query(User).filter(User.username == form.username.data).first():
            return render_template('registr.html', title='Регистрация',
                                   form=form,
                                   message="Такое имя уже занято")
        user = User(
            username=form.username.data,
            email=form.email.data,
            position=0
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('auth/registr.html', title='Регистрация', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('auth/login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('auth/login.html', title='Авторизация', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

