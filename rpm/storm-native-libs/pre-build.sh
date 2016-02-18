#!/bin/bash
set -ex

# install addictional packages
yum -y install pkgconfig \
  swig \
  libacl-devel \
  gpfs.base \
  lcmaps-without-gsi-devel \
  lcmaps-interface
