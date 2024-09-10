#!/bin/bash

IMAGE="condaforge/mambaforge"
PLATFORM="linux/arm64"

if [ -z "$1" ]
then
      echo "Image was not set, using $IMAGE"
else
IMAGE="$1"
echo "Setting Docker container to $IMAGE"
fi

docker run --cap-add=SYS_PTRACE \
           --privileged \
           --security-opt \
           seccomp=unconfined \
           -v `pwd`:/data \
           --platform "$PLATFORM" \
           -t -i \
           "$IMAGE"


#valgrind --tool=memcheck ./bin/pdal_io_stac_reader_test --gtest_filter=StacReaderTest.multiple_readers_test --gtest_catch_exceptions=0 > vgrind.txt 2>&1
#lldb -- ./bin/pdal_io_stac_reader_test --gtest_filter=StacReaderTest.multiple_readers_test --gtest_catch_exceptions=0
