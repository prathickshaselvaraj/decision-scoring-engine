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

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('My Sonar Server') {
                    sh '''
                        sonar-scanner \
                        -Dsonar.projectKey=decision-scoring-engine \
                        -Dsonar.sources=src \
                        -Dsonar.language=py \
                        -Dsonar.python.version=3 \
                        -Dsonar.host.url=http://localhost:9000 \
                        -Dsonar.token=sqp_7c5365d783b836a3716764843ab2d7a1d17f4269
                    '''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                echo 'Checking Quality Gate...'
                waitForQualityGate abortPipeline: true
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying to production...'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully! Deployed!'
        }
        failure {
            echo 'Quality Gate FAILED! Build stopped. No deployment!'
        }
    }
}
