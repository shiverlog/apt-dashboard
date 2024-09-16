from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from db import get_db_connection  # DB 연결 함수

# Blueprint 생성
login_page = Blueprint('login_page', __name__)

# Route for login page
@login_page.route('/login', methods=['GET', 'POST'])
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
                flash('정상적으로 로그인 되었습니다.', 'success')
                return redirect(url_for('/'))
            else:
                flash('인증되지 않았습니다. 다시 시도해주세요', 'danger')
        else:
            flash('Admin 계정이 없습니다.', 'danger')

    return render_template('login.html')