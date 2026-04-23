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

        stage('Clean Old Containers (Free Port 5000)') {
            steps {
                sh '''
                # Stop & remove our app container (if exists)
                docker stop $CONTAINER_NAME || true
                docker rm $CONTAINER_NAME || true

                # Also kill ANY container using port 5000 (safety)
                docker ps -q --filter "publish=5000" | xargs -r docker rm -f || true
                '''
            }
        }

        stage('Run Container with STRONG Auto-Heal') {
            steps {
                sh '''
                docker run -d -p 5000:5000 \
                --name $CONTAINER_NAME \
                --restart always \
                $IMAGE_NAME
                '''
            }
        }

        stage('Verify Restart Policy') {
            steps {
                sh '''
                echo "=== Restart Policy ==="
                docker inspect $CONTAINER_NAME | grep -A 3 RestartPolicy || true
                '''
            }
        }
    }
}
