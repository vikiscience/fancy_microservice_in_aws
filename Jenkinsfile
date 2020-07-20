pipeline {
    environment {
        registry = "bitelds/demos"
        dockerImage = ''
        port = 8085
        image_tag = 'fancy_app_image'
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
        stage('Lint code') {
            agent {
                dockerfile true
            }
            steps {
                // check packages
                sh 'pip list'
                // run tests
                sh 'make lint'
            }
        }
        stage('Build') {
            agent any
            steps {
                // build image for testing
                sh "docker build --no-cache --rm -t ${env.image_tag} ."
                sh "docker images"
            }
        }
        stage('Test code') {
            agent any
            steps {
                // run image for testing
                sh "docker run -i -t --rm -p ${env.port}:${env.port} ${env.image_tag}"
                //sh 'make test'
            }
        }
        stage('Build image') {
            agent any
            steps {
                script {
                    dockerImage = docker.build("${env.registry}/${env.image_tag}:${env.BUILD_ID}")
                    //dockerImage = docker.build registry + "fancy_app_image:$BUILD_NUMBER"
                    dockerImage.inside {
                        sh 'make test'
                    }
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
                sh "docker rmi ${env.registry}/${env.image_tag}:${env.BUILD_ID}"
            }
        }
    }
}