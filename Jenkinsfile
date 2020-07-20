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
                sh 'pip list'
                sh 'make lint'
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
                    dockerImage = docker.build registry + "fancy_app_image:$BUILD_NUMBER"
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