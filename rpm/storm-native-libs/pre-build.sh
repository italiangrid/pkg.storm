#!/bin/bash
set -ex

yum -y install pkgconfig \
  swig \
  libacl-devel \
  gpfs.base-3.4.0 \
  lcmaps-without-gsi-devel \
  lcmaps-interface \
  dkms
