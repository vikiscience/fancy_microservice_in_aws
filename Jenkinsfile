pipeline {
    environment {
        registry = "bitelds/demos"
        dockerImage = ''
    }
    agent none
    stages {
        stage('Lint HTML') {
            agent any
            steps {
                sh 'tidy -q -e templates/*.html'
            }
        }
        stage('Lint Dockerfile') {
            agent any
            steps {
                sh 'hadolint Dockerfile'
            }
        }
        stage('Test code') {
            agent {
                dockerfile true
            }
            steps {
                // check packages
                sh 'pip list'
                // run tests
                sh 'make lint'
                sh 'make test'
            }
        }
        stage('Build image') {
            agent any
            steps {
                script {
                    dockerImage = docker.build("${env.registry}/fancy_app_image:${env.BUILD_ID}")
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