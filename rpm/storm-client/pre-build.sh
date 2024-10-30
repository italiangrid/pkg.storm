#!/bin/bash
set -ex

# install addictional packages
yum -y install autoconf \
  autoconf-archive \
  automake \
  pkgconfig \
  globus-gssapi-gsi-devel \
  globus-gss-assist-devel \
  globus-common-devel \
  globus-gsi-credential-devel \
  gsoap-devel \
  CGSI-gSOAP-devel \
  voms
