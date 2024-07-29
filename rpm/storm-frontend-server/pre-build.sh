#!/bin/bash
set -ex

#rpm --import http://repository.egi.eu/sw/production/umd/UMD-RPM-PGP-KEY
yum install -y yum-utils

# Install StoRM stable repository
yum-config-manager --add-repo https://repo.cloud.cnaf.infn.it/repository/storm/storm-stable-redhat9.repo

yum install -y autoconf \
  autoconf-archive \
  automake \
  bear \
  bison \
  boost-devel \
  diffutils \
  CGSI-gSOAP-devel \
  file \
  gcc-c++ \
  gdb \
  git \
  globus-common-devel \
  gsoap-devel \
  libtool \
  libuuid-devel \
  make \
  mariadb-devel \
  openssl-devel \
  xmlrpc-c-devel