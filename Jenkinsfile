#!/usr/bin/env groovy

def platform2Dir = [
  "centos7" : 'rpm',
  "centos8" : 'rpm',
  "centos7java11" : 'rpm',
]

def buildPackages(platform, platform2Dir, includeBuildNumber) {
  return {
    unstash "source"

    def platformDir = platform2Dir[platform]

    if (!platformDir) {
      error("Unknown platform: ${platform}")
    }

    def includeEnv = ""
    if (includeBuildNumber) {
      includeEnv = "INCLUDE_BUILD_NUMBER=1"
    }

    dir(platformDir) {
      sh "PLATFORM=${platform} ${includeEnv} pkg-build.sh"
    }
  }
}

pipeline {
  agent { label 'docker' }

  options {
    timeout(time: 1, unit: 'HOURS')
    buildDiscarder(logRotator(numToKeepStr: '5'))
  }

  triggers { cron('@daily') }

  parameters {
    booleanParam(name: 'INCLUDE_BUILD_NUMBER', defaultValue: true, description: 'Include build number into rpm name')
  }

  environment {
    PLATFORMS = "centos7java11 centos8"
    PKG_TAG = "${env.BRANCH_NAME}"
    PACKAGES_VOLUME = "pkg-vol-${env.BUILD_TAG}"
    STAGE_AREA_VOLUME = "sa-vol-${env.BUILD_TAG}"
    PKG_BUILD_NUMBER = "${env.BUILD_NUMBER}"
    DOCKER_REGISTRY_HOST = "${env.DOCKER_REGISTRY_HOST}"
    DOCKER_ARGS = "--rm -v /opt/cnafsd/helper-scripts/scripts/:/usr/local/bin"
  }

  stages{
    stage('checkout') {
      steps {
        deleteDir()
        checkout scm
        stash name: "source", includes: "**"
      }
    }

    stage('setup-volumes') {
      steps {
        sh 'pwd && ls -lR'
        sh 'rm -rf artifacts && mkdir -p artifacts'
        sh './setup-volumes.sh'
      }
    }

    stage('package') {
      steps {
        script {
          if (params.INCLUDE_BUILD_NUMBER) {
            env.INCLUDE_BUILD_NUMBER = '1'
          }
          def buildStages = PLATFORMS.split(' ').collectEntries {
            [ "${it} build packages" : buildPackages(it, platform2Dir, params.INCLUDE_BUILD_NUMBER ) ]
          }
          parallel buildStages
        }
      }
    }

    stage('archive-artifacts') {
      steps {
        sh './copy-artifacts.sh'
        archiveArtifacts "artifacts/**"
        stash name: "packages", includes: "artifacts/packages/**"
      }
    }

    stage('cleanup') {
      steps {
          sh 'docker volume rm ${PACKAGES_VOLUME} ${STAGE_AREA_VOLUME} || echo Volume removal failed'
      }
    }
  }

  post {
    failure {
      slackSend color: 'danger', message: "${env.JOB_NAME} - #${env.BUILD_NUMBER} Failure (<${env.BUILD_URL}|Open>)"
    }
    
    changed {
      script {
        if('SUCCESS'.equals(currentBuild.currentResult)) {
          slackSend color: 'good', message: "${env.JOB_NAME} - #${env.BUILD_NUMBER} Back to normal (<${env.BUILD_URL}|Open>)"
        }
      }
    }
  }
}
