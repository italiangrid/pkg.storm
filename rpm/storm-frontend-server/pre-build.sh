#!/bin/bash
set -ex

# install addictional packages
yum install -y gcc \
  gcc-c++ \
  make \
  gsoap-devel \
  curl-devel \
  mysql-devel \
  globus-gssapi-gsi-devel \
  globus-gss-assist-devel \
  globus-common-devel \
  globus-gridmap-callout-error-devel \
  globus-gsi-credential-devel \
  CGSI-gSOAP-devel \
  storm-xmlrpc-c-devel \
  argus-pep-api-c \
  argus-pep-api-c-devel

el_version=$(lsb_release -rs | cut -f1 -d.)

if [ $el_version == "5" ]; then

  yum install -y boost141-devel

else

  yum install -y libuuid-devel boost-devel

fi
