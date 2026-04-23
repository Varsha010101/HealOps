pipeline {
    agent any

    environment {
        IMAGE_NAME = "auto-heal-app"
        CONTAINER_NAME = "auto-heal-container"
    }

    stages {

        stage('Build Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Clean Old Containers') {
            steps {
                sh '''
                docker rm -f $CONTAINER_NAME || true
                docker ps -q --filter "publish=5000" | xargs -r docker rm -f || true
                '''
            }
        }

        stage('Run Container (Auto-Heal)') {
            steps {
                sh '''
                docker run -d -p 5000:5000 \
                --name $CONTAINER_NAME \
                --restart always \
                $IMAGE_NAME
                '''
            }
        }
    }
}
