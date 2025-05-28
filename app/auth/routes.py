from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo, login_manager
from bson.objectid import ObjectId
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from bson.objectid import ObjectId, InvalidId

auth = Blueprint('auth', __name__)

class User:
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.email = user_data['email']
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    try:
        user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if user_data:
            return User(user_data)
    except (InvalidId, TypeError):
        return None

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = mongo.db.users.find_one({'email': form.email.data})
        if existing_user is None:
            hashed_password = generate_password_hash(form.password.data)
            mongo.db.users.insert_one({
                'username': form.username.data,
                'email': form.email.data,
                'password_hash': hashed_password,
                'created_at': datetime.utcnow()
            })
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('That email is already registered. Please choose a different one.', 'danger')
    
    return render_template('auth/register.html', title='Register', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = mongo.db.users.find_one({'email': form.email.data})
        if user and check_password_hash(user['password_hash'], form.password.data):
            user_obj = User(user)
            login_user(user_obj)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard.home'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    
    return render_template('auth/login.html', title='Login', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))