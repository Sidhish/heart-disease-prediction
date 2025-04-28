pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'heart-disease-app'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                url: 'https://github.com/your-repo/heart-disease-prediction.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${env.BUILD_ID}")
                }
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker run ${DOCKER_IMAGE}:${env.BUILD_ID} python -m pytest tests/'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                docker stop heart-app || true
                docker rm heart-app || true
                docker run -d -p 5000:5000 --name heart-app ${DOCKER_IMAGE}:${env.BUILD_ID}
                '''
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            docker.systemPrune()
        }
    }
}