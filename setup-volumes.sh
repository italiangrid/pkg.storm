#!/bin/bash
set -ex

PACKAGES_VOLUME=${PACKAGES_VOLUME:-packages-volume-pkg.storm}
STAGE_AREA_VOLUME=${STAGE_AREA_VOLUME:-stage-area-volume-pkg.storm}
MVN_REPO_VOLUME=${MVN_REPO_VOLUME:-mvn-repo-volume-pkg.storm}

export PACKAGES_VOLUME=$(docker volume create ${PACKAGES_VOLUME})
export STAGE_AREA_VOLUME=$(docker volume create ${STAGE_AREA_VOLUME})
export MVN_REPO_VOLUME=$(docker volume create ${MVN_REPO_VOLUME})
