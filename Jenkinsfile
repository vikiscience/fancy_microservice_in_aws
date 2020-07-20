pipeline {
    environment {
        registry = "bitelds/demos"
        dockerImage = ''
    }
    agent none
    stages {
        stage('Lint SRC') {
            agent {
                dockerfile true
            }
            steps {
                // check packages
                sh 'pip list'
                // Install hadolint
                sh "wget -O /bin/hadolint https://github.com/hadolint/hadolint/releases/download/v1.16.3/hadolint-Linux-x86_64"
                sh "chmod +x /bin/hadolint"
                // run tests
                sh 'make lint'
                sh 'make test'
            }
        }
        stage('Lint HTML') {
            agent any
            steps {
                sh 'tidy -q -e templates/*.html'
            }
        }
        stage('Build image') {
            agent any
            steps {
                script {
                    dockerImage = docker.build("$(env.registry)/fancy_app_image:${env.BUILD_ID}")
                    //dockerImage = docker.build registry + "fancy_app_image:$BUILD_NUMBER"
                }
            }
        }
        stage('Deploy image to Docker Hub') {
            agent any
            steps {
                script {
                    docker.withRegistry('') {
                        dockerImage.push()
                    }
                }
            }
        }
        stage('Remove unused docker image') {
            steps{
                sh "docker rmi $registry/fancy_app_image:$BUILD_NUMBER"
            }
        }
    }
}