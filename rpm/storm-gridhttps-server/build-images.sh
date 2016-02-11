#!/bin/bash
set -ex

IMAGE_TAG=italiangrid/pkg.storm-storm-gridhttps-server
tags=${tags:-"centos5 centos6 centos7"}

for t in ${tags}; do
  docker build -t ${IMAGE_TAG}:${t} -f Dockerfile.${t} .
done
