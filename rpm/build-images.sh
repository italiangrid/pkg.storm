#!/bin/bash

components="storm-backend-server storm-webdav storm-client storm-gridhttps-server yaim-storm storm-dynamic-info-provider storm-gridftp-dsi"

for c in ${components}; do
  pushd $c
  sh build-images.sh
  popd
done
