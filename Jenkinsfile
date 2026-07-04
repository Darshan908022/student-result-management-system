pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Successfully pulled code from GitHub!'
            }
        }
        stage('Build') {
            steps {
                echo 'Building application...'
                // Example: sh 'mvn clean package' or sh 'npm run build'
            }
        }
        stage('Test') {
            steps {
                echo 'Running tests...'
                // Example: sh 'mvn test' or sh 'npm test'
            }
        }
    }
}
