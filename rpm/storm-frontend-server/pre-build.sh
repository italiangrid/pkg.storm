#!/bin/bash
set -ex

# install addictional packages

yum install -y redhat-lsb
el_version=$(lsb_release -rs | cut -f1 -d.)

if [ $el_version == "5" ]; then

  wget http://emisoft.web.cern.ch/emisoft/dist/EMI/3/sl5/x86_64/base/emi-release-3.0.0-2.el5.noarch.rpm
  yum localinstall --nogpgcheck -y emi-release-3.0.0-2.el5.noarch.rpm

  yum install -y boost141-devel

else

  wget --no-check-certificate http://emisoft.web.cern.ch/emisoft/dist/EMI/3/sl6/x86_64/base/emi-release-3.0.0-2.el6.noarch.rpm
  yum localinstall --nogpgcheck -y emi-release-3.0.0-2.el6.noarch.rpm

  yum install -y libuuid-devel boost-devel

fi

yum install -y pkgconfig \
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
