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

        stage('Build Image') {
            steps {
                sh 'docker build --no-cache -t $IMAGE_NAME .'
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                echo "Stopping old container (if exists)..."
                docker stop $CONTAINER_NAME || true

                echo "Removing old container (if exists)..."
                docker rm $CONTAINER_NAME || true

                echo "Running new container..."
                docker run -d -p $PORT:5000 \

                --name $CONTAINER_NAME \
                --restart always \
                $IMAGE_NAME
                '''
            }
        }


        stage('Verify') {
            steps {
                sh 'docker ps'
            }
        }
    }
}

