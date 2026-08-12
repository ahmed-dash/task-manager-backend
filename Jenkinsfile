pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh '''
                docker run --rm -v $WORKSPACE:/app -w /app python:3.12-slim \
                  bash -c "pip install --quiet -r requirements-dev.txt --break-system-packages && pytest -q"
                '''
            }
        }
        stage('Deploy') {
            steps {
                sh 'cd /opt/task-manager && docker compose -f docker-compose.prod.yml up -d --build backend'
            }
        }
    }
}