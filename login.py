from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from db import get_db_connection  # Assuming db.py contains the get_db_connection function

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aptkey'

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Query to check if the user exists
        query = """
            SELECT id, username, email, password FROM Admin WHERE email = %s
        """
        cursor.execute(query, (email,))
        admin = cursor.fetchone()
        cursor.close()
        connection.close()

        if admin:
            # Check if the hashed password matches
            if check_password_hash(admin['password'], password):
                session['user'] = admin['username']
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid credentials. Please try again.', 'danger')
        else:
            flash('User does not exist.', 'danger')

    return render_template('login.html')

# Route for logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)