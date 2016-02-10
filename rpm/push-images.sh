#!/bin/bash

components="storm-backend-server"

for c in ${components}; do
  pushd $c
  sh push-images.sh
  popd
done
