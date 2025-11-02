import pickle
import os
from flask import Flask, request, render_template, redirect, url_for, session, flash
from functools import wraps
from authlib.integrations.flask_client import OAuth
import numpy as np
import pandas as pd
from src.pipeline.predict_pipeline import CustomData, PredictPipeline
from database import init_db, create_user, authenticate_user, get_user_by_username, get_user_by_email

from sklearn.preprocessing import StandardScaler

application = Flask(__name__)

app = application
app.secret_key = 'your-secret-key-change-in-production'

# Initialize database
init_db()

# Google OAuth Configuration
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID', 'your-google-client-id'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET', 'your-google-client-secret'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

##Route for a home page

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if len(username) < 3:
            return render_template('signup.html', error='Username must be at least 3 characters long')
        
        if len(password) < 6:
            return render_template('signup.html', error='Password must be at least 6 characters long')
        
        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match')
        
        success, result = create_user(username, email, password)
        
        if success:
            return render_template('signup.html', success='Account created successfully! Please login.')
        else:
            return render_template('signup.html', error=result)
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        success, user = authenticate_user(username, password)
        
        if success:
            session['logged_in'] = True
            session['username'] = user['username']
            session['email'] = user['email']
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')

@app.route('/login/google')
def google_login():
    redirect_uri = url_for('google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/login/google/callback')
def google_callback():
    token = google.authorize_access_token()
    user_info = token.get('userinfo')
    
    if user_info:
        email = user_info.get('email')
        username = email.split('@')[0]
        
        user = get_user_by_email(email)
        
        if not user:
            user = get_user_by_username(username)
            if not user:
                create_user(username, email, None, google_auth=True)
                user = get_user_by_username(username)
        
        session['logged_in'] = True
        session['username'] = username
        session['email'] = email
        session['user_id'] = user['id']
        session['google_user'] = True
        
        return redirect(url_for('index'))
    
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/learnmore')
@login_required
def learnmore():
    return render_template('learnmore.html')
@app.route('/predictdata', methods=['GET','POST'])
@login_required
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        data=CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('writing_score')),
            writing_score=float(request.form.get('reading_score'))

        )
        pred_df=data.get_data_as_data_frame()
        print(pred_df)

        predict_pipeline=PredictPipeline()
        results=predict_pipeline.predict(pred_df)
        value = results[0]
        formatted = f"{float(value):.3f}"
        return render_template('home.html', results=formatted)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0")