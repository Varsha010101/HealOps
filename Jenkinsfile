pipeline {
    agent any

    environment {
        IMAGE_NAME = "auto-heal-app"
        CONTAINER_NAME = "auto-heal-container"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Remove Old Container') {
            steps {
                sh 'docker rm -f $CONTAINER_NAME || true'
            }
        }

        stage('Remove Old Image') {
            steps {
                sh 'docker rmi -f $IMAGE_NAME || true'
            }
        }

        stage('Build Image') {
            steps {
                sh 'docker build --no-cache -t $IMAGE_NAME .'
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker run -d -p 5055:5000 \
                --name $CONTAINER_NAME \
                --restart always \
                $IMAGE_NAME
                '''
            }
        }
    }
}