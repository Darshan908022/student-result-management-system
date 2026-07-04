pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Successfully pulled code from GitHub!'
            }
        }
        stage('Install Dependencies') {
            steps {
                echo 'Installing project requirements...'
                // If you have a requirements.txt, this installs it locally
                bat 'pip install -r requirements.txt --user --upgrade'
            }
        }
        stage('Lint / Sanity Check') {
            steps {
                echo 'Checking syntax errors...'
                // Compiles the script to check for syntax bugs without running it
                bat 'python -m py_compile app.py'
            }
        }
    }
}
