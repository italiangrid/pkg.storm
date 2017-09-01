#!/bin/bash
set -ex

# Fix gsoap dependency error:
#
# Error: Package: gsoap-devel-2.7.16-5.el6.x86_64 (epel)
#           Requires: gsoap = 2.7.16-5.el6
#           Available: gsoap-2.7.16-3.el6.x86_64 (UMD-3-updates)
#               gsoap = 2.7.16-3.el6
#           Available: gsoap-2.7.16-4.el6.i686 (UMD-3-updates)
#               gsoap = 2.7.16-4.el6
yum --disablerepo=*UMD* install -y gsoap-devel

# install addictional packages
yum -y install pkgconfig \
  globus-gssapi-gsi-devel \
  globus-gss-assist-devel \
  gsoap-devel \
  CGSI-gSOAP-devel \
  voms
