import pickle
from flask import Flask, request, render_template, redirect, url_for, session, flash
from functools import wraps
import numpy as np
import pandas as pd
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

from sklearn.preprocessing import StandardScaler

application = Flask(__name__)

app = application
app.secret_key = 'your-secret-key-change-in-production'

# Demo users (in production, use a database with hashed passwords)
USERS = {
    'admin': 'admin123'
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

##Route for a home page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and USERS[username] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')

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