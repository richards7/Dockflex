pipeline {
    agent {
        label 'docker-agent'
    }

    options {
        timestamps()
        disableConcurrentBuilds()
        skipDefaultCheckout(true)
    }

    environment {
        AWS_REGION = 'us-east-1'
        AWS_ACCOUNT_ID = '054043816989'
        ECR_REPOSITORY = 'dockflex'

        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

        IMAGE_NAME = "${ECR_REGISTRY}/${ECR_REPOSITORY}"

        CANDIDATE_IMAGE = "dockflex-ci:${BUILD_NUMBER}"
        TEST_CONTAINER = "dockflex-test-${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Validate Docker Compose') {
            steps {
                sh 'docker compose config -q'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                      --pull \
                      -t ${CANDIDATE_IMAGE} .
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                    docker run --rm \
                      --name ${TEST_CONTAINER} \
                      ${CANDIDATE_IMAGE} \
                      python -m unittest discover -s tests -v
                '''
            }
        }

        stage('Authenticate to AWS ECR') {

            steps {

                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-credentials'
                ]]) {

                    sh '''
                        aws ecr get-login-password \
                        --region ${AWS_REGION} | docker login \
                        --username AWS \
                        --password-stdin ${ECR_REGISTRY}
                    '''
                }
            }
        }

        stage('Push Image to ECR') {

            steps {

                sh '''

                    docker tag ${CANDIDATE_IMAGE} ${IMAGE_NAME}:${BUILD_NUMBER}

                    docker tag ${CANDIDATE_IMAGE} ${IMAGE_NAME}:latest

                    docker push ${IMAGE_NAME}:${BUILD_NUMBER}

                    docker push ${IMAGE_NAME}:latest

                '''
            }

        }

    }

    post {

        always {

            sh '''

                docker rm -f ${TEST_CONTAINER} >/dev/null 2>&1 || true

                docker image rm ${CANDIDATE_IMAGE} >/dev/null 2>&1 || true

            '''

        }

    }

}