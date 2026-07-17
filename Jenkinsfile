pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        skipDefaultCheckout(true)
    }

    parameters {
        string(
            name: 'DOCKERHUB_IMAGE',
            defaultValue: 'richards7/dockflex',
            description: 'Docker Hub repository, formatted as namespace/image.'
        )
        booleanParam(
            name: 'PUSH_TO_DOCKERHUB',
            defaultValue: true,
            description: 'Push verified main/master builds to Docker Hub.'
        )
    }

    environment {
        CANDIDATE_IMAGE = "dockflex-ci:${BUILD_NUMBER}"
        TEST_CONTAINER = "dockflex-ci-${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Validate configuration') {
            steps {
                sh 'docker compose config -q'
            }
        }

        stage('Build candidate image') {
            steps {
                sh 'docker build --pull --tag "$CANDIDATE_IMAGE" .'
            }
        }

        stage('Test candidate image') {
            steps {
                sh '''#!/bin/sh
                    set -eu
                    docker run --name "$TEST_CONTAINER" "$CANDIDATE_IMAGE" \
                      python -m unittest discover -s tests -v
                '''
            }
        }

        stage('Push verified image to Docker Hub') {
            when {
                expression {
                    return params.PUSH_TO_DOCKERHUB &&
                        (!env.BRANCH_NAME || env.BRANCH_NAME == 'main' || env.BRANCH_NAME == 'master')
                }
            }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKERHUB_USERNAME',
                    passwordVariable: 'DOCKERHUB_TOKEN'
                )]) {
                    sh '''#!/bin/sh
                        set -eu
                        echo "$DOCKERHUB_TOKEN" | docker login --username "$DOCKERHUB_USERNAME" --password-stdin
                        docker tag "$CANDIDATE_IMAGE" "$DOCKERHUB_IMAGE:${BUILD_NUMBER}"
                        docker tag "$CANDIDATE_IMAGE" "$DOCKERHUB_IMAGE:latest"
                        docker push "$DOCKERHUB_IMAGE:${BUILD_NUMBER}"
                        docker push "$DOCKERHUB_IMAGE:latest"
                        docker logout
                    '''
                }
            }
        }
    }

    post {
        always {
            sh '''#!/bin/sh
                docker rm -f "$TEST_CONTAINER" >/dev/null 2>&1 || true
                docker image rm "$CANDIDATE_IMAGE" >/dev/null 2>&1 || true
            '''
        }
    }
}
