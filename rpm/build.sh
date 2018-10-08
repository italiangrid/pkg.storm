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

PLATFORM=${PLATFORM:-centos6}
COMPONENTS=${COMPONENTS:-${ALL_COMPONENTS}}

UMD_REPO_RPM=${UMD_REPO_RPM:-"http://repository.egi.eu/sw/production/umd/3/sl6/x86_64/updates/umd-release-3.14.4-1.el6.noarch.rpm"}

pkg_base_image_name="italiangrid/pkg.base:${PLATFORM}"

if [ -z "${SKIP_PKG_BASE_PULL_IMAGE}" ]; then
 docker pull ${pkg_base_image_name}
fi 

if [ -n "${USE_DOCKER_REGISTRY}" ]; then
  pkg_base_image_name="${DOCKER_REGISTRY_HOST}/${pkg_base_image_name}"
fi

if [ -z ${MVN_REPO_CONTAINER_NAME+x} ]; then
  mvn_repo_name=$(basename $(mktemp -u -t mvn-repo-XXXXX))
  # Create mvn repo container
  docker create -v /m2-repository --name ${mvn_repo_name} ${pkg_base_image_name}
else
  mvn_repo_name=${MVN_REPO_CONTAINER_NAME}
fi

# Run packaging
for c in ${COMPONENTS}; do
  build_env_file="$c/build-env"

  build_env=""

  comp_name=$(echo ${c} | tr '[:lower:]' '[:upper:]' | tr '-' '_')

  var_names="BUILD_REPO PKG_PACKAGES_DIR PKG_STAGE_DIR PKG_STAGE_SOURCE_DIR PKG_TAG PKG_REPO PKG_STAGE_RPMS PKG_STAGE_SRPMS UMD_REPO_RPM"

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

  if [ -n "${DATA_CONTAINER_NAME}" ]; then
    volumes_conf="${volumes_conf} --volumes-from ${DATA_CONTAINER_NAME}"
  fi

  docker run -i --volumes-from ${mvn_repo_name} \
    ${volumes_conf} \
    ${DOCKER_ARGS} \
    --env-file ${build_env_file} \
    ${build_env} \
    ${pkg_base_image_name}
done
