#!/bin/bash
set -ex

yum localinstall -y http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/e/epel-release-7-11.noarch.rpm
yum install dkms -y

yum -y install pkgconfig \
  swig \
  libacl-devel \
  gpfs.base-3.4.0 \
  lcmaps-without-gsi-devel \
  lcmaps-interface
