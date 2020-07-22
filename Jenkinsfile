pipeline {
    environment {
        registryUrl = "https://registry-1.docker.io/v2/"
        registryCreds = credentials("docker-hub-creds")
        registry = "bitelds"
        image_name = 'fancy_app_image'
        image_name_full = "${registry}/${image_name}"
        dockerImage = ''
        port = 8085
    }
    agent any
    stages {
        stage('Echo') {
            steps {
                sh "echo ${env.BUILD_ID}"
                sh "echo ${env.BUILD_NUMBER}"
                sh "echo ${env.registryUrl}"
                sh "echo ${env.registryCreds}"
                sh "echo ${env.registry}"
                sh "echo ${env.image_name}"
                sh "echo ${env.image_name_full}"
                sh "echo ${env.port}"
            }
        }
        stage('Lint HTML') {
            steps {
                sh 'tidy -q -e templates/*.html'
            }
        }
        stage('Lint Dockerfile') {
            steps {
                sh 'hadolint Dockerfile'
            }
        }
        stage('Check images') {
            steps {
                sh "docker images"
            }
        }
        stage('Build image') {
            steps {
                sh "docker build --no-cache --rm -t ${env.image_name_full}:${env.BUILD_ID} -t ${env.image_name_full}:latest ."
            }
        }
        stage('Run image and test') {
            steps {
                sh "docker run -d --rm -p ${env.port}:${env.port} --name ${env.image_name} ${env.image_name_full}:${env.BUILD_ID} sh -c 'pylint --disable=R,C,W1203 app.py; echo $?'"
            }
        }
        stage('Push image to Docker Hub') {
            steps {
                sh "docker login --username bitelds -p ${env.registryCreds}"
                sh "docker push ${env.image_name_full}:${env.BUILD_ID}"
                sh "docker push ${env.image_name_full}:latest"
            }
        }
        stage('Deploy the app') {
            steps {
                sh "kubectl apply -f './infrastructure/deployment.yaml'"
            }
        }
    }
    post {
        always {
            sh "docker stop ${env.image_name}"
            sh "docker rmi ${env.image_name_full}:${env.BUILD_ID}"
            sh "docker rmi ${env.image_name_full}:latest"
            sh "docker system prune -f"
        }
    }
}