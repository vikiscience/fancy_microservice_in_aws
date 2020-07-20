pipeline {
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
            agent all
            steps {
                sh 'tidy -q -e templates/*.html'
            }
        }
        stage('Build') {
            agent {
                node {

                    checkout scm
                    docker.withRegistry('https://hub.docker.com/r/bitelds/demos') {
                        def customImage = docker.build("fancy_app_image:${env.BUILD_ID}", "--no-cache --rm")
                        customImage.push()
                    }

                }
            }
            steps {
                sh 'echo "Hello World"'
            }
        }
    }
}