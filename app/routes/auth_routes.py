from flask import render_template,request,redirect,url_for,Blueprint,flash,session
from werkzeug.security import generate_password_hash,check_password_hash
from app.models import db,User

authentication_bp=Blueprint('authentication', __name__)

@authentication_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        username=request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
#Checking if the user laready exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('This email already has an account. You can Login')
            return redirect(url_for('authentication.login'))
#Now adding the user to the database
        user = User(full_name=full_name, username=username ,email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please login.','warning')
        return redirect(url_for('authentication.login'))

    return render_template('register.html')

@authentication_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        #Checking if the user exists or not
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
           #checking wether it is the user or admin 
            if user.is_admin:
                return redirect(url_for('dashboard.admin'))
            else:
                return redirect(url_for('dashboard.user'))
        else:
            flash('Invalid credentials','danger')
    
    return render_template('login.html')

@authentication_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()  # clears all session data (works for admin or user)
    return redirect(url_for('landing.landing'))  # send them to landing page
