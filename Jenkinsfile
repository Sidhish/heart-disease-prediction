pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'heart-disease-app'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Sidhish/heart-disease-prediction.git',
                    credentialsId: 'github-token'
            }
        }

        stage('Verify Docker') {
            steps {
                script {
                    bat 'docker --version'
                    bat 'docker info'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    bat "docker build -t ${DOCKER_IMAGE}:${env.BUILD_ID} ."
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat """
                        echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                    """
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    bat """
                        docker tag ${DOCKER_IMAGE}:${env.BUILD_ID} %DOCKER_USER%/${DOCKER_IMAGE}:latest
                        docker push %DOCKER_USER%/${DOCKER_IMAGE}:latest
                    """
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    bat "docker run --rm ${DOCKER_IMAGE}:${env.BUILD_ID} python -m pytest tests/"
                }
            }
        }

        stage('Deploy Container') {
            steps {
                script {
                    bat """
                        docker stop heart-disease-container || exit 0
                        docker rm heart-disease-container || exit 0
                        docker run -d --name heart-disease-container -p 5000:5000 %DOCKER_USER%/${DOCKER_IMAGE}:latest
                    """
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up unused Docker resources...'
            script {
                bat 'docker system prune -f'
            }
        }
    }
}
