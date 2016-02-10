#!/bin/bash

components="storm-webdav storm-backend-server"

for c in ${components}; do
  pushd $c
  sh build-images.sh
  popd
done
