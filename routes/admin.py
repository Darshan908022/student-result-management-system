from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from config import db
from firebase_admin import auth
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'admin':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    students = db.collection('users').where('role', '==', 'student').get()
    faculty = db.collection('users').where('role', '==', 'faculty').get()
    subjects = db.collection('subjects').get()
    stats = {'students': len(students), 'faculty': len(faculty), 'subjects': len(subjects)}
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/add-user', methods=['GET', 'POST'])
@admin_required
def add_user():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        department = request.form.get('department')
        reg_no = request.form.get('reg_no', '')
        try:
            user = auth.create_user(email=email, password=password, display_name=name)
            user_data = {'name': name, 'email': email, 'role': role, 'department': department}
            if role == 'student':
                user_data['reg_no'] = reg_no
            db.collection('users').document(user.uid).set(user_data)
            flash(name + ' added successfully!', 'success')
            return redirect(url_for('admin.users'))
        except Exception as e:
            flash('Error: ' + str(e), 'danger')
    return render_template('admin/add_user.html')

@admin_bp.route('/users')
@admin_required
def users():
    students = db.collection('users').where('role', '==', 'student').get()
    faculty = db.collection('users').where('role', '==', 'faculty').get()
    return render_template('admin/users.html', students=students, faculty=faculty)

@admin_bp.route('/add-subject', methods=['GET', 'POST'])
@admin_required
def add_subject():
    faculty_list = db.collection('users').where('role', '==', 'faculty').get()
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        department = request.form.get('department')
        semester = request.form.get('semester')
        faculty_uid = request.form.get('faculty_uid')
        try:
            db.collection('subjects').add({'name': name, 'code': code, 'department': department, 'semester': int(semester), 'faculty_uid': faculty_uid})
            flash('Subject ' + name + ' added successfully!', 'success')
            return redirect(url_for('admin.subjects'))
        except Exception as e:
            flash('Error: ' + str(e), 'danger')
    return render_template('admin/add_subject.html', faculty_list=faculty_list)

@admin_bp.route('/subjects')
@admin_required
def subjects():
    subjects = db.collection('subjects').get()
    return render_template('admin/subjects.html', subjects=subjects)
