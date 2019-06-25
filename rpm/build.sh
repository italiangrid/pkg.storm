#!/bin/bash
set -ex

set -a
source ./build.env
set +a

ALL_COMPONENTS="storm-xmlrpc-c \
                storm-backend-server \
                storm-frontend-server \
                storm-webdav \
                storm-client \
                yaim-storm \
                storm-dynamic-info-provider \
                storm-gridftp-dsi \
                storm-native-libs \
                cdmi-storm \
                emi-storm-backend-mp \
                emi-storm-frontend-mp \
                emi-storm-globus-gridftp-mp"

PLATFORM=${PLATFORM:-centos7}
COMPONENTS=${COMPONENTS:-${ALL_COMPONENTS}}

UMD_REPO_RPM=${UMD_REPO_RPM:-"http://repository.egi.eu/sw/production/umd/4/centos7/x86_64/updates/umd-release-4.1.3-1.el7.centos.noarch.rpm"}

pkg_base_image_name="italiangrid/pkg.base:${PLATFORM}"

if [ -z "${SKIP_PKG_BASE_PULL_IMAGE}" ]; then
 docker pull ${pkg_base_image_name}
fi

if [ -n "${USE_DOCKER_REGISTRY}" ]; then
  pkg_base_image_name="${DOCKER_REGISTRY_HOST}/${pkg_base_image_name}"
fi

if [ -z ${MVN_REPO_VOLUME_NAME+x} ]; then
  mvn_volume_name=$(basename $(mktemp -u -t mvn-repo.XXXXX))
  # Create mvn repo volume
  docker volume create ${mvn_volume_name}
else
  mvn_volume_name=${MVN_REPO_VOLUME_NAME}
fi

if [ -z ${DATA_VOLUME_NAME+x} ]; then
  data_volume_name=$(basename $(mktemp -u -t data-container.XXXXX))
  # Create data container volume
  docker volume create ${data_volume_name}
else
  data_volume_name=${DATA_VOLUME_NAME}
fi

if [ -z ${SOURCE_DATA_VOLUME_NAME+x} ]; then
  source_data_volume_name=$(basename $(mktemp -u -t source-data-container.XXXXX))
  # Create data container volume
  docker volume create ${source_data_volume_name}
else
  source_data_volume_name=${SOURCE_DATA_VOLUME_NAME}
fi

# Container label
label=$(basename $(mktemp -u -t pkg-storm.XXXXX))

# Run packaging
for c in ${COMPONENTS}; do
  build_env_file="$c/build-env"

  build_env=""

  comp_name=$(echo ${c} | tr '[:lower:]' '[:upper:]' | tr '-' '_')

  var_names="SUDO_BUILD BUILD_REPO PKG_PACKAGES_DIR PKG_STAGE_DIR PKG_STAGE_SOURCE_DIR PKG_TAG PKG_REPO PKG_STAGE_RPMS PKG_STAGE_SRPMS UMD_REPO_RPM"

  for v in ${var_names}; do
    c_var_name="${v}_${comp_name}"

    if [ -n "${!c_var_name}" ]; then
      build_env="${build_env} -e ${v}=${!c_var_name}"
    elif [ -n "${!v}" ]; then
        build_env="${build_env} -e ${v}=${!v}"
    fi
  done

  if [ -n "${INCLUDE_BUILD_NUMBER}" ]; then
    build_env="${build_env} -e BUILD_NUMBER=${BUILD_NUMBER:-test}"
  fi

  docker run -i -v ${mvn_volume_name}:/m2-repository \
    -v ${data_volume_name}:/stage-area \
    -v ${source_data_volume_name}:/stage-area-source \
    ${DOCKER_ARGS} \
    --env-file ${build_env_file} \
    ${build_env} \
    --label ${label} \
    ${pkg_base_image_name}
done

docker container prune -f --filter label=${label}

CID=`docker run -d -v ${data_volume_name}:/stage-area -v ${source_data_volume_name}:/stage-area-source busybox true`
docker cp ${CID}:/stage-area rpms
docker cp ${CID}:/stage-area-source srpms
docker rm -f ${CID}

if [ -z "${MVN_REPO_VOLUME_NAME+x}" ]; then
  docker volume rm -f ${MVN_REPO_VOLUME_NAME}
fi

if [ -z "${DATA_VOLUME_NAME+x}" ]; then
  docker volume rm -f ${DATA_VOLUME_NAME}
fi

if [ -z "${SOURCE_DATA_VOLUME_NAME+x}" ]; then
  docker volume rm -f ${SOURCE_DATA_VOLUME_NAME}
fi
