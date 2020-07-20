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
            agent any
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
        stage('Check images') {
            agent any
            steps {
                // build image for testing
                //sh "docker build --no-cache --rm -t ${env.image_name} ."
                sh "docker images"
            }
        }
        /*
        stage('Lint code') {
            agent {
                //dockerfile true
                dockerfile {
                    //args "--no-cache --rm -t ${env.image_name}"
                    additionalBuildArgs "--no-cache --rm -t ${env.image_name}"
                    args "-i --rm -p ${env.port}:${env.port} --name ${env.image_name}"
                }
            }
            steps {
                // check packages
                sh 'pip list'
                // run tests
                //sh 'make lint' --> error in Jenkins pipeline, which tries to create some file
                withEnv(['PYLINTHOME=.']) {
                    sh "pylint --exit-zero --disable=R,C,W1203 app.py"
                }
            }
        }
        */
        /*
        stage('Test code') {
            agent any
            steps {
                // allow for errors in this step
                catchError {
                    // run image for testing
                    //sh "docker run -i -t --rm -p ${env.port}:${env.port} ${env.image_name}"
                    //sh 'make test'
                    sh '''
                    DOCKER_RUN_OPTIONS="-i --rm"

                    # Only allocate tty if we detect one
                    if [ -t 0 ] && [ -t 1 ]; then
                        DOCKER_RUN_OPTIONS="$DOCKER_RUN_OPTIONS -t"
                    fi

                    docker run $DOCKER_RUN_OPTIONS --name ${env.image_name} ${env.image_name}
                    '''
                    sh "docker run $DOCKER_RUN_OPTIONS -p ${env.port}:${env.port} --name ${env.image_name}"
                }

            }
        }
        stage('Build image') {
            agent any
            steps {
                script {
                    dockerImage = docker.build("${env.image_name_full}:${env.BUILD_ID}")
                    //dockerImage = docker.build registry + "fancy_app_image:$BUILD_NUMBER"
                    dockerImage.inside {
                        withEnv(['PYLINTHOME=.']) {
                            sh "pylint --exit-zero --disable=R,C,W1203 app.py"
                        }
                        //sh 'make test' // not working
                    }
                }
            }
        }
        */
        stage('Build image') {
            agent any
            steps {
                sh "docker build --no-cache --rm -t ${env.image_name_full}:${env.BUILD_ID} -t ${env.image_name_full}:latest ."
            }
        }
        stage('Run image and test') {
            agent any
            steps {
                sh "docker run -d --rm -p ${env.port}:${env.port} --name ${env.image_name} ${env.image_name_full}:${env.BUILD_ID}"
                catchError {
                    withEnv(['PYLINTHOME=.']) {
                        sh "pylint --exit-zero --disable=R,C,W1203 app.py"
                    }
                    sh 'pytest'
                }
            }
        }
        stage('Push image to Docker Hub') {
            agent any
            steps {
                /*
                script {
                    docker.withRegistry("${env.registryUrl}", "${env.registryCreds}") {
                        dockerImage.push()
                        dockerImage.push("latest")
                    }
                }
                */
                sh "docker login --username bitelds -p ${env.registryCreds}"
                sh "docker push ${env.image_name_full}:${env.BUILD_ID}"
                sh "docker push ${env.image_name_full}:latest"
            }
        }
        /*
        stage('Remove unused docker image') {
            agent any
            steps{  //todo stop container
                sh "docker rmi ${env.image_name_full}:${env.BUILD_ID}"
            }
        }*/
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