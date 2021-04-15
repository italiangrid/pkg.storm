#!/bin/bash
set -ex

yum -y install pkgconfig \
  swig \
  libacl-devel \
  gpfs.base \
  lcmaps-without-gsi-devel \
  lcmaps-interface

yum -y install java-11-openjdk-devel
javac -version
