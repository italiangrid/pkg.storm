#!/bin/bash
set -ex

# install addictional packages
yum -y install pkgconfig \
  zlib \
  openssl-devel \
  libattr-devel \
  globus-gridftp-server-devel \
  globus-ftp-control-devel \
  globus-ftp-client-devel
