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
            parallel {
                stage('ESLint') {
                    agent {
                        dockerfile {
                            filename 'lint/Dockerfile.ESlint'
                            buildContext '.'
                            reuseNode true
                            // customWorkspace '/home/jenkins/workspace/frontend'
                        }
                    }
                    steps {
                        script {
                            // Running ESLint and storing the output in a file
                            sh '''
                            mkdir -p $WORKSPACE/lint-results
                            eslint ./**/*.js > $WORKSPACE/lint-results/eslint.txt || true
                            eslint styles.css > $WORKSPACE/lint-results/eslint-css.txt || true

                            '''
                            // Archiving the ESLint results
                            archiveArtifacts artifacts: 'lint-results/eslint.txt', allowEmptyArchive: true
                            archiveArtifacts artifacts: 'lint-results/eslint-css.txt', allowEmptyArchive: true
                            // sh 'cp lint-results/*.txt /path/to/container/artifacts/'

                        }
                    }
                }

                stage('HTMLHint') {
                    agent {
                        dockerfile {
                            filename 'lint/Dockerfile.htmllint'
                            buildContext '.'
                            reuseNode true
                            // customWorkspace '/home/jenkins/workspace/frontend'
                        }
                    }
                    steps {
                        script {
                            // Running ESLint and storing the output in a file
                            sh '''
                            mkdir -p $WORKSPACE/lint-results
                            htmlhint ./**/*.html > $WORKSPACE/lint-results/htmllint.txt || true
                            '''
                            // Archiving the ESLint results
                            archiveArtifacts artifacts: 'lint-results/htmllint.txt', allowEmptyArchive: true
                            // sh 'cp lint-results/*.txt /path/to/container/artifacts/'

                        }
                    }
                }

                stage('Flake8') {
                    agent {
                        dockerfile {
                            filename 'lint/Dockerfile.flakelint'
                            buildContext '.'
                            reuseNode true
                            // customWorkspace '/home/jenkins/workspace/frontend'
                        }
                    }
                    steps {
                        script {
                            // Running ESLint and storing the output in a file
                            sh '''
                            mkdir -p $WORKSPACE/lint-results
                            flake8 ./**/*.py > $WORKSPACE/lint-results/flakelint.txt || true
                            '''
                            // Archiving the ESLint results
                            archiveArtifacts artifacts: 'lint-results/flakelint.txt', allowEmptyArchive: true
                            // sh 'cp lint-results/*.txt /path/to/container/artifacts/'

                        }
                    }
                }

                stage('Hadolint') {
                    agent {
                        dockerfile {
                            filename 'lint/Dockerfile.hadolint'
                            buildContext '.'
                            reuseNode true
                            // customWorkspace '/home/jenkins/workspace/frontend'
                        }
                    }
                    steps {
                        script {
                            // Running ESLint and storing the output in a file
                            sh '''
                            mkdir -p $WORKSPACE/lint-results
                            hadolint ./frontend/Dockerfile > $WORKSPACE/lint-results/hadolint.txt || true
                            ''' 
                            // Archiving the ESLint results
                            archiveArtifacts artifacts: 'lint-results/hadolint.txt', allowEmptyArchive: true
                            // sh 'cp lint-results/*.txt /path/to/container/artifacts/'

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
