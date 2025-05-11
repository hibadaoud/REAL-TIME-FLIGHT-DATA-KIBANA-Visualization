pipeline {
    agent any
    // environment {
    //     IMAGE_NAME = 'hiba25/jenkins-flight-plateform'
    //     IMAGE_TAG = "${IMAGE_NAME}:${env.BUILD_NUMBER}"

    // }
    options {
        skipDefaultCheckout()
    }
    stages {
        stage('Checkout') {
            steps {
                cache(workspace: true, paths: ['.']) {
                    checkout scm
                }
            }
        stage('Lint') {
            agent {
                dockerfile {
                    filename 'lint/Dockerfile' // This is your custom Dockerfile
                }
            }
            parallel {
                stage('ESLint') {
                steps {
                    sh '''
                    mkdir -p lint-results
                    eslint backend/**/*.js > lint-results/eslint.txt || true
                    '''
                    archiveArtifacts artifacts: 'lint-results/eslint.txt', allowEmptyArchive: true
                }
                }

                stage('HTMLHint') {
                steps {
                    sh '''
                    mkdir -p lint-results
                    htmlhint frontend/**/*.html > lint-results/htmlhint.txt || true
                    '''
                    archiveArtifacts artifacts: 'lint-results/htmlhint.txt', allowEmptyArchive: true
                }
                }

                stage('Flake8') {
                steps {
                    sh '''
                    mkdir -p lint-results
                    flake8 spark/ > lint-results/flake8.txt || true
                    '''
                    archiveArtifacts artifacts: 'lint-results/flake8.txt', allowEmptyArchive: true
                }
                }

                stage('Hadolint') {
                steps {
                    sh '''
                    mkdir -p lint-results
                    hadolint backend/Dockerfile > lint-results/hadolint.txt || true
                    '''
                    archiveArtifacts artifacts: 'lint-results/hadolint.txt', allowEmptyArchive: true
                }
                }
            }
        }
    }

         
        // stage('Build Docker Image')
        // {
        //     steps
        //     {   
        //         sh 'docker build -t ${IMAGE_TAG} -f frontend/Dockerfile .'
        //         echo "Docker image build successfullyyy"
        //         sh "docker images"
        //     }
        // }
        
    }
}