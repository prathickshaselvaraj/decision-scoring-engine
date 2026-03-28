pipeline {
    agent any

    stages {
        stage('SCM') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Setting up Python virtual environment...'
                sh 'python3 -m venv venv'
                sh 'venv/bin/pip install --upgrade pip'
                sh 'venv/bin/pip install -r requirements.txt'
                echo 'Build complete.'
            }
        }

        stage('Test') {
            steps {
                echo 'Running unit tests...'
                sh 'venv/bin/pip install pytest'
                sh 'venv/bin/pytest --junitxml=report.xml'
            }
            post {
                always {
                    junit 'report.xml'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check test results.'
        }
    }
}
