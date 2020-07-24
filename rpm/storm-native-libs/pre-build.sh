#!/bin/bash
set -ex

yum localinstall -y http://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/e/epel-release-7-11.noarch.rpm
yum install redhat-lsb-core -y

majversion=$(lsb_release -rs | cut -f1 -d.)

if $majversion=='6'
then
  yum -y install pkgconfig \
    swig \
    libacl-devel \
    gpfs.base-3.4.0 \
    lcmaps-without-gsi-devel \
    lcmaps-interface
else
  # missing modutils for centos7
  yum install module-init-tools -y
  rpm -Uvh --nodeps $(repoquery --location gpfs.base-3.4.0)

  yum -y install pkgconfig \
    swig \
    libacl-devel \
    lcmaps-without-gsi-devel \
    lcmaps-interface
fi
