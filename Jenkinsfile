pipeline {

  agent {
    label 'deployment-test'
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
    PLATFORM = "centos7"
    INCLUDE_BUILD_NUMBER = "${params.INCLUDE_BUILD_NUMBER}"
  }

  stages {
    stage('Run') {
      steps {
        script {
          cleanWs notFailBuild: true
          checkout scm

          def repoStr = """[storm-test-${PLATFORM}]
name=storm-test-${PLATFORM}
baseurl=${env.JOB_URL}/lastSuccessfulBuild/artifact/rpms/${PLATFORM}/
protect=1
enabled=1
priority=1
gpgcheck=0
"""
          def sourceRepoStr = """[storm-test-source-${PLATFORM}]
name=storm-test-source-${PLATFORM}
baseurl=${env.JOB_URL}/lastSuccessfulBuild/artifact/srpms/${PLATFORM}/
protect=1
enabled=1
priority=1
gpgcheck=0
"""
          dir('rpm') {
            sh 'sh build.sh'
            writeFile file: "rpms/storm-test-${PLATFORM}.repo", text: "${repoStr}"
            writeFile file: "srpms/storm-test-source-${PLATFORM}.repo", text: "${sourceRepoStr}"
            archiveArtifacts 'rpms/**, srpms/**'
          }
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
        if ('SUCCESS'.equals(currentBuild.result)) {
          slackSend color: 'good', message: "${env.JOB_NAME} - #${env.BUILD_ID} Back to normal (<${env.BUILD_URL}|Open>)"
        }
      }
    }
  }
}
