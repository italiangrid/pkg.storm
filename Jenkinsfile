pipeline {
  agent { label 'docker' }

  options {
    timeout(time: 1, unit: 'HOURS')
    buildDiscarder(logRotator(numToKeepStr: '5'))
  }

  triggers { cron('@daily') }

  parameters {
    string(name: 'PLATFORM', defaultValue: 'centos6', description: 'OS Platform')
  }

  stages{
    stage('package') {
      environment {
        DATA_CONTAINER_NAME = "stage-area-pkg.storm-${env.JOB_BASE_NAME}-${env.BUILD_NUMBER}"
        PLATFORM = "${params.PLATFORM}"
      }
      steps {
        cleanWs notFailBuild: true
        checkout scm
        sh 'docker create -v /stage-area --name ${DATA_CONTAINER_NAME} italiangrid/pkg.base:centos6'
        sh '''
        pushd rpm
        ls -al
        sh build.sh
        popd
        '''
        sh 'docker cp ${DATA_CONTAINER_NAME}:/stage-area rpms'

        script {
          def repoStr = """[storm-test-${params.PLATFORM}]
name=storm-test-${params.PLATFORM}
baseurl=${env.JOB_URL}/lastSuccessfulBuild/artifact/rpms/${params.PLATFORM}/
protect=1
enabled=1
priority=1
gpgcheck=0
"""
          writeFile file: "rpms/storm-test-${params.PLATFORM}.repo", text: "${repoStr}"
        }

        sh 'docker cp ${DATA_CONTAINER_NAME}:/stage-area-source srpms'

        script {
          def sourceRepoStr = """[storm-test-source-${params.PLATFORM}]
name=storm-test-source-${params.PLATFORM}
baseurl=${env.JOB_URL}/lastSuccessfulBuild/artifact/srpms/${params.PLATFORM}/
protect=1
enabled=1
priority=1
gpgcheck=0
"""
          writeFile file: "srpms/storm-test-source-${params.PLATFORM}.repo", text: "${sourceRepoStr}"
        }

        sh 'docker rm -f ${DATA_CONTAINER_NAME}'

        archiveArtifacts 'rpms/**, srpms/**'
      }
    }
  }

  post {
    failure {
      slackSend color: 'danger', message: "${env.JOB_NAME} - #${env.BUILD_ID} Failure (<${env.BUILD_URL}|Open>)"
    }
    changed {
      script{
        if('SUCCESS'.equals(currentBuild.result)) {
          slackSend color: 'good', message: "${env.JOB_NAME} - #${env.BUILD_ID} Back to normal (<${env.BUILD_URL}|Open>)"
        }
      }
    }
  }
}
