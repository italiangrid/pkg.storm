#!/bin/bash
set -ex

#rpm --import http://repository.egi.eu/sw/production/umd/UMD-RPM-PGP-KEY
yum install -y yum-utils

# Install StoRM stable repository
yum-config-manager --add-repo https://repo.cloud.cnaf.infn.it/repository/storm/storm-stable-redhat9.repo

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
  storm-xmlrpc-c-devel
