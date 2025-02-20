from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
from ..models import User
from ..forms import (
    RegistrationForm,
    LoginForm,
)
import base64
from io import BytesIO
from .. import bcrypt
from werkzeug.utils import secure_filename
import base64, io

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("weather.index"))

    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
                "utf-8"
            )
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=hashed_password,
            )
            user.save()
            return redirect(url_for("users.login"))

    return render_template("register.html", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("weather.index"))

    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.objects(username=form.username.data).first()

            if user is not None and bcrypt.check_password_hash(
                user.password, form.password.data
            ):
                login_user(user)
                return redirect(url_for("users.account"))
            else:
                flash("Failed to log in!")

    return render_template("login.html", form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("weather.index"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    return render_template("account.html")
