#!/bin/bash
set -ex

# install addictional packages
yum -y install globus-gssapi-gsi-devel \
  globus-gss-assist-devel \
  globus-gsi-credential-devel
