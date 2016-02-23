#!/bin/bash
set -ex

PLATFORM=${PLATFORM:-centos6}
COMPONENTS=${COMPONENTS:-"storm-backend-server storm-frontend-server storm-xmlrpc-c storm-webdav storm-client storm-gridhttps-server yaim-storm storm-dynamic-info-provider storm-gridftp-dsi storm-native-libs"}

pkg_base_image_name="italiangrid/pkg.base:${PLATFORM}"

if [ -n "${USE_DOCKER_REGISTRY}" ]; then
  pkg_base_image_name="${DOCKER_REGISTRY_HOST}/${pkg_base_image_name}"
fi

docker pull ${pkg_base_image_name}

if [ -z ${MVN_REPO_CONTAINER_NAME+x} ]; then
  mvn_repo_name=$(basename $(mktemp -u -t mvn-repo-XXXXX))
  # Create mvn repo container
  docker create -v /m2-repository --name ${mvn_repo_name} ${pkg_base_image_name}
else
  mvn_repo_name=${MVN_REPO_CONTAINER_NAME}
fi

# Run packaging
for c in ${COMPONENTS}; do
  build_env=""

  while read -r line
  do
    build_env="${build_env} -e ${line}"
  done < "$c/build-env"

  if [ -n "${PKG_BUILD_NUMBER}" ]; then
    build_env="${build_env} -e BUILD_NUMBER=${PKG_BUILD_NUMBER}"
  fi

  if [ -n "${PKG_PACKAGES_DIR}" ]; then
    build_env="${build_env} -e PKG_PACKAGES_DIR=${PKG_PACKAGES_DIR}"
  fi

  if [ -n "${PKG_STAGE_DIR}" ]; then
    build_env="${build_env} -e PKG_STAGE_DIR=${PKG_STAGE_DIR}"
  fi

  if [ -n "${PKG_REPO}" ]; then
    build_env="${build_env} -e PKG_REPO=${PKG_REPO}"
  fi

  if [ -n "${DATA_CONTAINER_NAME}" ]; then
    volumes_conf="${volumes_conf} --volumes-from ${DATA_CONTAINER_NAME}"
  fi

  if [ -n "${STAGE_ALL}" ]; then
      build_env="${build_env} -e PKG_STAGE_RPMS=1"
  fi

  if [ -n "${PKG_TAG}" ]; then
    build_env="${build_env} -e PKG_TAG=${PKG_TAG}"
  fi

  docker run -i --volumes-from ${mvn_repo_name} \
    ${volumes_conf} \
    ${build_env} \
    ${pkg_base_image_name}

done
