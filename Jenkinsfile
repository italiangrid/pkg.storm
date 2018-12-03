def label = "worker-${UUID.randomUUID().toString()}"
def dataContainerName = "stage-area-pkg.storm-${env.JOB_BASE_NAME}-${env.BUILD_NUMBER}"

podTemplate(
    label: label,
    cloud: 'Kube mwdevel',
    nodeSelector: 'zone=ci-test',
    containers: [
        containerTemplate(
          name: 'pkg-storm-runner',
          image: 'italiangrid/kube-docker-runner:latest',
          command: 'cat',
          ttyEnabled: true,
          resourceRequestCpu: '1',
          resourceLimitCpu: '1.5',
          resourceRequestMemory: '1Gi',
          resourceLimitMemory: '1.5Gi'
        )
    ],
    volumes: [
        hostPathVolume(mountPath: '/var/run/docker.sock', hostPath: '/var/run/docker.sock'),
        secretVolume(mountPath: '/home/jenkins/.docker', secretName: 'registry-auth-basic'),
        secretVolume(mountPath: '/home/jenkins/.ssh', secretName: 'jenkins-ssh-keys'),
        persistentVolumeClaim(mountPath: '/srv/scratch', claimName: 'scratch-area-claim', readOnly: false)
    ],
    imagePullSecrets: ['jenkins-docker-registry'],
    envVars: [
        envVar(key: 'DATA_CONTAINER_NAME', value: dataContainerName)
    ]
) {

    parameters {
      string(name: 'PLATFORM', defaultValue: 'centos6', description: 'OS Platform')
    }

    node(label) {

        try {
            stage('package') {
                container('pkg-storm-runner') {

                    script {
                        cleanWs notFailBuild: true
                        checkout scm
                        sh "docker create -v /stage-area --name ${DATA_CONTAINER_NAME} italiangrid/pkg.base:centos6"
                        sh '''
                        pushd rpm
                        ls -al
                        sh build.sh
                        popd
                        '''
                        sh "docker cp ${DATA_CONTAINER_NAME}:/stage-area rpms"

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

                        sh "docker cp ${DATA_CONTAINER_NAME}:/stage-area-source srpms"

                        def sourceRepoStr = """[storm-test-source-${params.PLATFORM}]
name=storm-test-source-${params.PLATFORM}
baseurl=${env.JOB_URL}/lastSuccessfulBuild/artifact/srpms/${params.PLATFORM}/
protect=1
enabled=1
priority=1
gpgcheck=0
"""
                        writeFile file: "srpms/storm-test-source-${params.PLATFORM}.repo", text: "${sourceRepoStr}"

                        sh "docker rm -f ${DATA_CONTAINER_NAME}"
                    }

                    archiveArtifacts 'rpms/**, srpms/**'
                }
            }

        } catch (error) {

            slackSend color: 'danger', message: "${env.JOB_NAME} - #${env.BUILD_ID} Failure (<${env.BUILD_URL}|Open>)"

        } finally {

            script {
                if('SUCCESS'.equals(currentBuild.result)) {
                    slackSend color: 'good', message: "${env.JOB_NAME} - #${env.BUILD_ID} Back to normal (<${env.BUILD_URL}|Open>)"
                }
            }
        }
    }
}
