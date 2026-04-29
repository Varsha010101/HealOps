pipeline {
    agent any

    environment {
        IMAGE_NAME = "auto-heal-app"
        CONTAINER_NAME = "auto-heal-container"
        PORT = "5055"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test Docker') {
            steps {
                sh 'docker ps'
            }
        }

        stage('Build Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Clean Old Container') {
            steps {
                sh 'docker rm -f $CONTAINER_NAME || true'
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker run -d -p $PORT:5000 \
                --name $CONTAINER_NAME \
                --restart always \
                $IMAGE_NAME
                '''
            }
        }
    }
}