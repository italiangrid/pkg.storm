#!/bin/bash
set -ex

# We need UMD repos for Argus pep-c deps
UMD_REPO_PACKAGE_EL6="http://repository.egi.eu/sw/production/umd/3/sl6/x86_64/updates/umd-release-3.14.3-1.el6.noarch.rpm"

rpm --import http://repository.egi.eu/sw/production/umd/UMD-RPM-PGP-KEY

yum localinstall -y ${UMD_REPO_PACKAGE_EL6} && yum -y update

# We want to give more priority to the stage area repo than UMD
sed -i "s/priority=1/priority=2/" /etc/yum.repos.d/UMD-3-base.repo /etc/yum.repos.d/UMD-3-updates.repo 

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
