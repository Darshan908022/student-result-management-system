from flask import Blueprint, render_template, request, session, redirect, url_for
from config import db
from firebase_admin import auth

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id_token = request.form.get('idToken')
        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            user_doc = db.collection('users').document(uid).get()
            if not user_doc.exists:
                return render_template('login.html', error='User not found in database!')
            user_data = user_doc.to_dict()
            session['uid'] = uid
            session['role'] = user_data['role']
            session['name'] = user_data['name']
            role = user_data['role']
            if role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif role == 'faculty':
                return redirect(url_for('faculty.dashboard'))
            else:
                return redirect(url_for('student.dashboard'))
        except Exception as e:
            return render_template('login.html', error=str(e))
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
