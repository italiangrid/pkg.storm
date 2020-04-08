#!/bin/bash
set -ex

rpm --import http://repository.egi.eu/sw/production/umd/UMD-RPM-PGP-KEY
yum install -y yum-priorities lsb_release

majversion=$(lsb_release -rs | cut -f1 -d.)

# Install UMD repositories
if [ $majversion = "7" ]; then

  umd_release="http://repository.egi.eu/sw/production/umd/4/centos7/x86_64/updates/umd-release-4.1.3-1.el7.centos.noarch.rpm"

#  # storm is not currently included into UMD-4 RHEL7 repository
#  wget http://italiangrid.github.io/storm/repo/storm_sl6.repo -O /etc/yum.repos.d/storm_sl6.repo
else 
  umd_release="http://repository.egi.eu/sw/production/umd/4/sl6/x86_64/updates/umd-release-4.1.3-1.el6.noarch.rpm"
fi
yum localinstall -y $umd_release

# We want to give more priority to the stage area repo than UMD
sed -i "s/priority=1/priority=2/" /etc/yum.repos.d/UMD-*-base.repo /etc/yum.repos.d/UMD-*-updates.repo 

yum install -y pkgconfig \
  curl-devel \
  boost-devel \
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
