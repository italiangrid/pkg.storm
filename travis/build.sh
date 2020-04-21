#!/bin/bash
set -ex

error_handler() {
  echo ERROR: An error was encountered with the build.
  upload_report
  dump_output
  exit 1
}

trap 'error_handler' ERR

rm -rf artifacts
mkdir -p artifacts
./setup-volumes.sh
pushd rpm
pkg-build.sh
popd
./copy-artifacts.sh

exit $rc
