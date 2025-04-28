pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'heart-disease-app'
        DOCKER_HUB_CREDENTIALS = credentials('docker-hub')
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
                    // For Windows, ensure Docker is in Windows container mode if needed
                    def customImage = docker.build("${DOCKER_IMAGE}:${env.BUILD_ID}")
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                script {
                    // Authenticate with Docker Hub
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub') {
                        // Tag and push the image
                        def customImage = docker.image("${DOCKER_IMAGE}:${env.BUILD_ID}")
                        customImage.push()
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // For Windows, use bat instead of sh for command execution
                    bat 'docker run ${DOCKER_IMAGE}:${env.BUILD_ID} python -m pytest tests/'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Windows-compatible container management
                    bat '''
                    docker stop heart-app || echo "No container to stop"
                    docker rm heart-app || echo "No container to remove"
                    docker run -d -p 5000:5000 --name heart-app ${DOCKER_IMAGE}:${env.BUILD_ID}
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            script {
                // Windows-compatible cleanup
                bat 'docker system prune -f'
            }
        }
    }
}