pipeline {
  agent { label 'docker' }

  options {
    timeout(time: 1, unit: 'HOURS')
    buildDiscarder(logRotator(numToKeepStr: '5'))
  }

  parameters {
    string(name: 'PLATFORM', defaultValue: 'centos6', description: 'OS Platform')
  }

  stages{
    stage('package') {
      environment {
        DATA_CONTAINER_NAME = "stage-area-pkg.storm-${env.BUILD_ID}"
        PLATFORM = "${params.PLATFORM}"
      }
      steps {
        git(url: 'https://github.com/italiangrid/pkg.storm.git', branch: env.BRANCH_NAME)
        sh 'docker create -v /stage-area --name ${DATA_CONTAINER_NAME} italiangrid/pkg.base:centos6'
        sh '''
        pushd rpm
        ls -al
        sh build.sh
        popd
        '''
        sh 'docker cp ${DATA_CONTAINER_NAME}:/stage-area repo'
        sh 'docker rm -f ${DATA_CONTAINER_NAME}'

        script {
          def c = """[storm-test-${params.PLATFORM}]
name=storm-test-${params.PLATFORM}
baseurl=https://ci.cloud.cnaf.infn.it/job/pkg.storm/job/fix%252FSTOR-945/lastSuccessfulBuild/artifact/repo/${params.PLATFORM}/
protect=1
enabled=1
priority=1
gpgcheck=0
"""
          writeFile file: "repo/storm-test-${params.PLATFORM}.repo", text: "${c}"
        }

        archiveArtifacts 'repo/**'
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