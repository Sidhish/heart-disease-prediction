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
                script {
                    withCredentials([usernamePassword(
                        credentialsId: 'docker-hub',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        // Write password to file then use it for security
                        bat """
                            echo %DOCKER_PASS% > docker_password.txt
                            type docker_password.txt | docker login -u %DOCKER_USER% --password-stdin
                            del docker_password.txt
                        """
                    }
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: 'docker-hub',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        bat """
                            docker tag ${DOCKER_IMAGE}:${env.BUILD_ID} %DOCKER_USER%/${DOCKER_IMAGE}:latest
                            docker push %DOCKER_USER%/${DOCKER_IMAGE}:latest
                        """
                    }
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
    }

    post {
        always {
            echo 'Cleaning up...'
            script {
                bat 'docker system prune -f'
            }
        }
    }
}