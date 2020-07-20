pipeline {
    environment {
        registry = "bitelds/demos"
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
        stage('Build') {
            agent any
            steps {
                script {
                    docker.build registry + ":$BUILD_NUMBER"
                }
            }
        }
    }
}