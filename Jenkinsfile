pipeline {
    environment {
        registryUrl = 'https://hub.docker.com/r/'
        registryCreds = "docker-hub-creds"
        registry = "bitelds/demos"
        image_tag = 'fancy_app_image'
        image_tag_full = "${registry}/${image_tag}"
        dockerImage = ''
        port = 8085
    }
    agent none
    stages {
        stage('Echo') {
            agent any
            steps {
                sh "echo ${env.BUILD_ID}"
                sh "echo ${env.BUILD_NUMBER}"
                sh "echo ${env.registryUrl}"
                sh "echo ${env.registry}"
                sh "echo ${env.image_tag}"
                sh "echo ${env.image_tag_full}"
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
                //sh "docker build --no-cache --rm -t ${env.image_tag} ."
                sh "docker images"
            }
        }
        /*
        stage('Lint code') {
            agent {
                //dockerfile true
                dockerfile {
                    //args "--no-cache --rm -t ${env.image_tag}"
                    additionalBuildArgs "--no-cache --rm -t ${env.image_tag}"
                    args "-i --rm -p ${env.port}:${env.port} --name ${env.image_tag}"
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
                    //sh "docker run -i -t --rm -p ${env.port}:${env.port} ${env.image_tag}"
                    //sh 'make test'
                    sh '''
                    DOCKER_RUN_OPTIONS="-i --rm"

                    # Only allocate tty if we detect one
                    if [ -t 0 ] && [ -t 1 ]; then
                        DOCKER_RUN_OPTIONS="$DOCKER_RUN_OPTIONS -t"
                    fi

                    docker run $DOCKER_RUN_OPTIONS --name ${env.image_tag} ${env.image_tag}
                    '''
                    sh "docker run $DOCKER_RUN_OPTIONS -p ${env.port}:${env.port} --name ${env.image_tag}"
                }

            }
        }
        stage('Build image') {
            agent any
            steps {
                script {
                    dockerImage = docker.build("${env.image_tag_full}:${env.BUILD_ID}")
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
                sh "docker build --no-cache --rm -t ${env.image_tag_full}:${env.BUILD_ID} -t ${env.image_tag_full}:latest ."
            }
        }
        stage('Run image and test') {
            agent any
            steps {
                sh "docker run -d --rm -p ${env.port}:${env.port} --name ${env.image_tag}"
                catchError {
                    sh 'make lint'
                    sh 'make test'
                }
            }
        }
        stage('Push image to Docker Hub') {
            agent any
            steps {
                /*
                script {
                    docker.withRegistry("${env.registryUrl}") {
                        dockerImage.push()
                    }
                }
                */
                sh "docker login --username bitelds -p ${env.registryCreds}"
                sh "docker push ${env.image_tag_full}:${env.BUILD_ID}"
                sh "docker push ${env.image_tag_full}:latest"
            }
        }
        /*
        stage('Remove unused docker image') {
            agent any
            steps{  //todo stop container
                sh "docker rmi ${env.image_tag_full}:${env.BUILD_ID}"
            }
        }*/
    }
    post {
        always {
            sh "docker stop ${env.image_tag}"
            sh "docker rmi ${env.image_tag_full}:${env.BUILD_ID}"
            sh "docker rmi ${env.image_tag_full}:latest"
            sh "docker system prune"
        }
    }
}