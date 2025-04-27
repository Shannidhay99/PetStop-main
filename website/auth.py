from flask import Blueprint, render_template, request, flash, redirect, url_for, session


auth = Blueprint('auth', __name__)

# Dummy users for authentication
DUMMY_USERS = {
    "user@example.com": {
        "password": "password123",
        "user_id": 1,
        "username": "Regular User"
    },
    "admin@petzilla.com": {
        "password": "admin123",
        "user_id": 999,
        "username": "Admin User"
    }
}

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = DUMMY_USERS.get(email)
        
        if user and user['password'] == password:
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['email'] = email
            flash('Logged in successfully!', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Incorrect email or password.', category='error')
    
    return render_template("login.html")

@auth.route('/logout')
def logout():
    session.clear()  # Clears all session data
    flash('Logged out successfully!', category='success')
    return redirect(url_for('auth.login'))  # Redirect to the login page

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        phone = request.form.get('phone')
        address = request.form.get('address')
        
        # Simple validation
        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(username) < 2:
            flash('Username must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif email in DUMMY_USERS:
            flash('Email already exists.', category='error')
        else:
            # In a real application, we would save the user to the database
            # For now, just show success message and redirect to login
            flash('Account created successfully!', category='success')
            return redirect(url_for('auth.login'))
    
    return render_template('sign_up.html')

@auth.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check specifically for admin credentials
        if email == "admin@petzilla.com" and password == "admin123":
            session['user_id'] = 999
            session['username'] = "Admin User"
            session['email'] = email
            session['is_admin'] = True
            flash('Admin logged in successfully!', category='success')
            return redirect(url_for('views.adminDashboard'))
        else:
            flash('Incorrect admin credentials.', category='error')
    
    return render_template("adlogin.html")
