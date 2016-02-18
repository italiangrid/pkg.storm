#!/bin/bash
set -ex

# install addictional packages
wget --no-check-certificate https://raw.githubusercontent.com/cnaf/ci-puppet-modules/master/modules/puppet-gpfs-repo/files/gpfs.repo -O /etc/yum.repos.d/gpfs.repo
yum -y install pkgconfig \
  swig \
  libacl-devel \
  gpfs.base \
  gpfs.docs \
  gpfs.gpl \
  gpfs.msg.en_US \
  lcmaps-without-gsi-devel \
  lcmaps-interface
