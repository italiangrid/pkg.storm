#!/bin/bash
set -ex

# install addictional packages
yum -y install pkgconfig \
  globus-gssapi-gsi-devel \
  globus-gss-assist-devel \
  gsoap-devel \
  CGSI-gSOAP-devel \
  voms
