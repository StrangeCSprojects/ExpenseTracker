# Import core form tools and validators from Flask-WTF and WTForms
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, DateField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo


class RegisterForm(FlaskForm):
    """
    A form for creating a new user account.
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    """
    A form for user login.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ExpenseForm(FlaskForm):
    """
    A form for logging a new expense.
    """
    amount = FloatField('Amount', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('Food', 'Food'), ('Transportation', 'Transportation'),
        ('Entertainment', 'Entertainment'), ('Utilities', 'Utilities'),
        ('Other', 'Other')
    ])
    description = TextAreaField('Description')
    date = DateField('Date', format='%Y-%m-%d')
    submit = SubmitField('Add Expense')
