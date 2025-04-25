# Import core Flask utilities and response handling tools
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, Response
from .forms import ExpenseForm, RegisterForm, LoginForm
from .models import Expense, db, User
from flask_login import login_user, logout_user, login_required, current_user
import csv
import io


# Define route blueprints for separating main and auth functionality
auth = Blueprint('auth', __name__)
main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index() -> Response:
    """
    Displays the homepage with a form to log new expenses and a table of recent expenses.

    Params:
        GET: Displays the expense form and expense history.
        POST: Handles form submission to create a new expense.

    Returns:
        Response: Rendered index page with form and expense list.
    """
    # Instantiate the expense form
    form = ExpenseForm()

    # If form is submitted and valid, save the new expense to the database
    if form.validate_on_submit():
        expense = Expense(
            amount=form.amount.data,
            category=form.category.data,
            description=form.description.data,
            date=form.date.data or None,
            user_id=current_user.id
        )
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for('main.index'))

    # Query all expenses in reverse chronological order for display
    expenses = Expense.query.order_by(Expense.date.desc()).all()

    # Render the index page with the form and expenses
    return render_template('index.html', form=form, expenses=expenses)


@auth.route('/register', methods=['GET', 'POST'])
def register() -> Response:
    """
    Handles new user registration.

    Params:
        GET: Displays the registration form.
        POST: Creates a new user and hashes their password.

    Returns:
        Response: Redirect to login or render registration form.
    """
    # Instantiate the registration form
    form = RegisterForm()

    # If form is submitted and valid, create the user and save to database
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('auth.login'))

    # Render the registration form
    return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login() -> Response:
    """
    Handles user login.

    Params:
        GET: Displays the login form.
        POST: Authenticates the user and logs them in.

    Returns:
        Response: Redirect to homepage or re-render login form on failure.
    """
    # Instantiate the login form
    form = LoginForm()

    # On valid form submission, attempt user login
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # If user exists and password is correct, log them in
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))

        # Flash error message if login fails
        flash('Invalid credentials', 'danger')

    # Render the login form
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout() -> Response:
    """
    Logs out the currently authenticated user.

    Returns:
        Response: Redirect to homepage.
    """
    # Log out the user
    logout_user()

    # Redirect to home page
    return redirect(url_for('main.index'))


@main.route('/profile')
@login_required
def profile() -> Response:
    """
    Displays the user profile page.

    Returns:
        Response: Rendered profile page.
    """
    # Render a basic profile template
    return render_template('profile.html')


@main.route('/dashboard')
@login_required
def dashboard() -> Response:
    """
    Displays a pie chart of expense distribution by category for the current user.

    Returns:
        Response: Rendered dashboard page with chart data.
    """
    from sqlalchemy import func

    # Aggregate expenses by category and sum the amount for each
    data = db.session.query(
        Expense.category,
        func.sum(Expense.amount)
    ).filter_by(user_id=current_user.id).group_by(Expense.category).all()

    # Extract categories and values into separate lists
    labels = [d[0] for d in data]
    values = [float(d[1]) for d in data]

    # Render the dashboard template with labels and values for Chart.js
    return render_template('dashboard.html', labels=labels, values=values)


@main.route('/export/csv')
@login_required
def export_csv() -> Response:
    """
    Exports the user's expenses to a downloadable CSV file.

    Returns:
        Response: CSV file with all expenses for the current user.
    """
    # Query all expenses for the current user
    expenses = Expense.query.filter_by(user_id=current_user.id).all()

    # Create an in-memory string buffer for CSV writing
    si = io.StringIO()
    cw = csv.writer(si)

    # Write CSV header
    cw.writerow(['Amount', 'Category', 'Description', 'Date'])

    # Write each expense as a row in the CSV
    for expense in expenses:
        cw.writerow([
            expense.amount,
            expense.category,
            expense.description or '',
            expense.date.strftime('%Y-%m-%d')
        ])

    # Convert the buffer to a response with CSV MIME type
    output = Response(si.getvalue(), mimetype='text/csv')
    output.headers['Content-Disposition'] = 'attachment; filename=expenses.csv'

    return output
