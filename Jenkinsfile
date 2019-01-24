def dataContainerName = "stage-area-${env.JOB_BASE_NAME}-${env.BUILD_NUMBER}"
def podLabel = "pkg-storm-${env.JOB_BASE_NAME}-${env.BUILD_NUMBER}"

pipeline {
    agent {
        kubernetes {
            label "${podLabel}"
            cloud 'Kube mwdevel'
            defaultContainer 'jnlp'
            yamlFile 'jenkins/pod.yaml'
        }
    }

    options {
        timeout(time: 1, unit: 'HOURS')
        buildDiscarder(logRotator(numToKeepStr: '5'))
    }

    triggers { cron('@daily') }

    parameters {
        string(name: 'INCLUDE_BUILD_NUMBER', defaultValue: '1', description: 'OS Platform')
    }

    environment {
        DATA_CONTAINER_NAME = "${dataContainerName}"
        PLATFORM = "centos7"
        INCLUDE_BUILD_NUMBER = "${params.INCLUDE_BUILD_NUMBER}"
    }

    stages {
        stage('Run') {
            steps {
                container('kube-docker-runner') {
                    sh 'env | grep DATA_CONTAINER_NAME'
                    sh 'env | grep PLATFORM'

                    script {
                        cleanWs notFailBuild: true
                        checkout scm
                        sh "docker create -v /stage-area --name ${DATA_CONTAINER_NAME} italiangrid/pkg.base:${PLATFORM}"
                        sh '''
                        pushd rpm
                        ls -al
                        sh build.sh
                        popd
                        '''
                        sh "docker cp ${DATA_CONTAINER_NAME}:/stage-area rpms"

                        script {
                            def repoStr = """[storm-test-${PLATFORM}]
name=storm-test-${PLATFORM}
baseurl=${env.JOB_URL}/lastSuccessfulBuild/artifact/rpms/${PLATFORM}/
protect=1
enabled=1
priority=1
gpgcheck=0
"""
                            writeFile file: "rpms/storm-test-${PLATFORM}.repo", text: "${repoStr}"
                        }

                        sh "docker cp ${DATA_CONTAINER_NAME}:/stage-area-source srpms"

                        def sourceRepoStr = """[storm-test-source-${PLATFORM}]
name=storm-test-source-${PLATFORM}
baseurl=${env.JOB_URL}/lastSuccessfulBuild/artifact/srpms/${PLATFORM}/
protect=1
enabled=1
priority=1
gpgcheck=0
"""
                        writeFile file: "srpms/storm-test-source-${PLATFORM}.repo", text: "${sourceRepoStr}"

                        sh "docker rm -f ${DATA_CONTAINER_NAME}"
                    }

                    archiveArtifacts 'rpms/**, srpms/**'
                }
            }
        }
    }
    post {
        failure {
            slackSend color: 'danger', message: "${env.JOB_NAME} - #${env.BUILD_ID} Failure (<${env.BUILD_URL}|Open>)"
        }
        changed {
            script {
                if('SUCCESS'.equals(currentBuild.result)) {
                    slackSend color: 'good', message: "${env.JOB_NAME} - #${env.BUILD_ID} Back to normal (<${env.BUILD_URL}|Open>)"
                }
            }
        }
    }
}
