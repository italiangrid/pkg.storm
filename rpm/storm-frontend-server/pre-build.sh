#!/bin/bash
set -ex

yum install -y libuuid-devel boost-devel

rpm --import http://repository.egi.eu/sw/production/umd/UMD-RPM-PGP-KEY
yum install -y ${UMD_REPO_RPM}

# We want to give more priority to the stage area repo than UMD
sed -i "s/priority=1/priority=2/" /etc/yum.repos.d/UMD-*-base.repo /etc/yum.repos.d/UMD-*-updates.repo 

#if [ ${PLATFORM} == "centos7" ]; then
#
#  # storm is not currently included into UMD-4 RHEL7 repository
#  wget http://italiangrid.github.io/storm/repo/storm_sl6.repo -O /etc/yum.repos.d/storm_sl6.repo
#fi

yum install -y pkgconfig \
  boost-devel \
  curl-devel \
  mysql-devel \
  globus-gssapi-gsi-devel \
  globus-gss-assist-devel \
  globus-common-devel \
  globus-gridmap-callout-error-devel \
  globus-gsi-credential-devel \
  krb5-devel \
  gsoap-devel \
  CGSI-gSOAP-devel \
  libuuid-devel \
  voms \
  gcc \
  gcc-c++ \
  storm-xmlrpc-c-devel \
  argus-pep-api-c \
  argus-pep-api-c-devel
