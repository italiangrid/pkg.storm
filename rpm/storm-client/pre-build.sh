#!/bin/bash
set -ex

# install addictional packages
yum -y install g++ \
  gsoap-devel \
  voms \
  CGSI-gSOAP-devel \
  which \
  openssl-devel \
  zlib-devel
