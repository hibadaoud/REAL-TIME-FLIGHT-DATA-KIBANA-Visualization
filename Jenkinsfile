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
                cache(caches: [
                    [$class: 'ArbitraryFileCache',
                     path: '.',
                     includes: '**/*',
                     compressionMethod: 'TAR']
                ]) {
                    checkout scm
                }
            }
        }
        stage('Lint') {
            agent {
                dockerfile {
                    filename 'Dockerfile'
                    dir 'lint'
                    reuseNode true
                    // customWorkspace '/home/jenkins/workspace/frontend'
                }
            }
            parallel {
                stage('ESLint') {
                    steps {
                        script {
                            // Running ESLint and storing the output in a file
                            sh '''
                            mkdir -p lint-results
                            eslint backend/**/*.js > lint-results/eslint.txt || true
                            '''
                            // Archiving the ESLint results
                            archiveArtifacts artifacts: 'lint-results/eslint.txt', allowEmptyArchive: true
                            // sh 'cp lint-results/*.txt /path/to/container/artifacts/'

                        }
                    }
                }

                stage('HTMLHint') {
                    steps {
                        script {
                            // Running HTMLHint and storing the output in a file
                            sh '''
                            mkdir -p lint-results
                            htmlhint frontend/**/*.html > lint-results/htmlhint.txt || true
                            '''
                            // Archiving the HTMLHint results
                            archiveArtifacts artifacts: 'lint-results/htmlhint.txt', allowEmptyArchive: true
                        }
                    }
                }

                stage('Flake8') {
                    steps {
                        script {
                            // Running Flake8 and storing the output in a file
                            sh '''
                            mkdir -p lint-results
                            flake8 spark/*.py > lint-results/flake8.txt || true
                            '''
                            // Archiving the Flake8 results
                            archiveArtifacts artifacts: 'lint-results/flake8.txt', allowEmptyArchive: true
                        }
                    }
                }

                stage('Hadolint') {
                    steps {
                        script {
                            // Running Hadolint on the Dockerfile and storing the output in a file
                            sh '''
                            mkdir -p lint-results
                            hadolint backend/Dockerfile > lint-results/hadolint.txt || true
                            '''
                            // Archiving the Hadolint results
                            archiveArtifacts artifacts: 'lint-results/hadolint.txt', allowEmptyArchive: true
                        }
                    }
                }
            }
        }

        // stage('Build Docker Image') {
        //     steps {
        //         // Building the Docker image using the specified Dockerfile
        //         sh 'docker build -t ${IMAGE_TAG} -f frontend/Dockerfile .'
        //         echo "Docker image built successfully"
        //         // Listing the Docker images to verify
        //         sh "docker images"
        //     }
        // }
    }        
}
