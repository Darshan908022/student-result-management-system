from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from config import db
from functools import wraps

faculty_bp = Blueprint('faculty', __name__)

def faculty_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'faculty':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@faculty_bp.route('/dashboard')
@faculty_required
def dashboard():
    uid = session.get('uid')
    subjects = db.collection('subjects').where('faculty_uid', '==', uid).get()
    return render_template('faculty/dashboard.html', subjects=subjects)

@faculty_bp.route('/upload/<subject_id>', methods=['GET', 'POST'])
@faculty_required
def upload_marks(subject_id):
    subject = db.collection('subjects').document(subject_id).get().to_dict()
    students = db.collection('users').where('role', '==', 'student').get()
    if request.method == 'POST':
        for student in students:
            sid = student.id
            internal = request.form.get('internal_' + sid, 0)
            external = request.form.get('external_' + sid, 0)
            internal = int(internal)
            external = int(external)
            total = internal + external
            if total >= 90: grade = 'O'
            elif total >= 80: grade = 'A+'
            elif total >= 70: grade = 'A'
            elif total >= 60: grade = 'B+'
            elif total >= 50: grade = 'B'
            elif total >= 40: grade = 'C'
            else: grade = 'F'
            status = 'Pass' if total >= 40 else 'Fail'
            db.collection('results').add({'student_uid': sid, 'subject_id': subject_id, 'subject_name': subject['name'], 'subject_code': subject['code'], 'internal': internal, 'external': external, 'total': total, 'grade': grade, 'status': status, 'semester': subject['semester']})
        flash('Marks uploaded successfully!', 'success')
        return redirect(url_for('faculty.dashboard'))
    return render_template('faculty/upload.html', subject=subject, subject_id=subject_id, students=students)
