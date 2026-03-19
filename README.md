# Student Result Management System

A full-stack web application built with **Python Flask** and **Firebase** for managing student academic results.

## Features
- Role-based login (Admin, Faculty, Student)
- Admin can add students, faculty and subjects
- Faculty can upload marks
- Students can view results and download PDF marksheet
- Grade calculation (O, A+, A, B+, B, C, F)
- PDF marksheet generation

## Tech Stack
- **Frontend:** HTML, Bootstrap 5, Jinja2
- **Backend:** Python, Flask
- **Database:** Firebase Firestore
- **Authentication:** Firebase Auth
- **PDF:** ReportLab

## Setup
1. Clone the repository
2. Create virtual environment: python -m venv venv
3. Activate: venv\Scripts\Activate
4. Install packages: pip install -r requirements.txt
5. Add your serviceAccountKey.json
6. Run: python app.py

## Screenshots
- Admin Dashboard
- Faculty Upload Marks
- Student Results
- PDF Marksheet
