#!/bin/bash
set -ex

# install addictional packages

yum install -y redhat-lsb
el_version=$(lsb_release -rs | cut -f1 -d.)

if [ $el_version == "5" ]; then

  yum install --disableplugin=priorities -y boost141-devel

  rpm --import http://repository.egi.eu/sw/production/umd/UMD-RPM-PGP-KEY
  wget http://repository.egi.eu/sw/production/umd/3/sl5/x86_64/updates/umd-release-3.0.1-1.el5.noarch.rpm
  yum localinstall -y umd-release-3.0.1-1.el5.noarch.rpm

  # storm-xmlrpc-c-devel is missing from UMD-3 repositories
  wget http://italiangrid.github.io/storm/repo/storm_sl5.repo -O /etc/yum.repos.d/storm_sl5.repo

fi

if [ $el_version == "6" ]; then

  yum install -y libuuid-devel boost-devel

  rpm --import http://repository.egi.eu/sw/production/umd/UMD-RPM-PGP-KEY
  yum install -y http://repository.egi.eu/sw/production/umd/3/sl6/x86_64/updates/umd-release-3.14.3-1.el6.noarch.rpm

  # storm-xmlrpc-c-c++ is broken into UMD-3 repositories
  wget http://italiangrid.github.io/storm/repo/storm_sl6.repo -O /etc/yum.repos.d/storm_sl6.repo
fi

if [ $el_version == "7" ]; then

  yum install -y libuuid-devel boost-devel

  rpm --import http://repository.egi.eu/sw/production/umd/UMD-RPM-PGP-KEY
  yum install -y http://repository.egi.eu/sw/production/umd/4/centos7/x86_64/updates/umd-release-4.1.2-1.el7.centos.noarch.rpm

  # storm is not currently included into UMD-4 repositories
  wget http://italiangrid.github.io/storm/repo/storm_sl6.repo -O /etc/yum.repos.d/storm_sl6.repo
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
