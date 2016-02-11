#!/bin/bash

components="storm-backend-server storm-webdav storm-client storm-native-libs"

for c in ${components}; do
  pushd $c
  sh build-images.sh
  popd
done
