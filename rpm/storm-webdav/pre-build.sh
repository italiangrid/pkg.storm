#!/bin/bash
set -ex

yum -y install java-11-openjdk-devel
javac -version
