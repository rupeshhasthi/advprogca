from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from app import db
from app.models import Expense, User
from app.forms import ExpenseForm, RegisterForm, LoginForm
from functools import wraps
from datetime import datetime

main = Blueprint("main", __name__)


# Authentication Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)

    return decorated_function


# Register
@main.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered.", "danger")
            return redirect(url_for("main.register"))
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please login.", "success")
        return redirect(url_for("main.login"))
    return render_template("register.html", form=form)


# Login
@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session["user_id"] = user.id
            flash("Logged in successfully.", "success")
            return redirect(url_for("main.index"))
        else:
            flash("Invalid credentials.", "danger")
    return render_template("login.html", form=form)


# Logout
@main.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("main.login"))


# Home / Dashboard
@main.route("/")
@login_required
def index():
    user_id = session["user_id"]
    total = (
        db.session.query(db.func.sum(Expense.amount))
        .filter_by(user_id=user_id)
        .scalar()
        or 0
    )
    return render_template("index.html", total=total)


# View Expenses
@main.route("/expenses")
@login_required
def expenses():
    user_id = session["user_id"]
    all_expenses = (
        Expense.query.filter_by(user_id=user_id).order_by(Expense.datetime.desc()).all()
    )
    return render_template("expenses.html", expenses=all_expenses)


# Add Expense
@main.route("/add", methods=["GET", "POST"])
@login_required
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        new_expense = Expense(
            category=form.category.data,
            amount=form.amount.data,
            note=form.note.data,
            user_id=session["user_id"],
        )
        db.session.add(new_expense)
        db.session.commit()
        flash("Expense added.", "success")
        return redirect(url_for("main.expenses"))
    return render_template("add_expense.html", form=form)


# Delete Expense
@main.route("/delete/<int:expense_id>", methods=["POST"])
@login_required
def delete_expense(expense_id):
    user_id = session["user_id"]
    expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first_or_404()
    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted.", "info")
    return redirect(url_for("main.expenses"))
