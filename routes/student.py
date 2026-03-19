from flask import Blueprint, render_template, session, redirect, url_for, make_response
from config import db
from functools import wraps
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

student_bp = Blueprint('student', __name__)

def student_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'student':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@student_bp.route('/dashboard')
@student_required
def dashboard():
    uid = session.get('uid')
    results = db.collection('results').where('student_uid', '==', uid).get()
    result_list = [r.to_dict() for r in results]
    total_subjects = len(result_list)
    passed = sum(1 for r in result_list if r.get('status') == 'Pass')
    failed = total_subjects - passed
    avg = round(sum(r.get('total', 0) for r in result_list) / total_subjects, 2) if total_subjects > 0 else 0
    return render_template('student/dashboard.html', results=result_list, total=total_subjects, passed=passed, failed=failed, avg=avg)

@student_bp.route('/download-marksheet')
@student_required
def download_marksheet():
    uid = session.get('uid')
    user_doc = db.collection('users').document(uid).get().to_dict()
    results = db.collection('results').where('student_uid', '==', uid).get()
    result_list = [r.to_dict() for r in results]
    total_subjects = len(result_list)
    passed = sum(1 for r in result_list if r.get('status') == 'Pass')
    avg = round(sum(r.get('total', 0) for r in result_list) / total_subjects, 2) if total_subjects > 0 else 0
    overall = 'PASS' if passed == total_subjects else 'FAIL'
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []
    title = Paragraph('<b>PANIMALAR ENGINEERING COLLEGE</b>', styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 10))
    subtitle = Paragraph('STUDENT MARKSHEET', styles['Heading2'])
    elements.append(subtitle)
    elements.append(Spacer(1, 20))
    info = [
        ['Student Name:', user_doc.get('name', '-')],
        ['Register No:', user_doc.get('reg_no', '-')],
        ['Department:', user_doc.get('department', '-')],
    ]
    info_table = Table(info, colWidths=[150, 300])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 11),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 20))
    table_data = [['Subject', 'Code', 'Internal', 'External', 'Total', 'Grade', 'Status']]
    for r in result_list:
        table_data.append([r.get('subject_name',''), r.get('subject_code',''), str(r.get('internal',0)), str(r.get('external',0)), str(r.get('total',0)), r.get('grade',''), r.get('status','')])
    result_table = Table(table_data, colWidths=[130, 60, 60, 65, 55, 55, 55])
    result_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.black),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.lightgrey]),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(result_table)
    elements.append(Spacer(1, 20))
    summary = [
        ['Total Subjects:', str(total_subjects)],
        ['Subjects Passed:', str(passed)],
        ['Average Score:', str(avg)],
        ['Overall Result:', overall],
    ]
    summary_table = Table(summary, colWidths=[150, 150])
    summary_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 11),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TEXTCOLOR', (1,3), (1,3), colors.green if overall == 'PASS' else colors.red),
        ('FONTNAME', (1,3), (1,3), 'Helvetica-Bold'),
    ]))
    elements.append(summary_table)
    doc.build(elements)
    buffer.seek(0)
    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=marksheet.pdf'
    return response
