pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'heart-disease-app'
        DOCKER_HUB_CREDENTIALS = credentials('docker-hub') // Make sure this credential exists in Jenkins
    }

    stages {
        stage('Checkout') {
            steps {
                // Use the correct GitHub URL and your credentials ID
                git branch: 'main', 
                url: 'https://github.com/Sidhish/heart-disease-prediction.git',
                credentialsId: 'github-token' // Make sure this credential exists in Jenkins
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build with Windows-compatible commands
                    bat "docker build -t ${DOCKER_IMAGE}:${env.BUILD_ID} ."
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                script {
                    // Login to Docker Hub
                    withCredentials([usernamePassword(
                        credentialsId: 'docker-hub',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        bat "docker login -u %DOCKER_USER% -p %DOCKER_PASS%"
                    }
                    
                    // Tag and push the image
                    bat "docker tag ${DOCKER_IMAGE}:${env.BUILD_ID} %DOCKER_USER%/${DOCKER_IMAGE}:${env.BUILD_ID}"
                    bat "docker push %DOCKER_USER%/${DOCKER_IMAGE}:${env.BUILD_ID}"
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Run tests in the container
                    bat "docker run --rm ${DOCKER_IMAGE}:${env.BUILD_ID} python -m pytest tests/"
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Stop and remove existing container if it exists
                    bat "docker stop heart-app || echo No container to stop"
                    bat "docker rm heart-app || echo No container to remove"
                    
                    // Run new container
                    bat "docker run -d -p 5000:5000 --name heart-app ${DOCKER_IMAGE}:${env.BUILD_ID}"
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            script {
                // Clean up Docker system
                bat 'docker system prune -f'
            }
        }
    }
}