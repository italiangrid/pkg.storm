#!/bin/bash
set -ex

yum -y install pkgconfig \
  swig \
  libacl-devel \
  gpfs.base \
  lcmaps-without-gsi-devel \
  lcmaps-interface
