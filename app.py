from flask import Flask, redirect, url_for
from config import db

app = Flask(__name__)
app.secret_key = "student-result-secret-key"

from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.faculty import faculty_bp
from routes.student import student_bp

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(faculty_bp, url_prefix='/faculty')
app.register_blueprint(student_bp, url_prefix='/student')

@app.route('/')
def home():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
