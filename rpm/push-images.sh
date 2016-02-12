#!/bin/bash

components="storm-backend-server \
  storm-webdav \
  storm-client \
  storm-gridhttps-server \
  yaim-storm \
  storm-dynamic-info-provider \
  storm-grdftp-dsi"

for c in ${components}; do
  pushd $c
  sh push-images.sh
  popd
done
