pipeline {
    agent any
    environment {
        IMAGE_NAME = 'hiba25/jenkins-flight-app'
        IMAGE_TAG = "${IMAGE_NAME}:${env.BUILD_NUMBER}"

    }
    stages {

        stage('Build Docker Image')
        {
            steps
            {   
                sh 'cd frontend'
                sh 'docker build -t ${IMAGE_TAG} .'
                echo "Docker image build successfully"
                sh "docker images"
            }
        }
       
    }
}