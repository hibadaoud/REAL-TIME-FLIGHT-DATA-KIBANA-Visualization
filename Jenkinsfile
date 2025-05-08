pipeline {
    agent any
    environment {
        IMAGE_NAME = 'hiba25/jenkins-flight-plateform'
        IMAGE_TAG = "${IMAGE_NAME}:${env.BUILD_NUMBER}"

    }
    stages {
         stage('Debug Path') {
            steps {
                sh 'pwd'
                sh 'ls -la'
            }
        }
        stage('Build Docker Image')
        {
            steps
            {   
                sh 'docker build -t ${IMAGE_TAG} -f frontend/Dockerfile .'
                echo "Docker image build successfullyyy"
                sh "docker images"
            }
        }
       
    }
}