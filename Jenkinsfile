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
                    // Use proper Docker Hub authentication with credentials binding
                    withCredentials([usernamePassword(
                        credentialsId: 'docker-hub',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        // Use --password-stdin for secure login
                        bat """
                            echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
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
                        // Tag and push the image
                        bat """
                            docker tag ${DOCKER_IMAGE}:${env.BUILD_ID} %DOCKER_USER%/${DOCKER_IMAGE}:${env.BUILD_ID}
                            docker push %DOCKER_USER%/${DOCKER_IMAGE}:${env.BUILD_ID}
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

        stage('Deploy') {
            steps {
                script {
                    bat """
                        docker stop heart-app || echo No container to stop
                        docker rm heart-app || echo No container to remove
                        docker run -d -p 5000:5000 --name heart-app ${DOCKER_IMAGE}:${env.BUILD_ID}
                    """
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