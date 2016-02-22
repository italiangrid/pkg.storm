#!/bin/bash
set -ex

# install addictional packages
yum install -y pkgconfig \
  subversion \
  curl-devel \
  libxml2-devel \
  readline-devel \
  ncurses-devel \
  autoconf \
  rpm-build
