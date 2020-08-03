#!/bin/bash
set -ex

yum localinstall -y http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/e/epel-release-7-11.noarch.rpm
yum install redhat-lsb-core -y

yum -y install pkgconfig \
  swig \
  libacl-devel \
  gpfs.base \
  lcmaps-without-gsi-devel \
  lcmaps-interface
