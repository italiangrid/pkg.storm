#!/bin/bash
set -ex

# Override GPFS repo
rm /etc/yum.repos.d/gpfs.repo
wget -P /etc/yum.repos.d https://ci.cloud.cnaf.infn.it/job/repo_gpfs/lastSuccessfulBuild/artifact/gpfs.repo

yum -y install pkgconfig \
  swig \
  libacl-devel \
  gpfs.base-3.4.0 \
  lcmaps-without-gsi-devel \
  lcmaps-interface
