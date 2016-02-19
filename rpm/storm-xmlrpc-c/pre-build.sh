#!/bin/bash
set -ex

# install addictional packages
yum install -y pkgconfig \
  curl-devel \
  libxml2-devel \
  readline-devel \
  ncurses-devel
